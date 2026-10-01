# `piperom/pushover.py`: adaptive pseudo-pushover

## Responsibility

Runs the equivalent static procedure over a list of target displacements, builds the capacity curve and
the adaptive shapes, and writes them to CSV.

## Interface

**`run_pushover(system, settings, progress=None) -> PushoverResult`**:
- `system` is a `PipingSystem` (resolved internally) or a `ResolvedSystem`.
- `progress(k, n, step)` is called after each step; the CLI prints, the app updates a progress bar.
- `settings.warm_start` decides whether each step starts from the previous shape or from a uniform
  one.

**`run_step(rs, settings, delta_c, d_init=None) -> (PushoverStep, ShapeResult)`**: one Δc. Also used by `sdof`.

**`PushoverStep`**: one point of the curve, derived from a `ShapeResult` by `from_shape`.

| Field | Content |
|---|---|
| `delta_c`, `base_shear`, `u_sdof` | capacity-curve point; u_SDOF = Δc / (Γ · max d_norm) |
| `gamma`, `effective_mass`, `total_mass`, `mass_ratio` | modal quantities |
| `d_norm` | shape normalised to the reference DOF |
| `d_scaled` | Δc × shape (max |d| = 1) |
| `f_push`, `loads` | load pattern |
| `iterations`, `converged`, `final_change` | convergence info |

**`PushoverResult`**:
- fields: `name`, `dofs` (from `ResolvedSystem.dof_table()`), `steps`;
- `n_not_converged`, `curve_rows()`, `shape_rows()`;
- `write(out_dir, system=None, settings=None)`: writes `pushover_curve.csv`, `pushover_shapes.csv` (long
  format: one row per step and DOF) and, if given, copies of the inputs.

Helpers:
- `rows_to_csv(rows, columns)`: floats written with `repr`, i.e. full precision.
- `solver_settings(settings)`: maps settings to `SolverSettings`.
- `CURVE_COLUMNS`, `SHAPE_COLUMNS`: the CSV column orders, also used by the app.

## Design notes

- Output layout is explicit and stable: DOFs carry their kind, position, braced flag and branch index.
  The paper's text files had a different column order per archetype ([legacy_issues.md](../legacy_issues.md),
  C2).
- Steps are independent unless `warm_start` is on, so they could be parallelised. They aren't, because
  a full pushover takes seconds.

## Tests

`tests/test_regression.py` (all archetypes, every value against the paper's files), `tests/test_app.py`.
