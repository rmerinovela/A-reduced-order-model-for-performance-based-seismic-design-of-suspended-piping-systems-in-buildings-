"""Verification with the full 3D models of the paper (``inputs/models3d/<name>.json``).

The model files hold the OpenSees commands of the paper's 3D models, unchanged (converted by
``validation/convert_3d_models.py``). The analysis follows ``3D_models/*.py``: gravity, Rayleigh damping
on modes 1-2 (mass + last-committed stiffness), bidirectional floor motions (x and y components applied
together), Newmark average acceleration and the same fallback sequence.
"""

from __future__ import annotations

import json
import math
import os
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

import numpy as np
import openseespy.opensees as op

from . import DEFAULTS_DIR, INPUTS_DIR
from .inputs import InputError, check_keys, deep_merge, parse_number, parse_rayleigh, read_yaml
from .motions import FloorMotion

MODELS3D_DIR = INPUTS_DIR / "models3d"


@dataclass
class Model3D:
    name: str
    description: str
    commands: list
    node_groups: dict[str, list[int]]
    rom_systems: dict[str, str]

    def node_coords(self) -> dict[int, tuple[float, float, float]]:
        return {int(a[0]): tuple(float(v) for v in a[1:4]) for c, a in self.commands if c == "node"}


def list_models3d() -> list[str]:
    return sorted(p.stem for p in MODELS3D_DIR.glob("*.json"))


def load_model3d(name: str) -> Model3D:
    path = MODELS3D_DIR / f"{name}.json"
    if not path.exists():
        raise InputError(f"No 3D model '{name}' in inputs/models3d/ (available: {', '.join(list_models3d())})")
    d = json.loads(path.read_text())
    return Model3D(d["name"], d.get("description", ""), d["commands"], d["node_groups"], d.get("rom_systems", {}))


def model3d_for_system(system_name: str) -> str | None:
    for name in list_models3d():
        if system_name in load_model3d(name).rom_systems.values():
            return name
    return None


@dataclass
class Verification3DSettings:
    gravity_steps: int
    damping_ratio: float
    rayleigh_modes: tuple[int, int]
    mass_proportional: float
    current_stiffness: float
    committed_stiffness: float
    initial_stiffness: float
    test: str
    tolerance: float
    max_iterations: int
    fallback_test: str
    fallback_tolerance: float
    fallback_max_iterations: int

    @classmethod
    def from_dict(cls, data: dict | None = None) -> "Verification3DSettings":
        d = deep_merge(read_yaml(DEFAULTS_DIR / "settings.yaml").get("verification_3d", {}), data or {})
        s = "verification_3d"
        check_keys(s, d, {"gravity_steps", "damping_ratio", "rayleigh_modes", "rayleigh", "test", "tolerance",
                           "max_iterations", "fallback_test", "fallback_tolerance", "fallback_max_iterations"})
        mass, current, committed, initial = parse_rayleigh(s, d["rayleigh"])
        modes = tuple(int(v) for v in d["rayleigh_modes"])
        if len(modes) != 2 or min(modes) < 1:
            raise InputError("'verification_3d.rayleigh_modes' must be two mode numbers, e.g. [1, 2]")
        return cls(
            gravity_steps=parse_number(s, "gravity_steps", d["gravity_steps"], integer=True),
            damping_ratio=parse_number(s, "damping_ratio", d["damping_ratio"], positive=False),
            rayleigh_modes=modes,
            mass_proportional=mass, current_stiffness=current, committed_stiffness=committed,
            initial_stiffness=initial,
            test=str(d["test"]), tolerance=parse_number(s, "tolerance", d["tolerance"]),
            max_iterations=parse_number(s, "max_iterations", d["max_iterations"], integer=True),
            fallback_test=str(d["fallback_test"]),
            fallback_tolerance=parse_number(s, "fallback_tolerance", d["fallback_tolerance"]),
            fallback_max_iterations=parse_number(s, "fallback_max_iterations", d["fallback_max_iterations"], integer=True),
        )


@dataclass
class Response3D:
    model: str
    record_x: str
    record_y: str
    level: int | None
    periods: list[float]
    time: np.ndarray
    nodes_x: list[int]
    nodes_y: list[int]
    ux: np.ndarray            # (n_time, n_nodes_x) displacement in x relative to the floor (mm)
    uy: np.ndarray            # (n_time, n_nodes_y)
    completed: bool
    end_time: float
    duration: float

    @property
    def peak_x(self) -> np.ndarray:
        return np.max(np.abs(self.ux), axis=0) if self.ux.size else np.full(len(self.nodes_x), np.nan)

    @property
    def peak_y(self) -> np.ndarray:
        return np.max(np.abs(self.uy), axis=0) if self.uy.size else np.full(len(self.nodes_y), np.nan)


def build_model3d(model: Model3D) -> None:
    op.wipe()
    op.logFile(os.devnull, "-noEcho")
    for cmd, args in model.commands:
        if cmd == "wipe":
            continue
        getattr(op, cmd)(*args)


def run_3d(model: Model3D, motion_x: FloorMotion, motion_y: FloorMotion, s: Verification3DSettings,
           progress: Callable[[float], None] | None = None, chunk: int = 500) -> Response3D:
    if abs(motion_x.dt - motion_y.dt) > 1e-12:
        raise InputError("The x and y floor motions must have the same time step")
    build_model3d(model)

    # gravity (static, load control)
    op.constraints("Transformation")
    op.numberer("RCM")
    op.system("BandGeneral")
    op.test("NormDispIncr", 1.0e-8, 200)
    op.algorithm("Newton")
    op.integrator("LoadControl", 1.0 / s.gravity_steps)
    op.analysis("Static")
    if op.analyze(s.gravity_steps) != 0:
        raise RuntimeError("Gravity analysis of the 3D model failed")
    op.loadConst("-time", 0.0)

    periods = [2 * math.pi / math.sqrt(lam) for lam in op.eigen(4)]
    i, j = s.rayleigh_modes
    lam = op.eigen(max(i, j))
    wi, wj = math.sqrt(lam[i - 1]), math.sqrt(lam[j - 1])
    xi = s.damping_ratio
    op.rayleigh(s.mass_proportional * xi * (2 * wi * wj) / (wi + wj), s.current_stiffness * 2 * xi / (wi + wj),
                s.initial_stiffness * 2 * xi / (wi + wj), s.committed_stiffness * 2 * xi / (wi + wj))

    dt = motion_x.dt
    npts = min(len(motion_x.acc), len(motion_y.acc))
    t_max = dt * npts
    op.timeSeries("Path", 1000, "-dt", dt, "-values", *motion_x.acc, "-factor", 1, "-prependZero")
    op.timeSeries("Path", 2000, "-dt", dt, "-values", *motion_y.acc, "-factor", 1, "-prependZero")
    op.pattern("UniformExcitation", 100, 1, "-accel", 1000)
    op.pattern("UniformExcitation", 200, 2, "-accel", 2000)

    nodes_x, nodes_y = model.node_groups["X"], model.node_groups["Y"]
    with tempfile.TemporaryDirectory() as tmp:
        fx, fy = Path(tmp) / "x.out", Path(tmp) / "y.out"
        op.recorder("Node", "-file", str(fx), "-time", "-dt", dt, "-node", *nodes_x, "-dof", 1, "disp")
        op.recorder("Node", "-file", str(fy), "-time", "-dt", dt, "-node", *nodes_y, "-dof", 2, "disp")

        op.wipeAnalysis()
        op.integrator("Newmark", 0.5, 0.25)
        op.numberer("RCM")
        op.system("FullGeneral")
        op.constraints("Transformation")
        op.test(s.test, s.tolerance, s.max_iterations)
        op.algorithm("Newton")
        op.analysis("Transient")

        done, ok = 0, 0
        while done < npts and ok == 0:        # same as analyze(npts, dt), in chunks to report progress
            n = min(chunk, npts - done)
            ok = op.analyze(n, dt)
            done += n
            if progress:
                progress(min(op.getTime() / t_max, 1.0))

        if ok != 0:
            def main():
                op.test(s.test, s.tolerance, s.max_iterations)
                op.algorithm("Newton")

            def fallback():
                op.test(s.fallback_test, s.fallback_tolerance, s.fallback_max_iterations)

            ok = 0
            control_time = op.getTime()
            last_report = control_time
            while control_time < t_max and ok == 0:
                control_time = op.getTime()
                ok = op.analyze(1, dt)
                if ok != 0:
                    fallback()
                    op.algorithm("Newton", "-initial")
                    ok = op.analyze(1, dt / 2)
                    main()
                if ok != 0:
                    op.algorithm("Broyden", 50)
                    fallback()
                    ok = op.analyze(1, dt / 2)
                    main()
                if ok != 0:
                    op.algorithm("NewtonLineSearch")
                    fallback()
                    ok = op.analyze(1, dt / 10)
                    main()
                if ok != 0:
                    op.algorithm("KrylovNewton")
                    fallback()
                    ok = op.analyze(1, dt / 20)
                    main()
                if progress and control_time - last_report > 0.02 * t_max:
                    last_report = control_time
                    progress(min(control_time / t_max, 1.0))
        end_time = op.getTime()
        op.wipe()
        ax = np.loadtxt(fx, ndmin=2)
        ay = np.loadtxt(fy, ndmin=2)

    n = min(len(ax), len(ay))
    return Response3D(
        model=model.name, record_x=motion_x.record, record_y=motion_y.record, level=motion_x.level,
        periods=periods, time=ax[:n, 0], nodes_x=list(nodes_x), nodes_y=list(nodes_y),
        ux=ax[:n, 1:], uy=ay[:n, 1:], completed=end_time >= t_max - 0.5 * dt, end_time=end_time, duration=t_max,
    )


def braced_peaks(model: Model3D, response: Response3D) -> dict[str, float]:
    """Largest peak displacement over the braced nodes, per direction: the measure stored in the paper's
    ``Results/*_DispX.txt`` / ``*_DispY.txt``."""
    out = {}
    for d, nodes, peaks in (("x", response.nodes_x, response.peak_x), ("y", response.nodes_y, response.peak_y)):
        idx = [nodes.index(n) for n in model.node_groups.get(f"{d.upper()}t", []) if n in nodes]
        out[d] = float(peaks[idx].max()) if idx else float("nan")
    return out
