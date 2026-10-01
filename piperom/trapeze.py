"""Seismic trapeze (brace) behaviour.

The Pinching4 parameter files in ``inputs/trapezes/`` are the single source of truth.
The equivalent static procedure uses a trilinear secant-stiffness idealisation derived from them:

    first branch  : origin -> envelope point 2   (point 1 is ignored)
    second branch : envelope point 2 -> envelope point 3
    third branch  : slope = POST_YIELD_STIFFNESS_RATIO * first-branch slope

Only the positive envelope is used by the static procedure (the response is symmetric).
"""

from __future__ import annotations

import csv
import io
from dataclasses import dataclass
from pathlib import Path

from . import TRAPEZES_DIR

DEFAULT_TRAPEZE_FILES = {
    "transverse": TRAPEZES_DIR / "pinching4_C-TPS-T.csv",
    "longitudinal": TRAPEZES_DIR / "pinching4_C-TPS-L.csv",
}

POST_YIELD_STIFFNESS_RATIO = 0.01

# Parameter names without their one-letter prefix ("T"/"L" in the default files).
_ENVELOPE = [f"e{s}{q}{i}" for s in "PN" for q in "fd" for i in range(1, 5)]
_CYCLIC = ["rDispP", "rForceP", "uForceP", "rDispN", "rForceN", "uForceN"]
_DAMAGE = (
    [f"gK{i}" for i in range(1, 5)] + ["gKLim"]
    + [f"gD{i}" for i in range(1, 5)] + ["gDLim"]
    + [f"gF{i}" for i in range(1, 5)] + ["gFLim"]
    + ["gE"]
)
PARAMETER_NAMES = _ENVELOPE + _CYCLIC + _DAMAGE + ["dmgType"]


@dataclass(frozen=True)
class Pinching4:
    """Pinching4 parameters of one trapeze (OpenSees uniaxialMaterial Pinching4)."""

    name: str
    pos_force: tuple[float, float, float, float]
    pos_disp: tuple[float, float, float, float]
    neg_force: tuple[float, float, float, float]
    neg_disp: tuple[float, float, float, float]
    r_disp_p: float
    r_force_p: float
    u_force_p: float
    r_disp_n: float
    r_force_n: float
    u_force_n: float
    g_k: tuple[float, float, float, float]
    g_k_lim: float
    g_d: tuple[float, float, float, float]
    g_d_lim: float
    g_f: tuple[float, float, float, float]
    g_f_lim: float
    g_e: float
    dmg_type: str

    @classmethod
    def from_parameters(cls, params: dict[str, str], name: str = "") -> "Pinching4":
        missing = [p for p in PARAMETER_NAMES if p not in params]
        if missing:
            raise ValueError(f"Trapeze file '{name}' is missing parameters: {', '.join(missing)}")

        def f(key):
            try:
                return float(params[key])
            except ValueError:
                raise ValueError(f"Trapeze file '{name}': parameter {key} must be a number") from None

        def four(prefix):
            return tuple(f(f"{prefix}{i}") for i in range(1, 5))

        p4 = cls(
            name=name,
            pos_force=four("ePf"), pos_disp=four("ePd"),
            neg_force=four("eNf"), neg_disp=four("eNd"),
            r_disp_p=f("rDispP"), r_force_p=f("rForceP"), u_force_p=f("uForceP"),
            r_disp_n=f("rDispN"), r_force_n=f("rForceN"), u_force_n=f("uForceN"),
            g_k=four("gK"), g_k_lim=f("gKLim"),
            g_d=four("gD"), g_d_lim=f("gDLim"),
            g_f=four("gF"), g_f_lim=f("gFLim"),
            g_e=f("gE"), dmg_type=params["dmgType"].strip(),
        )
        p4.validate()
        return p4

    def validate(self) -> None:
        pd, nd = self.pos_disp, self.neg_disp
        if not all(a < b for a, b in zip((0.0,) + pd[:-1], pd)):
            raise ValueError(f"Trapeze '{self.name}': positive envelope deformations must be > 0 and increasing")
        if not all(a > b for a, b in zip((0.0,) + nd[:-1], nd)):
            raise ValueError(f"Trapeze '{self.name}': negative envelope deformations must be < 0 and decreasing")
        if any(v <= 0 for v in self.pos_force) or any(v >= 0 for v in self.neg_force):
            raise ValueError(f"Trapeze '{self.name}': envelope forces must be > 0 (positive) and < 0 (negative)")
        if self.dmg_type not in ("cycle", "energy"):
            raise ValueError(f"Trapeze '{self.name}': dmgType must be 'cycle' or 'energy'")

    def parameters(self) -> dict[str, float | str]:
        """Unprefixed parameter dictionary (inverse of ``from_parameters``)."""
        out: dict[str, float | str] = {}
        for i in range(4):
            out[f"ePf{i+1}"] = self.pos_force[i]
        for i in range(4):
            out[f"ePd{i+1}"] = self.pos_disp[i]
        for i in range(4):
            out[f"eNf{i+1}"] = self.neg_force[i]
        for i in range(4):
            out[f"eNd{i+1}"] = self.neg_disp[i]
        out.update(rDispP=self.r_disp_p, rForceP=self.r_force_p, uForceP=self.u_force_p,
                   rDispN=self.r_disp_n, rForceN=self.r_force_n, uForceN=self.u_force_n)
        for key, vals, lim in (("gK", self.g_k, self.g_k_lim), ("gD", self.g_d, self.g_d_lim),
                               ("gF", self.g_f, self.g_f_lim)):
            for i in range(4):
                out[f"{key}{i+1}"] = vals[i]
            out[f"{key}Lim"] = lim
        out["gE"] = self.g_e
        out["dmgType"] = self.dmg_type
        return out

    def scaled(self, force_scale: float, disp_scale: float) -> "Pinching4":
        """Copy with envelope forces multiplied by ``force_scale`` and deformations by ``disp_scale``."""
        from dataclasses import replace

        return replace(
            self,
            pos_force=tuple(force_scale * v for v in self.pos_force),
            neg_force=tuple(force_scale * v for v in self.neg_force),
            pos_disp=tuple(disp_scale * v for v in self.pos_disp),
            neg_disp=tuple(disp_scale * v for v in self.neg_disp),
        )

    def opensees_args(self) -> list:
        """Arguments of ``uniaxialMaterial('Pinching4', tag, *args)``."""
        env = []
        for f, d in zip(self.pos_force, self.pos_disp):
            env += [f, d]
        for f, d in zip(self.neg_force, self.neg_disp):
            env += [f, d]
        return (env + [self.r_disp_p, self.r_force_p, self.u_force_p, self.r_disp_n, self.r_force_n, self.u_force_n]
                + [*self.g_k, self.g_k_lim, *self.g_d, self.g_d_lim, *self.g_f, self.g_f_lim, self.g_e, self.dmg_type])

    @classmethod
    def from_opensees_args(cls, args, name: str = "") -> "Pinching4":
        """Inverse of ``opensees_args`` (the tag excluded)."""
        a = list(args)
        if len(a) != 39:
            raise ValueError(f"Pinching4 needs 39 arguments after the tag, got {len(a)}")
        f = [float(v) for v in a[:38]]
        return cls(
            name=name,
            pos_force=tuple(f[0:8:2]), pos_disp=tuple(f[1:8:2]),
            neg_force=tuple(f[8:16:2]), neg_disp=tuple(f[9:16:2]),
            r_disp_p=f[16], r_force_p=f[17], u_force_p=f[18], r_disp_n=f[19], r_force_n=f[20], u_force_n=f[21],
            g_k=tuple(f[22:26]), g_k_lim=f[26], g_d=tuple(f[27:31]), g_d_lim=f[31],
            g_f=tuple(f[32:36]), g_f_lim=f[36], g_e=f[37], dmg_type=str(a[38]),
        )

    def to_csv(self, prefix: str = "") -> str:
        buf = io.StringIO()
        w = csv.writer(buf, lineterminator="\n")
        w.writerow(["parameter", "value", "description"])
        for key, val in self.parameters().items():
            w.writerow([prefix + key, _fmt(val), ""])
        return buf.getvalue()


def _fmt(v):
    if isinstance(v, float) and v.is_integer():
        return str(int(v))
    return str(v)


@dataclass(frozen=True)
class Trilinear:
    """Trilinear backbone used (as a secant stiffness) by the equivalent static procedure."""

    d1: float
    d2: float
    f1: float
    f2: float
    k3_ratio: float = POST_YIELD_STIFFNESS_RATIO

    @property
    def k1(self) -> float:
        return self.f1 / self.d1

    @property
    def k2(self) -> float:
        return (self.f2 - self.f1) / (self.d2 - self.d1)

    @property
    def k3(self) -> float:
        return self.k3_ratio * self.k1

    def secant_stiffness(self, disp: float) -> float:
        k1, k2, k3, d1, d2 = self.k1, self.k2, self.k3, self.d1, self.d2
        d_abs = abs(disp)
        if d_abs <= 1e-12:
            return k1
        F1 = k1 * d1
        F2 = F1 + k2 * (d2 - d1)
        if d_abs <= d1:
            F = k1 * d_abs
        elif d_abs <= d2:
            F = F1 + k2 * (d_abs - d1)
        else:
            F = F2 + k3 * (d_abs - d2)
        return F / d_abs

    def force(self, disp: float) -> float:
        return self.secant_stiffness(disp) * abs(disp)


def trilinear_from_pinching4(p: Pinching4) -> Trilinear:
    return Trilinear(d1=p.pos_disp[1], d2=p.pos_disp[2], f1=p.pos_force[1], f2=p.pos_force[2])


def parse_trapeze_csv(text: str, name: str = "") -> Pinching4:
    """Parse a trapeze file (columns ``parameter,value[,description]``).

    Parameter names carry a one-letter prefix (e.g. ``TePf1`` or ``LePf1``); any single
    leading letter is accepted, as long as it is the same for all rows.
    """
    rows = list(csv.reader(io.StringIO(text)))
    if not rows or [c.strip().lower() for c in rows[0][:2]] != ["parameter", "value"]:
        raise ValueError(f"Trapeze file '{name}': first row must be 'parameter,value,description'")
    params: dict[str, str] = {}
    prefixes = set()
    for row in rows[1:]:
        if not row or not row[0].strip():
            continue
        key = row[0].strip()
        if len(row) < 2:
            raise ValueError(f"Trapeze file '{name}': row '{key}' has no value")
        prefixes.add(key[0])
        params[key[1:]] = row[1].strip()
    if len(prefixes) > 1:
        raise ValueError(f"Trapeze file '{name}': mixed parameter prefixes {sorted(prefixes)}")
    return Pinching4.from_parameters(params, name=name)


def load_trapeze(source: str | Path | Pinching4 | None, kind: str) -> Pinching4:
    """Load a trapeze from ``None``/``"default"`` (bundled file), a CSV path, or pass a Pinching4 through."""
    if isinstance(source, Pinching4):
        return source
    if source is None or str(source) == "default":
        path = DEFAULT_TRAPEZE_FILES[kind]
    else:
        path = Path(source)
    return parse_trapeze_csv(path.read_text(), name=path.name)
