"""The new codebase against the results of the original scripts."""

import numpy as np
import pytest

from piperom.inputs import load_system
from piperom.sdof import derive_sdof
from validation.legacy import (ARCHETYPES, EQUIV_STATIC_EXAMPLE, LEGACY_L, compare_pushover,
                               extract_support_displacements, legacy_settings, run_legacy_equivalent_static)


@pytest.mark.parametrize("tag", ARCHETYPES)
def test_pushover_reproduces_legacy_results(tag):
    """Every value of Pushover2D/pushover_results_<tag>.txt (written with 3 decimals) is reproduced."""
    cmp = compare_pushover(tag)
    assert cmp["n_diff"] == 0, f"{tag}: {cmp['n_diff']} of {cmp.get('n_cells')} values differ"
    assert cmp["max_abs_diff"] <= 0.0005 + 1e-9


def test_sdof_parameters_reproduce_equivalent_static_pipeline(tmp_path):
    """derive_sdof reproduces equivalent_static.py + the parameter extraction of NLTHA_SDOF.py."""
    ref = run_legacy_equivalent_static(tmp_path)
    system = load_system(EQUIV_STATIC_EXAMPLE)
    system.trapezes["longitudinal"] = str(LEGACY_L)
    rs = system.resolve()
    params = derive_sdof(rs, legacy_settings(), delta_c=float(ref["dc"]))

    assert np.array_equal(rs.brace_mask, ref["stiff_mask"])
    assert params.n_transverse == int(ref["nT"])
    assert params.n_longitudinal_trapezes == int(ref["nL"])
    assert params.gamma == pytest.approx(float(ref["Gamma"]), rel=1e-12)
    assert params.effective_mass == pytest.approx(float(ref["M_eff"]), rel=1e-12)
    assert params.u_sdof == pytest.approx(float(ref["u_sdof"]), rel=1e-12)
    np.testing.assert_allclose(params.d_norm, ref["d_norm"], rtol=1e-12)
    disp_shape = extract_support_displacements(ref["d_norm"], ref["stiff_mask"], int(ref["nOrth"]))
    np.testing.assert_allclose(params.support_shape, disp_shape, rtol=1e-12)

    # Scaled Pinching4 envelopes as built in NLTHA_SDOF.py (single branch: nL/n_ortho = n_braces)
    gamma = float(ref["Gamma"])
    for s, phi in zip(params.supports, disp_shape):
        base = rs.transverse if s.kind == "transverse" else rs.longitudinal
        n = 1 if s.kind == "transverse" else int(ref["nL"]) / int(ref["nOrth"])
        np.testing.assert_allclose(s.spring.pos_disp, [v / (gamma * phi) for v in base.pos_disp], rtol=1e-12)
        np.testing.assert_allclose(s.spring.neg_disp, [v / (gamma * phi) for v in base.neg_disp], rtol=1e-12)
        np.testing.assert_allclose(s.spring.pos_force, [n * v for v in base.pos_force], rtol=1e-12)
        np.testing.assert_allclose(s.spring.neg_force, [n * v for v in base.neg_force], rtol=1e-12)
