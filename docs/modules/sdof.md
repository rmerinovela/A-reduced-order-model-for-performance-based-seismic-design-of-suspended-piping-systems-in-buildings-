# `piperom/sdof.py`: equivalent SDOF parameters

## Responsibility

Derives the equivalent SDOF at a chosen Δc: Γ, effective mass, the supports with their shape value φ,
and the scaled Pinching4 spring of each support. It replaces the values typed by hand into the paper's
`Pushover_SDOF/*.py`, and reproduces the paper's `equivalent_static.py` → `NLTHA_SDOF.py` chain.

## Interface

**`derive_sdof(system, settings, delta_c=None) -> SDOFParameters`**: runs `pushover.run_step` at
`delta_c` (default: `settings.sdof_delta_c`) from a uniform shape.

**`sdof_from_step(rs, step) -> SDOFParameters`**: the same from an existing pushover step, without
re-analysing.

**`SDOFSupport`**:

| Field | Content |
|---|---|
| `kind` | `"transverse"` (braced hanger) or `"longitudinal"` (branch) |
| `dof`, `x`, `branch` | position in the DOF list, coordinate, branch index |
| `phi` | shape value (normalised to the reference DOF) |
| `n_trapezes` | 1, or the branch's `n_braces` |
| `spring` | the scaled `Pinching4`: deformations / (Γ·φ), forces × `n_trapezes` |

**`SDOFParameters`**:
- fields: `name`, `delta_c`, `gamma`, `effective_mass`, `total_mass`, `mass_ratio`, `u_sdof`,
  `base_shear`, `converged`, `iterations`, `supports` (transverse first, then branches), `d_norm`;
- `n_transverse`, `n_longitudinal_trapezes`, `support_shape` (the `DispShape` vector of the paper's
  scripts);
- `to_dict()` / `to_yaml()`, `springs_csv()`, `write(out_dir)` (`sdof_parameters.yaml`, `sdof_springs.csv`).

## Design notes

- Each branch's longitudinal strength is `n_braces` × the trapeze, consistent with the static model. The
  paper's `NLTHA_SDOF.py` divides the total by the number of branches, which differs when branches have
  different counts ([legacy_issues.md](../legacy_issues.md), A3).
- The SDOF isn't analysed here; `timehistory.SDOFModel.from_parameters` turns the parameters into
  an analysable model.

## Tests

`tests/test_regression.py::test_sdof_parameters_reproduce_equivalent_static_pipeline`. It runs the
untouched paper script and compares Γ, M_eff, u_SDOF, the full shape, the support shape and every
scaled envelope point (relative tolerance 1e-12).
