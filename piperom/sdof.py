"""Equivalent SDOF parameters at a chosen target displacement Delta_c.

This replaces the values typed by hand into ``code implementation for paper/Pushover_SDOF/*.py`` and reproduces the
``equivalent_static.py`` -> ``NLTHA_SDOF.py`` chain of ``code_proposed_procedure/``:

* the equivalent static procedure is run at Delta_c;
* Gamma and the effective mass come from the converged shape;
* each braced hanger (transverse) and each branch (longitudinal) is one support, with
  phi = displaced shape at the support, normalised to the reference (last) branch DOF;
* each support becomes a Pinching4 spring of the SDOF with envelope deformations divided by
  Gamma * phi and envelope forces multiplied by the number of trapezes it represents
  (1 for a braced hanger, ``n_braces`` for a branch).

The SDOF itself (mass = effective mass, parallel springs) is not analysed here.
"""

from __future__ import annotations

import csv
import io
from dataclasses import dataclass
from pathlib import Path

import numpy as np

from .inputs import AnalysisSettings, PipingSystem, ResolvedSystem, dump_yaml
from .pushover import PushoverStep, run_step
from .trapeze import Pinching4


@dataclass
class SDOFSupport:
    kind: str           # "transverse" (braced hanger) or "longitudinal" (branch)
    dof: int
    x: float
    branch: int | None
    phi: float
    n_trapezes: int
    spring: Pinching4   # scaled Pinching4 of the SDOF spring


@dataclass
class SDOFParameters:
    name: str
    delta_c: float
    gamma: float
    effective_mass: float
    total_mass: float
    mass_ratio: float
    u_sdof: float
    base_shear: float
    converged: bool
    iterations: int
    supports: list[SDOFSupport]
    d_norm: np.ndarray

    @property
    def n_transverse(self) -> int:
        return sum(s.kind == "transverse" for s in self.supports)

    @property
    def n_longitudinal_trapezes(self) -> int:
        return sum(s.n_trapezes for s in self.supports if s.kind == "longitudinal")

    @property
    def support_shape(self) -> np.ndarray:
        """phi at transverse supports then branches (``DispShape`` of the original SDOF scripts)."""
        return np.array([s.phi for s in self.supports])

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "delta_c": self.delta_c,
            "gamma": self.gamma,
            "effective_mass": self.effective_mass,
            "total_mass": self.total_mass,
            "mass_ratio": self.mass_ratio,
            "u_sdof": self.u_sdof,
            "base_shear": self.base_shear,
            "converged": self.converged,
            "iterations": self.iterations,
            "n_transverse_supports": self.n_transverse,
            "n_longitudinal_trapezes": self.n_longitudinal_trapezes,
            "supports": [
                {"kind": s.kind, "dof": s.dof, "x": s.x, "branch": s.branch, "phi": float(s.phi),
                 "n_trapezes": s.n_trapezes, "pinching4": s.spring.parameters()}
                for s in self.supports
            ],
        }

    def to_yaml(self) -> str:
        return dump_yaml(self.to_dict())

    def springs_csv(self) -> str:
        """One row per SDOF spring with its scaled envelope (forces in N, deformations in mm of SDOF)."""
        buf = io.StringIO()
        cols = (["support", "kind", "x", "branch", "phi", "n_trapezes"]
                + [f"ePf{i}" for i in range(1, 5)] + [f"ePd{i}" for i in range(1, 5)]
                + [f"eNf{i}" for i in range(1, 5)] + [f"eNd{i}" for i in range(1, 5)])
        w = csv.writer(buf, lineterminator="\n")
        w.writerow(cols)
        for k, s in enumerate(self.supports):
            p = s.spring.parameters()
            w.writerow([k, s.kind, repr(s.x), "" if s.branch is None else s.branch, repr(float(s.phi)),
                        s.n_trapezes] + [repr(float(p[c])) for c in cols[6:]])
        return buf.getvalue()

    def write(self, out_dir: str | Path) -> list[Path]:
        out = Path(out_dir)
        out.mkdir(parents=True, exist_ok=True)
        files = [out / "sdof_parameters.yaml", out / "sdof_springs.csv"]
        files[0].write_text(self.to_yaml())
        files[1].write_text(self.springs_csv())
        return files


def sdof_from_step(rs: ResolvedSystem, step: PushoverStep, converged: bool | None = None,
                   iterations: int | None = None) -> SDOFParameters:
    gamma = step.gamma
    supports: list[SDOFSupport] = []
    for i in np.where(rs.brace_mask == 1)[0]:
        phi = float(step.d_norm[i])
        supports.append(SDOFSupport("transverse", int(i), float(rs.hanger_x[i]), None, phi, 1,
                                    rs.transverse.scaled(1.0, 1.0 / (gamma * phi))))
    for j in range(rs.n_branches):
        i = rs.n_hangers + j
        phi = float(step.d_norm[i])
        n = int(rs.branch_n_braces[j])
        supports.append(SDOFSupport("longitudinal", i, float(rs.branch_x[j]), j, phi, n,
                                    rs.longitudinal.scaled(float(n), 1.0 / (gamma * phi))))
    return SDOFParameters(
        name=rs.name, delta_c=step.delta_c, gamma=gamma, effective_mass=step.effective_mass,
        total_mass=step.total_mass, mass_ratio=step.mass_ratio, u_sdof=step.u_sdof, base_shear=step.base_shear,
        converged=step.converged if converged is None else converged,
        iterations=step.iterations if iterations is None else iterations,
        supports=supports, d_norm=step.d_norm,
    )


def derive_sdof(system: PipingSystem | ResolvedSystem, settings: AnalysisSettings,
                delta_c: float | None = None) -> SDOFParameters:
    """Run the equivalent static procedure at ``delta_c`` (default: ``settings.sdof_delta_c``)."""
    rs = system.resolve() if isinstance(system, PipingSystem) else system
    dc = settings.sdof_delta_c if delta_c is None else float(delta_c)
    step, _ = run_step(rs, settings, dc)
    return sdof_from_step(rs, step)
