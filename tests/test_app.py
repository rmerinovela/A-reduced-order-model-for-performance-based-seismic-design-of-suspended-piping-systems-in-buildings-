"""Smoke test of the Streamlit app (headless)."""

from pathlib import Path

import pytest

st_testing = pytest.importorskip("streamlit.testing.v1")
APP = str(Path(__file__).resolve().parents[1] / "app" / "streamlit_app.py")


def button(at, label):
    return next(b for b in at.button if b.label == label)


def test_app_runs_pushover_and_sdof():
    at = st_testing.AppTest.from_file(APP, default_timeout=180)
    at.run()
    assert not at.exception, at.exception

    # switch input modes back and forth: inputs must survive
    at.radio(key="h_mode").set_value("Explicit positions").run()
    at.radio(key="h_mode").set_value("Regular grid").run()
    at.radio(key="b_mode").set_value("Evenly spaced").run()
    at.radio(key="b_mode").set_value("Select hangers").run()
    assert not at.exception, at.exception
    assert at.session_state.h_first == 1000

    at.number_input(key="s_n").set_value(4).run()
    button(at, "Run pseudo-pushover").click().run()
    assert not at.exception, at.exception
    assert len(at.session_state.po_result.steps) == 4

    button(at, "Derive SDOF parameters").click().run()
    assert not at.exception, at.exception
    sd = at.session_state.sdof_result
    assert sd.delta_c == 12.0 and sd.n_transverse == 5


@pytest.mark.skipif(not (Path(__file__).resolve().parents[1] / "motions" / "floor_motions" / "ResultsS4").exists(),
                    reason="floor motions not available")
def test_app_runs_time_history_and_3d():
    at = st_testing.AppTest.from_file(APP, default_timeout=600)
    at.run()
    button(at, "Derive SDOF parameters").click().run()
    at.toggle(key="th_all").set_value(False).run()
    button(at, "Run SDOF time histories").click().run()
    assert not at.exception, at.exception
    model, resp = at.session_state.th_result
    assert len(resp) == 2 and all(r.completed for r in resp)

    button(at, "Run 3D verification").click().run()
    assert not at.exception, at.exception
    res = at.session_state.v3_result
    assert res.response.completed and set(res.rom) == {"x", "y"}


def test_app_reports_invalid_geometry():
    at = st_testing.AppTest.from_file(APP, default_timeout=60)
    at.run()
    at.radio(key="h_mode").set_value("Explicit positions").run()
    at.text_area(key="h_positions").set_value("1000, 500").run()
    assert not at.exception, at.exception
    assert any("increasing" in e.value for e in at.error)
