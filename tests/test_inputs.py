"""Input handling: alternative ways of defining the same system must give identical models."""

import numpy as np
import pytest

from piperom.inputs import AnalysisSettings, InputError, PipingSystem, load_settings, load_system
from piperom.pushover import run_step
from piperom.trapeze import DEFAULT_TRAPEZE_FILES, load_trapeze, parse_trapeze_csv, trilinear_from_pinching4
from validation.legacy import ARCHETYPE_DIR, REPO

BASE = {
    "name": "t",
    "main_line": {"length": 18000, "n_pipes": 3},
    "hangers": {"first": 1000, "spacing": 3000},
    "braces": {"mask": [0, 1, 0, 1, 0, 1]},
    "branches": [{"x": 18000, "length": 36000, "n_pipes": 3, "n_braces": 4}],
}


def system(**over):
    d = {**BASE, **over}
    return PipingSystem.from_dict(d)


def first_step(s):
    rs = s.resolve()
    step, _ = run_step(rs, load_settings(), 12.0)
    return step


def test_default_trapezes_are_the_repository_files():
    for kind in ("transverse", "longitudinal"):
        assert DEFAULT_TRAPEZE_FILES[kind].parent == REPO / "inputs" / "trapezes"
        load_trapeze("default", kind)


def test_trilinear_from_pinching4_matches_original_transverse_constants():
    tri = trilinear_from_pinching4(load_trapeze("default", "transverse"))
    assert (tri.d1, tri.d2, tri.f1, tri.f2) == (10.0, 17.0, 6000.0, 9000.0)
    assert tri.k3 == pytest.approx(0.01 * 600.0)


def test_trapeze_csv_roundtrip_and_prefix_free():
    p = load_trapeze("default", "longitudinal")
    again = parse_trapeze_csv(p.to_csv(prefix="X"), name="x")
    assert again.parameters() == p.parameters()


def test_trapeze_csv_errors():
    text = DEFAULT_TRAPEZE_FILES["transverse"].read_text()
    with pytest.raises(ValueError, match="missing"):
        parse_trapeze_csv("\n".join(l for l in text.splitlines() if not l.startswith("TgE")))
    with pytest.raises(ValueError, match="increasing"):
        parse_trapeze_csv(text.replace("TePd3,17", "TePd3,5"))


@pytest.mark.parametrize("braces", [{"positions": [4000, 10000, 16000]}, {"count": 3}])
def test_brace_definitions_are_equivalent(braces):
    a, b = system(), system(braces=braces)
    np.testing.assert_array_equal(a.resolve().brace_mask, b.resolve().brace_mask)


def test_hanger_grid_equals_explicit_positions():
    a = system()
    b = system(hangers={"positions": [1000, 4000, 7000, 10000, 13000, 16000]})
    np.testing.assert_array_equal(a.resolve().hanger_x, b.resolve().hanger_x)
    assert first_step(a).gamma == first_step(b).gamma


def test_end_clearance_controls_grid():
    def n_hangers(clearance):
        return len(system(hangers={"first": 1000, "spacing": 3000, "end_clearance": clearance}).hanger_x())

    assert len(system().hanger_x()) == 6
    assert n_hangers(500) == 6
    assert n_hangers(2500) == 5


def test_branches_from_csv(tmp_path):
    (tmp_path / "b.csv").write_text("x,length,n_pipes,n_braces\n18000,36000,3,4\n")
    (tmp_path / "s.yaml").write_text(
        "main_line: {length: 18000, n_pipes: 3}\nhangers: {first: 1000, spacing: 3000}\n"
        "braces: {mask: [0,1,0,1,0,1]}\nbranches: b.csv\n")
    assert first_step(load_system(tmp_path / "s.yaml")).gamma == first_step(system()).gamma


def test_yaml_roundtrip_of_all_archetypes(tmp_path):
    for path in sorted(ARCHETYPE_DIR.glob("*.yaml")):
        s = load_system(path)
        (tmp_path / "x.yaml").write_text(s.to_yaml())
        again = load_system(tmp_path / "x.yaml")
        assert again.to_dict() == s.to_dict()


def test_custom_trapeze_file_is_used(tmp_path):
    text = DEFAULT_TRAPEZE_FILES["transverse"].read_text().replace("TePf2,6000", "TePf2,3000")
    (tmp_path / "t.csv").write_text(text)
    s = system(trapezes={"transverse": str(tmp_path / "t.csv")})
    assert s.resolve().transverse_trilinear.f1 == 3000.0
    assert first_step(s).base_shear < first_step(system()).base_shear


@pytest.mark.parametrize("over, msg", [
    ({"branches": []}, "At least one branch"),
    ({"braces": {"mask": [0, 1]}}, "6 hangers"),
    ({"braces": {"mask": [0, 1, 0, 1, 0, 1], "count": 2}}, "exactly one"),
    ({"braces": {"positions": [5000]}}, "not at a hanger"),
    ({"branches": [{"x": 4000, "length": 1000, "n_pipes": 1, "n_braces": 1}]}, "braced hanger"),
    ({"branches": [{"x": 19000, "length": 1000, "n_pipes": 1, "n_braces": 1}]}, "on the main line"),
    ({"hangers": {"positions": [3000, 1000]}}, "increasing"),
    ({"main_line": {"length": -1, "n_pipes": 3}}, "> 0"),
    ({"unknown_key": 1}, "Unknown"),
])
def test_invalid_inputs(over, msg):
    with pytest.raises(InputError, match=msg):
        system(**over).resolve()


def test_settings_defaults_and_overrides():
    s = load_settings()
    np.testing.assert_array_equal(s.delta_c(), np.linspace(0.1, 50.0, 50))
    s2 = AnalysisSettings.from_dict({"pushover": {"delta_c_values": [1, 2, 5]}, "sdof": {"delta_c": 7}})
    np.testing.assert_array_equal(s2.delta_c(), [1.0, 2.0, 5.0])
    assert s2.sdof_delta_c == 7.0 and s2.max_iterations == 50
    with pytest.raises(InputError, match="Unknown"):
        AnalysisSettings.from_dict({"pushover": {"steps": 3}})
