"""Helpers comparing the new codebase with the results of the original scripts
(in ``code implementation for paper/``).

The original static procedure used a longitudinal trapeze backbone of 11500 N at 24 mm, whereas the
Pinching4 file has 10000 N at 24 mm. ``legacy_static_C-TPS-L.csv`` reproduces the value the scripts
actually used, so the new engine can be checked against their results.
"""

from __future__ import annotations

import re
import tempfile
import subprocess
import sys
from pathlib import Path

import numpy as np

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from piperom.inputs import PipingSystem, load_settings, load_system  # noqa: E402
from piperom.pushover import PushoverResult, run_pushover  # noqa: E402
from piperom.sdof import sdof_from_step  # noqa: E402

LEGACY_L = Path(__file__).resolve().parent / "legacy_static_C-TPS-L.csv"
PAPER = REPO / "code implementation for paper"   # original scripts and results
ARCHETYPE_DIR = REPO / "inputs" / "archetypes"
ARCHETYPES = sorted(p.stem for p in ARCHETYPE_DIR.glob("*.yaml"))
EQUIV_STATIC_EXAMPLE = REPO / "inputs" / "examples" / "equivalent_static_example.yaml"


def archetype(tag: str, legacy_trapezes: bool = True) -> PipingSystem:
    system = load_system(ARCHETYPE_DIR / f"{tag}.yaml")
    if legacy_trapezes:
        system.trapezes["longitudinal"] = str(LEGACY_L)
    return system


def legacy_driver(tag: str) -> Path:
    return PAPER / "Pushover2D" / f"CS_Lumped_Iter_{tag}_cont_PO.py"


def legacy_table(result: PushoverResult, tag: str) -> np.ndarray:
    """New results laid out like ``pushover_results_<tag>.txt`` (incl. the driver's DOF sorting)."""
    sort = "d_norm[order]" in legacy_driver(tag).read_text()
    order = np.argsort(np.array([d["x"] for d in result.dofs])) if sort else slice(None)
    return np.array([[s.delta_c, s.gamma, s.effective_mass, s.base_shear, s.mass_ratio, s.u_sdof,
                      *s.d_norm[order], *s.d_scaled[order], *s.f_push[order]] for s in result.steps])


def compare_pushover(tag: str) -> dict:
    result = run_pushover(archetype(tag), load_settings())
    new = legacy_table(result, tag)
    ref = np.loadtxt(PAPER / "Pushover2D" / f"pushover_results_{tag}.txt")
    if new.shape != ref.shape:
        return {"tag": tag, "shape_new": new.shape, "shape_ref": ref.shape, "n_diff": -1}
    formatted = np.vectorize(lambda v: float(f"{v:.3f}"))(new)
    return {"tag": tag, "n_cells": ref.size, "n_diff": int((formatted != ref).sum()),
            "max_abs_diff": float(np.abs(new - ref).max()), "result": result}


def run_legacy_equivalent_static(workdir: Path) -> dict:
    """Run the untouched ``code_proposed_procedure/equivalent_static.py`` in ``workdir``."""
    workdir.mkdir(parents=True, exist_ok=True)
    script = PAPER / "code_proposed_procedure" / "equivalent_static.py"
    subprocess.run([sys.executable, str(script)], cwd=workdir, check=True, capture_output=True,
                   env={"MPLBACKEND": "Agg", "PATH": ""})
    data = np.load(workdir / "Results" / "EquivStatic" / "equiv_static_nT4_nL3.npz")
    return {k: data[k] for k in data.files}


def extract_support_displacements(d_dof, stiff_mask, n_orth):
    """Copy of the function in ``code_proposed_procedure/NLTHA_SDOF.py``."""
    d_dof = np.asarray(d_dof)
    stiff_mask = np.asarray(stiff_mask, dtype=bool)
    d_stiff = d_dof[:len(stiff_mask)][stiff_mask]
    return np.concatenate([d_stiff, d_dof[-n_orth:]]) if n_orth > 0 else d_stiff


def hand_typed_sdof(tag: str) -> dict:
    """Constants typed into ``Pushover_SDOF/<tag>_SDOF.py``."""
    src = (PAPER / "Pushover_SDOF" / f"{tag}_SDOF.py").read_text()
    shape = re.search(r"^DispShape = (.*)$", src, re.M).group(1)
    n_shape = int(re.search(r"np\.ones\((\d+)\)", shape).group(1)) if "ones" in shape else None
    return {
        "mass": float(re.search(r"^mass = \[([\d.]+)", src, re.M).group(1)),
        "gamma": float(re.search(r"^Gamma = (.*)$", src, re.M).group(1)),
        "shape": np.ones(n_shape) if n_shape else np.array(eval(shape), float),
        "rigid": n_shape is not None,
        "nT": int(re.search(r"^nT = (\d+)", src, re.M).group(1)),
        "nL": int(re.search(r"^nL = (\d+)", src, re.M).group(1)),
    }


def match_hand_typed(tag: str, result: PushoverResult) -> dict:
    """Find the pushover step whose derived SDOF parameters best match the hand-typed ones."""
    ht = hand_typed_sdof(tag)
    rs = archetype(tag).resolve()
    best = None
    for k, step in enumerate(result.steps):
        p = sdof_from_step(rs, step)
        T = np.array([s.phi for s in p.supports if s.kind == "transverse"])
        ht_T = ht["shape"][:ht["nT"]]
        if len(T) == len(ht_T):
            err_T = min(np.abs(T - ht_T).max(), np.abs(T[::-1] - ht_T).max())
        else:
            err_T = np.inf
        score = err_T + abs(p.gamma - ht["gamma"])
        if best is None or score < best["score"]:
            best = {"score": score, "step": k, "delta_c": step.delta_c, "gamma": p.gamma,
                    "effective_mass": p.effective_mass, "max_dphi_T": err_T,
                    "nT": p.n_transverse, "nL": p.n_longitudinal_trapezes}
    best["hand"] = ht
    return best


# ----------------------------------------------------------------------------- capturing OpenSees models

class StopCapture(Exception):
    pass


class OpenSeesRecorder:
    """Stand-in for ``openseespy.opensees`` that records calls instead of executing them."""

    def __init__(self, stop_at: set[str]):
        self.calls: list[tuple[str, tuple]] = []
        self._stop_at = stop_at

    def __getattr__(self, name):
        if name.startswith("_"):
            raise AttributeError(name)

        def call(*args):
            if name in self._stop_at:
                raise StopCapture(name)
            self.calls.append((name, args))
            return [] if name == "eigen" else 0
        return call


def capture_opensees_calls(script: Path, stop_at: set[str], patch=None) -> tuple[list, dict]:
    """Execute ``script`` with a recording ``op`` until one of ``stop_at`` is called.

    Returns the recorded calls and the script's global variables at that point. The script runs in a
    temporary working directory, so folders it creates don't end up in the repository.
    """
    import os
    src = script.read_text()
    src = src.replace("import openseespy.opensees as op", "").replace("import vfo.vfo as vfo", "")
    if patch:
        src = patch(src)
    rec = OpenSeesRecorder(stop_at)
    ns = {"__name__": "__capture__", "op": rec}
    cwd = os.getcwd()
    with tempfile.TemporaryDirectory() as tmp:
        os.chdir(tmp)
        try:
            exec(compile(src, str(script), "exec"), ns)
        except StopCapture:
            pass
        finally:
            os.chdir(cwd)
    return rec.calls, ns


def hand_typed_sdof_model(tag: str):
    """The SDOF defined in ``Pushover_SDOF/<tag>_SDOF.py`` (mass and parallel springs as typed)."""
    from piperom.timehistory import SDOFModel
    from piperom.trapeze import Pinching4
    calls, _ = capture_opensees_calls(PAPER / "Pushover_SDOF" / f"{tag}_SDOF.py", {"eigen", "recorder", "analyze"})
    mass = next(float(a[a.index("-mass") + 1]) for n, a in calls if n == "node" and "-mass" in a)
    mats = {a[1]: Pinching4.from_opensees_args(a[2:], name=f"{tag} mat {a[1]}")
            for n, a in calls if n == "uniaxialMaterial" and a[0] == "Pinching4"}
    parallel = next(a for n, a in calls if n == "uniaxialMaterial" and a[0] == "Parallel")
    return SDOFModel(name=tag, mass=mass, springs=[mats[t] for t in parallel[2:]])
