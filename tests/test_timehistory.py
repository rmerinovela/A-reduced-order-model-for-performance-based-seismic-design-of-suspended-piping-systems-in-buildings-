"""Time-history engines against the paper's stored results (need the floor motions in motions/)."""

import numpy as np
import pytest

from piperom.inputs import InputError
from piperom.motions import MOTIONS_DIR, load_motion_sets, motion_set, select_runs
from piperom.timehistory import TimeHistorySettings, run_sdof_time_history
from piperom.trapeze import Pinching4, load_trapeze
from validation.legacy import PAPER, hand_typed_sdof_model

HAVE_MOTIONS = (MOTIONS_DIR / "floor_motions" / "ResultsS4" / "FloorAcc_IM10_120111.txt").exists()
needs_motions = pytest.mark.skipif(not HAVE_MOTIONS, reason="floor motions not available in motions/")


def test_pinching4_opensees_args_roundtrip():
    p = load_trapeze("default", "longitudinal")
    again = Pinching4.from_opensees_args(p.opensees_args(), name=p.name)
    assert again == p


def test_motion_catalogue_and_selection():
    sets = load_motion_sets()
    assert {"S4_IM", "S4_150"} <= set(sets)
    ms = sets["S4_IM"]
    assert len(ms.records) == 44 and len(ms.pairs()) == 22 and ms.levels == list(range(1, 13))
    assert len(select_runs(ms, [1, 2], None)) == 88
    assert select_runs(ms, [3], ["120111"]) == [("120111", 3)]
    assert len(select_runs(sets["S4_150"])) == 150
    with pytest.raises(InputError, match="not available"):
        select_runs(ms, [13], None)
    with pytest.raises(InputError, match="not in motion set"):
        select_runs(ms, [1], ["999"])


@needs_motions
@pytest.mark.parametrize("tag, key", [("M01x", "dispXs"), ("M01y", "dispYs")])
def test_sdof_time_history_reproduces_paper(tag, key):
    """Paper SDOF peaks: columns = IM1-IM10, rows = records in Names.txt order."""
    ms, s = motion_set("S4_IM"), TimeHistorySettings.from_dict()
    model = hand_typed_sdof_model(tag)
    ref = np.load(PAPER / "Results" / f"{tag[:3]}_peak_displacements.npy", allow_pickle=True).item()[key]
    for row in (0, 1, 7):
        for level in (3, 10):
            peak = run_sdof_time_history(model, ms.load(ms.records[row], level), s).peak_u
            assert peak == pytest.approx(ref[row, level - 1], rel=2e-3)


@needs_motions
def test_3d_verification_reproduces_paper():
    """Largest peak over the braced nodes = Results/M01_biron_DispX/Y.txt (row = record index)."""
    from piperom.verification3d import Verification3DSettings, braced_peaks, load_model3d, run_3d
    ms, m = motion_set("S4_IM"), load_model3d("M01")
    rx, ry = ms.pairs()[0]
    r = run_3d(m, ms.load(rx, 10), ms.load(ry, 10), Verification3DSettings.from_dict())
    assert r.completed
    R = PAPER / "Results"
    for d, peak in braced_peaks(m, r).items():
        rec = rx if d == "x" else ry
        ref = np.loadtxt(R / f"M01_biron_Disp{d.upper()}.txt")[ms.records.index(rec), 9]
        assert peak == pytest.approx(ref, abs=0.006)
