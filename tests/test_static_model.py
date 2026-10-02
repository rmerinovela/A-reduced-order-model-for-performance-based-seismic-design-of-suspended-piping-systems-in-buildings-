"""Equilibrium of the equivalent static load pattern (docs/legacy_issues.md, A2)."""

import numpy as np
import pytest

from piperom.static_model import SolverSettings, solve_static_step
from validation.legacy import ARCHETYPES, archetype


def spring_forces_and_base_shear(tag, split, delta=20.0):
    rs = archetype(tag, legacy_trapezes=False).resolve()
    d = np.ones(rs.n_dof)
    step = solve_static_step(rs, d, delta, SolverSettings("NormDispIncr", 1e-8, 50, split))
    braced = np.where(rs.brace_mask == 1)[0]
    springs = np.sum(step.brace_stiffness * delta * d[braced]) + np.sum(step.branch_stiffness * delta * d[rs.n_hangers:])
    return springs, step.base_shear


@pytest.mark.parametrize("tag", ARCHETYPES)
def test_consistent_split_applies_the_full_spring_forces(tag):
    springs, base_shear = spring_forces_and_base_shear(tag, "consistent")
    assert base_shear == pytest.approx(springs, rel=1e-12)


def test_legacy_split_loses_part_of_the_branch_force():
    springs, base_shear = spring_forces_and_base_shear("M01y", "legacy")
    assert base_shear < springs
