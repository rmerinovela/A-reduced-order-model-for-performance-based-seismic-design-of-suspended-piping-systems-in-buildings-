"""Nonlinear time-history analysis of the equivalent SDOF under a floor acceleration history.

Port of ``code implementation for paper/code_proposed_procedure/NLTHA_SDOF.py``: one zeroLength element
with the parallel Pinching4 springs of the supports, mass = effective mass, Rayleigh damping on the
current stiffness (2%), Newmark average acceleration, and the same solution fallbacks.
"""

from __future__ import annotations

import math
import os
import tempfile
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np
import openseespy.opensees as op

from .inputs import check_keys, deep_merge, parse_number, parse_rayleigh, read_yaml
from . import DEFAULTS_DIR
from .motions import FloorMotion
from .trapeze import Pinching4

G_MM_S2 = 9805.0
RIGID = 10e12


@dataclass
class SDOFModel:
    """What the time-history analysis needs: mass and the springs acting in parallel."""

    name: str
    mass: float
    springs: list[Pinching4]
    gamma: float | None = None
    support_phi: list[float] = field(default_factory=list)      # same order as springs
    support_labels: list[str] = field(default_factory=list)

    @classmethod
    def from_parameters(cls, p) -> "SDOFModel":
        """Longitudinal springs first, then transverse (order of NLTHA_SDOF.py)."""
        sup = [s for s in p.supports if s.kind == "longitudinal"] + [s for s in p.supports if s.kind == "transverse"]
        labels = [f"{s.kind} x={s.x:g}" + ("" if s.branch is None else f" (branch {s.branch + 1})") for s in sup]
        return cls(name=p.name, mass=p.effective_mass, springs=[s.spring for s in sup], gamma=p.gamma,
                   support_phi=[s.phi for s in sup], support_labels=labels)


@dataclass
class TimeHistorySettings:
    damping_ratio: float
    mass_proportional: float
    current_stiffness: float
    committed_stiffness: float
    initial_stiffness: float
    test: str
    tolerance: float
    max_iterations: int
    fallback_tolerance: float
    fallback_max_iterations: int

    @classmethod
    def from_dict(cls, data: dict | None = None) -> "TimeHistorySettings":
        d = deep_merge(read_yaml(DEFAULTS_DIR / "settings.yaml").get("sdof_time_history", {}), data or {})
        check_keys("sdof_time_history", d, {"damping_ratio", "rayleigh", "test", "tolerance", "max_iterations",
                                             "fallback_tolerance", "fallback_max_iterations"})
        s = "sdof_time_history"
        mass, current, committed, initial = parse_rayleigh(s, d["rayleigh"])
        return cls(
            damping_ratio=parse_number(s, "damping_ratio", d["damping_ratio"], positive=False),
            mass_proportional=mass, current_stiffness=current, committed_stiffness=committed,
            initial_stiffness=initial,
            test=str(d["test"]), tolerance=parse_number(s, "tolerance", d["tolerance"]),
            max_iterations=parse_number(s, "max_iterations", d["max_iterations"], integer=True),
            fallback_tolerance=parse_number(s, "fallback_tolerance", d["fallback_tolerance"]),
            fallback_max_iterations=parse_number(s, "fallback_max_iterations", d["fallback_max_iterations"], integer=True),
        )

    def to_dict(self) -> dict:
        return {"damping_ratio": self.damping_ratio,
                "rayleigh": {"mass": self.mass_proportional, "current_stiffness": self.current_stiffness,
                             "committed_stiffness": self.committed_stiffness,
                             "initial_stiffness": self.initial_stiffness},
                "test": self.test, "tolerance": self.tolerance, "max_iterations": self.max_iterations,
                "fallback_tolerance": self.fallback_tolerance,
                "fallback_max_iterations": self.fallback_max_iterations}


@dataclass
class SDOFResponse:
    motion: str
    record: str
    level: int | None
    period: float
    time: np.ndarray
    u: np.ndarray               # SDOF displacement relative to the floor (mm)
    force: np.ndarray           # spring force (N)
    completed: bool
    end_time: float
    duration: float
    peak_u: float = float("nan")   # peak |u| (kept when the histories are dropped)

    def __post_init__(self):
        if len(self.u):
            self.peak_u = float(np.max(np.abs(self.u)))


def _build(model: SDOFModel) -> None:
    op.wipe()
    op.logFile(os.devnull, "-noEcho")
    op.model("basic", "-ndm", 2, "-ndf", 3)
    op.node(1, 0.0, 0.0)
    op.node(2, 0.0, 0.0, "-mass", model.mass, model.mass, 0)
    op.fix(1, 1, 1, 1)
    tags = []
    for k, spring in enumerate(model.springs):
        tag = 10 + k
        op.uniaxialMaterial("Pinching4", tag, *spring.opensees_args())
        tags.append(tag)
    op.uniaxialMaterial("Parallel", 1000, *tags)
    op.uniaxialMaterial("Elastic", 4, RIGID)
    op.element("zeroLength", 1, 1, 2, "-mat", 1000, 4, 4, "-dir", 1, 2, 3)


def _gravity(model: SDOFModel) -> None:
    op.timeSeries("Constant", 1)
    op.pattern("Plain", 1, 1)
    op.load(2, 0, model.mass * G_MM_S2, 0)
    op.constraints("Transformation")
    op.numberer("RCM")
    op.system("BandGeneral")
    op.test("NormDispIncr", 1.0e-8, 200)
    op.algorithm("Newton")
    op.integrator("LoadControl", 0.1)
    op.analysis("Static")
    op.analyze(10)
    op.loadConst("-time", 0.0)


def sdof_period(model: SDOFModel) -> float:
    _build(model)
    _gravity(model)
    return 2 * math.pi / math.sqrt(op.eigen(1)[0])


def run_sdof_time_history(model: SDOFModel, motion: FloorMotion, s: TimeHistorySettings) -> SDOFResponse:
    _build(model)
    _gravity(model)
    omega = math.sqrt(op.eigen(1)[0])
    xi = s.damping_ratio
    op.rayleigh(s.mass_proportional * xi * (2 * omega), s.current_stiffness * 2 * xi / omega,
                s.initial_stiffness * 2 * xi / omega, s.committed_stiffness * 2 * xi / omega)

    dt, npts = motion.dt, len(motion.acc)
    t_max = dt * npts
    op.timeSeries("Path", 1000, "-dt", dt, "-values", *motion.acc, "-factor", 1, "-prependZero")

    with tempfile.TemporaryDirectory() as tmp:
        f_u, f_f = Path(tmp) / "u.out", Path(tmp) / "f.out"
        op.recorder("Node", "-file", str(f_u), "-time", "-node", 2, "-dof", 1, "disp")
        op.recorder("Element", "-file", str(f_f), "-ele", 1, "force")
        op.pattern("UniformExcitation", 100, 1, "-accel", 1000)

        op.wipeAnalysis()
        op.integrator("Newmark", 0.5, 0.25)
        op.numberer("RCM")
        op.system("BandGeneral")
        op.constraints("Plain")
        op.test(s.test, s.tolerance, s.max_iterations)
        op.algorithm("Newton")
        op.analysis("Transient")

        ok = op.analyze(npts, dt)
        if ok != 0:
            ok = 0
            control_time = op.getTime()
            while control_time < t_max and ok == 0:
                control_time = op.getTime()
                ok = op.analyze(1, dt)
                if ok != 0:
                    op.test(s.test, s.fallback_tolerance, s.fallback_max_iterations, 0)
                    op.algorithm("Newton", "-initial")
                    ok = op.analyze(1, dt)
                    op.test(s.test, s.tolerance, s.max_iterations)
                    op.algorithm("Newton")
                if ok != 0:
                    op.test(s.test, s.fallback_tolerance, s.fallback_max_iterations, 0)
                    op.algorithm("Broyden", 8)
                    ok = op.analyze(1, dt)
                    op.algorithm("Newton")
                if ok != 0:
                    op.algorithm("NewtonLineSearch", 0.8)
                    ok = op.analyze(1, dt)
                    op.algorithm("Newton")
                if ok != 0:
                    op.algorithm("KrylovNewton")
                    ok = op.analyze(1, dt)
                    op.algorithm("Newton")
        end_time = op.getTime()
        op.wipe()
        u = np.loadtxt(f_u, ndmin=2)
        frc = np.loadtxt(f_f, ndmin=2)

    n = min(len(u), len(frc))
    return SDOFResponse(
        motion=motion.set_name, record=motion.record, level=motion.level, period=2 * math.pi / omega,
        time=u[:n, 0], u=u[:n, 1], force=-frc[:n, 0] if frc.size else np.zeros(n),
        completed=end_time >= t_max - 0.5 * dt, end_time=end_time, duration=t_max,
    )


def support_demands(model: SDOFModel, peak_u: float) -> list[dict]:
    """Peak support displacement Gamma * phi * u_SDOF and its ratio to the trapeze envelope points."""
    if model.gamma is None:
        return []
    rows = []
    for label, phi, spring in zip(model.support_labels, model.support_phi, model.springs):
        d = model.gamma * phi * peak_u
        base = [v * model.gamma * phi for v in spring.pos_disp]      # unscaled trapeze deformations
        rows.append({"support": label, "phi": phi, "peak_displacement": d,
                     **{f"ratio_to_ePd{i + 1}": d / base[i] for i in range(4)}})
    return rows

