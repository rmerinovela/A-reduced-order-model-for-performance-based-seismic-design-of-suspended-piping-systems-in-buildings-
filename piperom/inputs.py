"""Input definitions: piping system and analysis settings, loaded from YAML files or dictionaries.

Defaults live only in ``inputs/defaults/*.yaml``; user files are deep-merged over them.
"""

from __future__ import annotations

import copy
import csv
import io
import math
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import numpy as np
import yaml

from . import DEFAULTS_DIR
from .trapeze import Pinching4, Trilinear, load_trapeze, trilinear_from_pinching4

# Limits imposed by the OpenSees tag numbering of the static model.
MAX_HANGERS = 299
MAX_BRANCHES = 9999
COORD_DECIMALS = 6          # coordinates are rounded to 1e-6 mm
BRANCH_BRACE_CLASH_TOL = 1e-2


class InputError(ValueError):
    """Invalid user input."""


# ----------------------------------------------------------------------------- helpers

def read_yaml(path: Path) -> dict:
    with open(path) as fh:
        data = yaml.safe_load(fh) or {}
    if not isinstance(data, dict):
        raise InputError(f"{path}: expected a mapping at the top level")
    return data


def deep_merge(base: dict, override: dict) -> dict:
    out = copy.deepcopy(base)
    for key, val in (override or {}).items():
        if isinstance(val, dict) and isinstance(out.get(key), dict):
            out[key] = deep_merge(out[key], val)
        else:
            out[key] = copy.deepcopy(val)
    return out


def check_keys(section: str, data: dict, allowed: set[str]) -> None:
    unknown = set(data) - allowed
    if unknown:
        raise InputError(f"Unknown entries in '{section}': {', '.join(sorted(unknown))}")


def parse_number(section: str, key: str, value, positive=True, integer=False):
    if value is None or (isinstance(value, float) and math.isnan(value)):
        raise InputError(f"'{section}.{key}' is required")
    try:
        v = int(value) if integer else float(value)
    except (TypeError, ValueError):
        raise InputError(f"'{section}.{key}' must be a number, got {value!r}") from None
    if integer and float(value) != v:
        raise InputError(f"'{section}.{key}' must be an integer, got {value!r}")
    if positive and v <= 0:
        raise InputError(f"'{section}.{key}' must be > 0, got {value!r}")
    return v


def parse_rayleigh(section: str, r: dict) -> tuple[float, float, float, float]:
    """Factors (mass, current, committed, initial stiffness) of a ``rayleigh`` settings entry."""
    keys = ("mass", "current_stiffness", "committed_stiffness", "initial_stiffness")
    check_keys(f"{section}.rayleigh", r, set(keys))
    return tuple(parse_number(f"{section}.rayleigh", k, r[k], positive=False) for k in keys)


# ----------------------------------------------------------------------------- system

@dataclass
class PipeProperties:
    outer_diameter: float
    inner_diameter: float
    elastic_modulus: float
    shear_modulus: float
    density: float
    fluid_density: float | None
    mass_factor: float

    @property
    def effective_fluid_density(self) -> float:
        return self.density / 7.8 if self.fluid_density is None else self.fluid_density


@dataclass
class Branch:
    x: float
    length: float
    n_pipes: int
    n_braces: int


@dataclass
class PipingSystem:
    """Plan geometry and structural definition of one loading direction.

    The main line lies along x and is loaded transversely (y). Branches are straight pipelines
    orthogonal to the main line, loaded along their axis, each lumped into one DOF.
    """

    name: str
    description: str
    length: float
    n_pipes: int
    pipe: PipeProperties
    hanger_first: float | None
    hanger_spacing: float | None
    hanger_end_clearance: float
    hanger_positions: list[float] | None
    brace_mask: list[int] | None
    brace_positions: list[float] | None
    brace_count: int | None
    branches: list[Branch]
    branch_participation: float
    trapezes: dict[str, Any] = field(default_factory=dict)   # kind -> "default" | path | Pinching4

    # ------------------------------------------------------------------ construction
    @classmethod
    def from_dict(cls, data: dict, base_dir: Path | None = None) -> "PipingSystem":
        data = deep_merge(read_yaml(DEFAULTS_DIR / "system.yaml"), data)
        check_keys("system", data, {"name", "description", "main_line", "pipe", "hangers", "braces",
                                     "branches", "branch_participation", "trapezes"})
        base_dir = Path(base_dir) if base_dir else Path.cwd()

        main = data.get("main_line") or {}
        check_keys("main_line", main, {"length", "n_pipes"})

        p = data["pipe"]
        check_keys("pipe", p, {"outer_diameter", "inner_diameter", "elastic_modulus", "shear_modulus",
                                "density", "fluid_density", "mass_factor"})
        pipe = PipeProperties(
            outer_diameter=parse_number("pipe", "outer_diameter", p["outer_diameter"]),
            inner_diameter=parse_number("pipe", "inner_diameter", p["inner_diameter"], positive=False),
            elastic_modulus=parse_number("pipe", "elastic_modulus", p["elastic_modulus"]),
            shear_modulus=parse_number("pipe", "shear_modulus", p["shear_modulus"]),
            density=parse_number("pipe", "density", p["density"]),
            fluid_density=None if p.get("fluid_density") is None
            else parse_number("pipe", "fluid_density", p["fluid_density"], positive=False),
            mass_factor=parse_number("pipe", "mass_factor", p["mass_factor"]),
        )

        h = data.get("hangers") or {}
        check_keys("hangers", h, {"first", "spacing", "end_clearance", "positions"})

        b = data.get("braces") or {}
        check_keys("braces", b, {"mask", "positions", "count"})
        given = [k for k in ("mask", "positions", "count") if b.get(k) is not None]
        if len(given) != 1:
            raise InputError("'braces' needs exactly one of: mask, positions, count")

        branches_raw = data.get("branches")
        if isinstance(branches_raw, str):
            path = Path(branches_raw)
            path = path if path.is_absolute() else base_dir / path
            branches_raw = read_branches_csv(path.read_text())
        branches = [_branch(i, br) for i, br in enumerate(branches_raw or [])]

        trapezes = {}
        tr = data.get("trapezes") or {}
        check_keys("trapezes", tr, {"transverse", "longitudinal"})
        for kind in ("transverse", "longitudinal"):
            src = tr.get(kind, "default")
            if isinstance(src, str) and src != "default":
                path = Path(src)
                src = str(path if path.is_absolute() else base_dir / path)
            trapezes[kind] = src

        return cls(
            name=str(data.get("name") or "unnamed"),
            description=str(data.get("description") or ""),
            length=parse_number("main_line", "length", main.get("length")),
            n_pipes=parse_number("main_line", "n_pipes", main.get("n_pipes"), integer=True),
            pipe=pipe,
            hanger_first=None if h.get("first") is None else parse_number("hangers", "first", h["first"]),
            hanger_spacing=None if h.get("spacing") is None else parse_number("hangers", "spacing", h["spacing"]),
            hanger_end_clearance=parse_number("hangers", "end_clearance", h.get("end_clearance"), positive=False),
            hanger_positions=None if h.get("positions") is None else [float(v) for v in h["positions"]],
            brace_mask=None if b.get("mask") is None else [int(v) for v in b["mask"]],
            brace_positions=None if b.get("positions") is None else [float(v) for v in b["positions"]],
            brace_count=None if b.get("count") is None else parse_number("braces", "count", b["count"],
                                                                 positive=False, integer=True),
            branches=branches,
            branch_participation=parse_number("system", "branch_participation", data.get("branch_participation")),
            trapezes=trapezes,
        )

    def to_dict(self) -> dict:
        """Plain-data representation (custom trapezes given as Pinching4 objects are written as 'custom')."""
        hangers: dict[str, Any] = {"end_clearance": self.hanger_end_clearance}
        if self.hanger_positions is not None:
            hangers["positions"] = list(self.hanger_positions)
        else:
            hangers.update(first=self.hanger_first, spacing=self.hanger_spacing)
        if self.brace_mask is not None:
            braces = {"mask": list(self.brace_mask)}
        elif self.brace_positions is not None:
            braces = {"positions": list(self.brace_positions)}
        else:
            braces = {"count": self.brace_count}
        trapezes = {k: (f"custom_{k}.csv" if isinstance(v, Pinching4) else str(v))
                    for k, v in self.trapezes.items()}
        return {
            "name": self.name,
            "description": self.description,
            "main_line": {"length": self.length, "n_pipes": self.n_pipes},
            "pipe": dict(vars(self.pipe)),
            "hangers": hangers,
            "braces": braces,
            "branches": [dict(vars(br)) for br in self.branches],
            "branch_participation": self.branch_participation,
            "trapezes": trapezes,
        }

    def to_yaml(self) -> str:
        return dump_yaml(self.to_dict())

    # ------------------------------------------------------------------ resolution
    def hanger_x(self) -> np.ndarray:
        if self.hanger_positions is not None:
            x = np.round(np.array(self.hanger_positions, dtype=float), COORD_DECIMALS)
            if len(x) == 0:
                raise InputError("At least one hanger is required")
            if np.any(np.diff(x) <= 0):
                raise InputError("Hanger positions must be strictly increasing")
            if x[0] <= 0 or x[-1] >= self.length:
                raise InputError("Hanger positions must lie strictly inside the main line (0 < x < length)")
            return x
        if self.hanger_first is None or self.hanger_spacing is None:
            raise InputError("'hangers' needs either 'positions' or both 'first' and 'spacing'")
        L, x0, s, c = self.length, self.hanger_first, self.hanger_spacing, self.hanger_end_clearance
        if x0 > L - c:
            raise InputError(f"First hanger at {x0:g} must be at least {c:g} mm from the main-line end")
        n_max = int((L - c - x0) // s)
        x = [x0 + i * s for i in range(n_max + 1) if x0 + i * s <= L - c + 1e-6]
        return np.round(np.array(x, dtype=float), COORD_DECIMALS)

    def brace_mask_array(self, hanger_x: np.ndarray) -> np.ndarray:
        n = len(hanger_x)
        if self.brace_mask is not None:
            mask = np.array(self.brace_mask, dtype=int)
            if len(mask) != n:
                raise InputError(f"Brace mask has {len(mask)} entries but there are {n} hangers")
            if not np.all((mask == 0) | (mask == 1)):
                raise InputError("Brace mask must contain only 0 and 1")
            return mask
        if self.brace_positions is not None:
            mask = np.zeros(n, dtype=int)
            for xb in self.brace_positions:
                hit = np.where(np.abs(hanger_x - xb) < 1e-6)[0]
                if len(hit) == 0:
                    raise InputError(f"Brace at x={xb:g} is not at a hanger location")
                mask[hit[0]] = 1
            return mask
        return evenly_spaced_brace_mask(hanger_x, self.length, self.brace_count)

    def resolve(self) -> "ResolvedSystem":
        hx = self.hanger_x()
        if len(hx) > MAX_HANGERS:
            raise InputError(f"At most {MAX_HANGERS} hangers are supported, got {len(hx)}")
        mask = self.brace_mask_array(hx)
        if not self.branches:
            raise InputError("At least one branch is required (the procedure is defined for main line + branches)")
        if len(self.branches) > MAX_BRANCHES:
            raise InputError(f"At most {MAX_BRANCHES} branches are supported")
        bx = np.round(np.array([br.x for br in self.branches], dtype=float), COORD_DECIMALS)
        if np.any(bx < 0) or np.any(bx > self.length):
            raise InputError("Branch positions must lie on the main line (0 <= x <= length)")
        braced_x = hx[mask == 1]
        for i, xo in enumerate(bx):
            if np.any(np.abs(braced_x - xo) < BRANCH_BRACE_CLASH_TOL):
                raise InputError(f"Branch {i + 1} at x={xo:g} coincides with a braced hanger (not allowed)")
        if self.pipe.inner_diameter >= self.pipe.outer_diameter:
            raise InputError("Pipe inner diameter must be smaller than the outer diameter")

        t = load_trapeze(self.trapezes.get("transverse"), "transverse")
        l = load_trapeze(self.trapezes.get("longitudinal"), "longitudinal")
        return ResolvedSystem(
            name=self.name,
            length=float(self.length),
            n_pipes=self.n_pipes,
            pipe=self.pipe,
            hanger_x=hx,
            brace_mask=mask,
            branch_x=bx,
            branch_length=np.array([br.length for br in self.branches], dtype=float),
            branch_n_pipes=np.array([br.n_pipes for br in self.branches], dtype=int),
            branch_n_braces=np.array([br.n_braces for br in self.branches], dtype=int),
            branch_participation=self.branch_participation,
            transverse=t,
            longitudinal=l,
            transverse_trilinear=trilinear_from_pinching4(t),
            longitudinal_trilinear=trilinear_from_pinching4(l),
        )


def _branch(i: int, br: dict) -> Branch:
    if not isinstance(br, dict):
        raise InputError(f"Branch {i + 1} must be a mapping with x, length, n_pipes, n_braces")
    check_keys(f"branches[{i + 1}]", br, {"x", "length", "n_pipes", "n_braces"})
    s = f"branches[{i + 1}]"
    return Branch(
        x=parse_number(s, "x", br.get("x"), positive=False),
        length=parse_number(s, "length", br.get("length")),
        n_pipes=parse_number(s, "n_pipes", br.get("n_pipes"), integer=True),
        n_braces=parse_number(s, "n_braces", br.get("n_braces"), integer=True),
    )


def read_branches_csv(text: str) -> list[dict]:
    rows = list(csv.DictReader(io.StringIO(text)))
    need = {"x", "length", "n_pipes", "n_braces"}
    if rows and not need <= set(rows[0]):
        raise InputError(f"Branch file needs columns: {', '.join(sorted(need))}")
    return [{k: r[k] for k in need} for r in rows]


def evenly_spaced_brace_mask(hanger_x: np.ndarray, length: float, count: int) -> np.ndarray:
    """Place ``count`` braces at length/count spacing starting at half a spacing, each snapped to the
    nearest hanger not already used (``compute_stiff_mask`` of the original code)."""
    n = len(hanger_x)
    if count > n:
        raise InputError(f"Cannot place {count} braces on {n} hangers")
    mask = np.zeros(n, dtype=int)
    if count == 0:
        return mask
    spacing = length / count
    used: set[int] = set()
    for x in spacing / 2.0 + spacing * np.arange(count):
        for idx in np.argsort(np.abs(hanger_x - x)):
            if idx not in used:
                used.add(int(idx))
                break
    mask[sorted(used)] = 1
    return mask


@dataclass
class ResolvedSystem:
    """Validated, array-based system ready for analysis."""

    name: str
    length: float
    n_pipes: int
    pipe: PipeProperties
    hanger_x: np.ndarray
    brace_mask: np.ndarray
    branch_x: np.ndarray
    branch_length: np.ndarray
    branch_n_pipes: np.ndarray
    branch_n_braces: np.ndarray
    branch_participation: float
    transverse: Pinching4
    longitudinal: Pinching4
    transverse_trilinear: Trilinear
    longitudinal_trilinear: Trilinear

    @property
    def n_hangers(self) -> int:
        return len(self.hanger_x)

    @property
    def n_branches(self) -> int:
        return len(self.branch_x)

    @property
    def n_dof(self) -> int:
        return self.n_hangers + self.n_branches

    def dof_table(self) -> list[dict]:
        """One row per DOF, in DOF order: all hangers by position, then branches in input order."""
        rows = [{"dof": i, "kind": "hanger", "x": float(x), "braced": bool(self.brace_mask[i]), "branch": None}
                for i, x in enumerate(self.hanger_x)]
        rows += [{"dof": self.n_hangers + j, "kind": "branch", "x": float(x), "braced": True, "branch": j}
                 for j, x in enumerate(self.branch_x)]
        return rows


def load_system(path: str | Path) -> PipingSystem:
    path = Path(path)
    return PipingSystem.from_dict(read_yaml(path), base_dir=path.parent)


# ----------------------------------------------------------------------------- settings

@dataclass
class AnalysisSettings:
    delta_c_start: float
    delta_c_stop: float
    n_steps: int
    delta_c_values: list[float] | None
    warm_start: bool
    max_iterations: int
    tolerance: float
    solver_test: str
    solver_tolerance: float
    solver_max_iterations: int
    sdof_delta_c: float
    motions: dict = field(default_factory=dict)              # default floor-motion selection
    sdof_time_history: dict = field(default_factory=dict)    # parsed by timehistory.TimeHistorySettings
    verification_3d: dict = field(default_factory=dict)      # parsed by verification3d.Verification3DSettings

    @classmethod
    def from_dict(cls, data: dict | None = None) -> "AnalysisSettings":
        d = deep_merge(read_yaml(DEFAULTS_DIR / "settings.yaml"), data or {})
        check_keys("settings", d, {"pushover", "shape_iteration", "static_solver", "sdof", "motions",
                                    "sdof_time_history", "verification_3d"})
        po, it, so, sd = d["pushover"], d["shape_iteration"], d["static_solver"], d["sdof"]
        check_keys("pushover", po, {"delta_c_start", "delta_c_stop", "n_steps", "delta_c_values", "warm_start"})
        check_keys("shape_iteration", it, {"max_iterations", "tolerance"})
        check_keys("static_solver", so, {"test", "tolerance", "max_iterations"})
        check_keys("sdof", sd, {"delta_c"})
        values = po.get("delta_c_values")
        if values is not None:
            values = [parse_number("pushover", "delta_c_values", v) for v in values]
            if not values:
                raise InputError("'pushover.delta_c_values' must not be empty")
        s = cls(
            delta_c_start=parse_number("pushover", "delta_c_start", po["delta_c_start"]),
            delta_c_stop=parse_number("pushover", "delta_c_stop", po["delta_c_stop"]),
            n_steps=parse_number("pushover", "n_steps", po["n_steps"], integer=True),
            delta_c_values=values,
            warm_start=bool(po["warm_start"]),
            max_iterations=parse_number("shape_iteration", "max_iterations", it["max_iterations"], integer=True),
            tolerance=parse_number("shape_iteration", "tolerance", it["tolerance"]),
            solver_test=str(so["test"]),
            solver_tolerance=parse_number("static_solver", "tolerance", so["tolerance"]),
            solver_max_iterations=parse_number("static_solver", "max_iterations", so["max_iterations"], integer=True),
            sdof_delta_c=parse_number("sdof", "delta_c", sd["delta_c"]),
            motions=d.get("motions") or {},
            sdof_time_history=d.get("sdof_time_history") or {},
            verification_3d=d.get("verification_3d") or {},
        )
        if values is None and s.delta_c_stop < s.delta_c_start:
            raise InputError("'pushover.delta_c_stop' must be >= 'delta_c_start'")
        return s

    def delta_c(self) -> np.ndarray:
        if self.delta_c_values is not None:
            return np.array(self.delta_c_values, dtype=float)
        return np.linspace(self.delta_c_start, self.delta_c_stop, self.n_steps)

    def to_dict(self) -> dict:
        return {
            "pushover": {"delta_c_start": self.delta_c_start, "delta_c_stop": self.delta_c_stop,
                         "n_steps": self.n_steps, "delta_c_values": self.delta_c_values,
                         "warm_start": self.warm_start},
            "shape_iteration": {"max_iterations": self.max_iterations, "tolerance": self.tolerance},
            "static_solver": {"test": self.solver_test, "tolerance": self.solver_tolerance,
                              "max_iterations": self.solver_max_iterations},
            "sdof": {"delta_c": self.sdof_delta_c},
            "motions": self.motions,
            "sdof_time_history": self.sdof_time_history,
            "verification_3d": self.verification_3d,
        }

    def to_yaml(self) -> str:
        return dump_yaml(self.to_dict())


def load_settings(path: str | Path | None = None) -> AnalysisSettings:
    return AnalysisSettings.from_dict(read_yaml(Path(path)) if path else {})


def dump_yaml(data: dict) -> str:
    return yaml.safe_dump(_plain(data), sort_keys=False, default_flow_style=None, width=100)


def _plain(obj):
    """Convert numpy scalars/arrays and floats that are integers into YAML-friendly values."""
    if isinstance(obj, dict):
        return {k: _plain(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple, np.ndarray)):
        return [_plain(v) for v in obj]
    if isinstance(obj, np.integer):
        return int(obj)
    if isinstance(obj, (float, np.floating)):
        f = float(obj)
        return int(f) if f.is_integer() and abs(f) < 1e15 else f
    return obj
