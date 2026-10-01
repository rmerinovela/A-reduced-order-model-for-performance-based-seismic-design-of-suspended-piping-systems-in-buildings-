"""Adaptive pseudo-pushover: the equivalent static procedure repeated over increasing Delta_c.

At each target displacement Delta_c the displaced shape is iterated to convergence; the step gives one
point of the capacity curve (base shear vs equivalent SDOF displacement) and the adaptive shape.
"""

from __future__ import annotations

import csv
import io
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable

import numpy as np

from .inputs import AnalysisSettings, PipingSystem, ResolvedSystem
from .static_model import ShapeResult, SolverSettings, iterate_shape

CURVE_COLUMNS = ["step", "delta_c", "gamma", "effective_mass", "base_shear", "mass_ratio", "u_sdof",
                 "iterations", "converged", "final_change"]
SHAPE_COLUMNS = ["step", "delta_c", "dof", "kind", "x", "braced", "branch",
                 "d_norm", "d_scaled", "f_push", "load"]


@dataclass
class PushoverStep:
    delta_c: float
    gamma: float
    effective_mass: float
    total_mass: float
    base_shear: float
    mass_ratio: float
    u_sdof: float
    d_norm: np.ndarray      # shape normalised to the reference (last) DOF
    d_scaled: np.ndarray    # delta_c * shape normalised to max |d| = 1
    f_push: np.ndarray
    loads: np.ndarray
    iterations: int
    converged: bool
    final_change: float

    @classmethod
    def from_shape(cls, delta_c: float, res: ShapeResult) -> "PushoverStep":
        d_scaled = delta_c * res.d_star
        d_norm = d_scaled / d_scaled[-1]
        s = res.step
        return cls(
            delta_c=float(delta_c), gamma=float(s.gamma), effective_mass=float(s.effective_mass), total_mass=float(s.total_mass),
            base_shear=float(s.base_shear), mass_ratio=float(s.mass_ratio),
            u_sdof=float(delta_c / (s.gamma * np.max(d_norm))),
            d_norm=d_norm, d_scaled=d_scaled, f_push=s.f_push, loads=s.loads,
            iterations=res.iterations, converged=res.converged,
            final_change=res.history[-1] if res.history else float("nan"),
        )


@dataclass
class PushoverResult:
    name: str
    dofs: list[dict]
    steps: list[PushoverStep] = field(default_factory=list)

    @property
    def n_not_converged(self) -> int:
        return sum(not s.converged for s in self.steps)

    def curve_rows(self) -> list[dict]:
        return [{"step": k, "delta_c": s.delta_c, "gamma": s.gamma, "effective_mass": s.effective_mass,
                 "base_shear": s.base_shear, "mass_ratio": s.mass_ratio, "u_sdof": s.u_sdof,
                 "iterations": s.iterations, "converged": s.converged, "final_change": s.final_change}
                for k, s in enumerate(self.steps)]

    def shape_rows(self) -> list[dict]:
        rows = []
        for k, s in enumerate(self.steps):
            for dof in self.dofs:
                i = dof["dof"]
                rows.append({"step": k, "delta_c": s.delta_c, "dof": i, "kind": dof["kind"], "x": dof["x"],
                             "braced": dof["braced"], "branch": "" if dof["branch"] is None else dof["branch"],
                             "d_norm": s.d_norm[i], "d_scaled": s.d_scaled[i], "f_push": s.f_push[i],
                             "load": s.loads[i]})
        return rows

    def write(self, out_dir: str | Path, system: PipingSystem | None = None,
              settings: AnalysisSettings | None = None) -> list[Path]:
        out = Path(out_dir)
        out.mkdir(parents=True, exist_ok=True)
        files = [out / "pushover_curve.csv", out / "pushover_shapes.csv"]
        files[0].write_text(rows_to_csv(self.curve_rows(), CURVE_COLUMNS))
        files[1].write_text(rows_to_csv(self.shape_rows(), SHAPE_COLUMNS))
        if system is not None:
            files.append(out / "system.yaml")
            files[-1].write_text(system.to_yaml())
        if settings is not None:
            files.append(out / "settings.yaml")
            files[-1].write_text(settings.to_yaml())
        return files


def rows_to_csv(rows: list[dict], columns: list[str]) -> str:
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=columns, lineterminator="\n")
    w.writeheader()
    for r in rows:
        w.writerow({k: (repr(float(v)) if isinstance(v, (float, np.floating)) else v) for k, v in r.items()})
    return buf.getvalue()


def solver_settings(settings: AnalysisSettings) -> SolverSettings:
    return SolverSettings(settings.solver_test, settings.solver_tolerance, settings.solver_max_iterations)


def run_step(rs: ResolvedSystem, settings: AnalysisSettings, delta_c: float,
             d_init: np.ndarray | None = None) -> tuple[PushoverStep, ShapeResult]:
    d0 = np.ones(rs.n_dof) if d_init is None else d_init
    res = iterate_shape(rs, d0, delta_c, settings.max_iterations, settings.tolerance, solver_settings(settings))
    return PushoverStep.from_shape(delta_c, res), res


def run_pushover(system: PipingSystem | ResolvedSystem, settings: AnalysisSettings,
                 progress: Callable[[int, int, PushoverStep], None] | None = None) -> PushoverResult:
    rs = system.resolve() if isinstance(system, PipingSystem) else system
    result = PushoverResult(name=rs.name, dofs=rs.dof_table())
    d_prev = None
    deltas = settings.delta_c()
    for k, dc in enumerate(deltas):
        step, res = run_step(rs, settings, float(dc), d_prev if settings.warm_start else None)
        d_prev = res.d_star
        result.steps.append(step)
        if progress:
            progress(k + 1, len(deltas), step)
    return result

