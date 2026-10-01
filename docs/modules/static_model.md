# `piperom/static_model.py`: equivalent static analysis (OpenSees)

## Responsibility

The numerical core: for one assumed shape and one target displacement, it builds the reduced model in
OpenSees, computes the inertial load pattern, solves, and returns the displacements and modal
quantities. It also holds the fixed-point iteration on the shape. Method:
[methodology.md](../methodology.md#1-equivalent-static-procedure-at-a-target-displacement-δc).

It's a restructured port of `build_model` / `iterate_shape_from_static` of the paper's
`Pushover2D/Functions.py`, with:
- the **same OpenSees commands, tags, creation order and floating-point operation order**;
- the regression tests reproducing the paper's results exactly.

Don't "simplify" the arithmetic without re-running `tests/test_regression.py`.

## Interface

**`solve_static_step(rs, d, delta, solver) -> StaticStep`**: one model build and linear solve.

`StaticStep` fields:

| Field | Content |
|---|---|
| `u` | displacements at the DOFs |
| `dof_x`, `dof_mass`, `branch_mass` | DOF positions and masses |
| `loads`, `branch_stay_load` | applied loads |
| `brace_stiffness`, `branch_stiffness` | secant stiffnesses used |
| `gamma`, `effective_mass`, `total_mass`, `mass_ratio` | modal quantities |
| `base_shear`, `f_push` | base shear and load pattern |

**`iterate_shape(rs, d_init, delta, max_iterations, tolerance, solver) -> ShapeResult`**: repeats the solve,
normalising the displacements to max |u| = 1, until the RMS change is below `tolerance`.

`ShapeResult` fields:

| Field | Content |
|---|---|
| `d_star` | converged shape |
| `step` | the last `StaticStep` |
| `iterations`, `converged` | iteration count and status |
| `history` | RMS change per iteration |

Other members:
- `SolverSettings(test, tolerance, max_iterations)`: the OpenSees convergence test of each solve.
- `normalize_shape(phi)`: divides by max |φ|.

## Internal structure of `solve_static_step`

1. Section properties (`_section`) and mass per length.
2. Main-line mesh: nodes at 0, hangers, branch junctions and L. A branch closer than `SNAP_TOL` to a node
   snaps onto it.
3. Lumped masses from tributary lengths; elastic beam chain.
4. Hangers:
   - fixed top node, bottom node rigid-linked to the beam;
   - zeroLength spring between them: brace secant stiffness (braced) or `SOFT_STIFFNESS` (unbraced),
     rigid in z and rotations.
5. Branches: a node offset by `BRANCH_OFFSET`, a beam stub, the lumped mass and a spring of stiffness
   `n_braces` × longitudinal secant.
6. Load pattern:
   - branch force split into stay and pass parts, in one loop (`_neighbours` finds the tributary
     window);
   - pass part divided left/right;
   - segment-wise redistribution ∝ m·d between branch junctions.
7. Static solve; Γ, M_eff, mass ratio and base shear with the shape normalised to the last DOF (the
   reference branch).

The paper's code also ran a diagnostic `eigen(2)` at every solve, whose result nothing used. It's
omitted: results are unchanged (regression tests) and the pushover runs about 3× faster.

## Side effects and constraints

- Uses OpenSees' **global** model: calls `op.wipe()` first and sends OpenSees output to `/dev/null`. Not
  thread-safe; run concurrent analyses in separate processes (`jobs`).
- Tag scheme (`MAIN_NODE`, `HANGER_*`, `BRANCH_*`, …) limits a model to 299 hangers, checked in
  `inputs`.
- Raises `RuntimeError` if the static solve fails (it's linear, so this signals a malformed model).

## Known behaviours kept from the paper's code

- The stay and pass parts of a branch force don't sum to the branch force ([legacy_issues.md](../legacy_issues.md),
  A2).
- Branch DOF displacements are read at the main-line junction node, not at the lumped branch node.

## Tests

`tests/test_regression.py` reproduces all 18 `pushover_results_*.txt` files through `pushover`.
