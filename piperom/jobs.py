"""Entry points for running analyses in a separate process.

OpenSeesPy keeps a single global model per Python process, so concurrent analyses in one process
(e.g. several app sessions served by threads) would overwrite each other's models. Callers that may
run analyses concurrently should execute these functions in a worker process.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from . import INPUTS_DIR
from .inputs import AnalysisSettings, PipingSystem, load_system
from .motions import motion_set
from .pushover import PushoverResult, run_pushover
from .sdof import SDOFParameters, derive_sdof
from .timehistory import SDOFModel, SDOFResponse, TimeHistorySettings, run_sdof_time_history
from .verification3d import Response3D, Verification3DSettings, load_model3d, run_3d

MAX_STORED_HISTORIES = 100


def pushover_job(system: PipingSystem, settings: AnalysisSettings, queue=None) -> PushoverResult:
    progress = (lambda k, n, step: queue.put((k, n))) if queue is not None else None
    return run_pushover(system, settings, progress)


def sdof_job(system: PipingSystem, settings: AnalysisSettings, delta_c: float) -> SDOFParameters:
    return derive_sdof(system, settings, delta_c)


def sdof_time_history_job(model: SDOFModel, set_name: str, runs: list[tuple[str, int | None]], floor: int,
                          settings: AnalysisSettings, queue=None) -> list[SDOFResponse]:
    """Run the SDOF for each (record, level); time histories are kept only for small batches."""
    ms = motion_set(set_name)
    s = TimeHistorySettings.from_dict(settings.sdof_time_history)
    out = []
    for k, (record, level) in enumerate(runs):
        r = run_sdof_time_history(model, ms.load(record, level, floor), s)
        if len(runs) > MAX_STORED_HISTORIES:
            r.time = r.u = r.force = np.array([])
        out.append(r)
        if queue is not None:
            queue.put((k + 1, len(runs)))
    return out


@dataclass
class RomPrediction:
    direction: str
    system: str
    record: str
    gamma: float
    phi_max: float
    peak_u: float
    completed: bool

    @property
    def peak_support_displacement(self) -> float:
        return self.gamma * self.phi_max * self.peak_u


@dataclass
class VerificationResult:
    response: Response3D
    rom: dict[str, RomPrediction]


def verification_job(model_name: str, set_name: str, record_x: str, record_y: str, level: int | None,
                     floor: int, settings: AnalysisSettings, queue=None) -> VerificationResult:
    """3D analysis under (record_x, record_y) and the reduced-order prediction for each direction."""
    ms = motion_set(set_name)
    mx, my = ms.load(record_x, level, floor), ms.load(record_y, level, floor)
    model = load_model3d(model_name)
    th = TimeHistorySettings.from_dict(settings.sdof_time_history)
    rom = {}
    for direction, motion in (("x", mx), ("y", my)):
        name = model.rom_systems.get(direction)
        path = INPUTS_DIR / "archetypes" / f"{name}.yaml"
        if not name or not path.exists():
            continue
        p = derive_sdof(load_system(path), settings)
        sm = SDOFModel.from_parameters(p)
        r = run_sdof_time_history(sm, motion, th)
        rom[direction] = RomPrediction(direction, name, motion.record, p.gamma, max(sm.support_phi),
                                       r.peak_u, r.completed)
    progress = (lambda f: queue.put((f, 1.0))) if queue is not None else None
    response = run_3d(model, mx, my, Verification3DSettings.from_dict(settings.verification_3d), progress)
    return VerificationResult(response, rom)
