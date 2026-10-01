# `piperom/verification3d.py`: 3D verification models

## Responsibility

Loads the paper's 3D models from `inputs/models3d/*.json` and runs them under a bidirectional floor
motion, with the analysis procedure of the paper's `3D_models` scripts.

## Interface

**`Model3D`**:
- fields: `name`, `description`, `commands` (`[[opensees_command, [args…]], …]`), `node_groups` (`X`, `Y`,
  `Xt`, `Yt`, …), `rom_systems` (`{"x": system, "y": system}`);
- `node_coords()`: node tag → (x, y, z).

Model functions:
- `list_models3d()`, `load_model3d(name)`: `InputError` if missing.
- `model3d_for_system(system_name)`: the 3D model whose `rom_systems` contains the system, or `None`.

**`Verification3DSettings.from_dict(section)`**: gravity steps, damping ratio, Rayleigh modes and factors,
main and fallback convergence tests.

**`build_model3d(model)`**: `op.wipe()`, silences OpenSees, and replays the recorded commands (skipping
`wipe`).

**`run_3d(model, motion_x, motion_y, settings, progress=None, chunk=500) -> Response3D`**:

1. Builds the model.
2. Gravity: load control in `gravity_steps` steps, then `loadConst`.
3. `eigen(4)` for the reported periods.
4. Rayleigh coefficients from the two `rayleigh_modes`.
5. Path series of both components; uniform excitation in x and y.
6. Recorders of the `X` / `Y` node groups every time step.
7. Newmark transient analysis, with the paper's fallbacks (halved, /10 and /20 sub-steps).

The main analysis advances in chunks of `chunk` steps so `progress(fraction)` can report. That's
numerically identical to a single `analyze(n)` call, and switches to the step-by-step fallback loop at
the first failure, as the paper's scripts do.

**`Response3D`**:
- fields: `model`, `record_x`, `record_y`, `level`, `periods`, `time`, `nodes_x`, `nodes_y`, `ux` and `uy`
  (time × node, relative to the floor), `completed`, `end_time`, `duration`;
- `peak_x`, `peak_y`: peak |u| per node.

**`braced_peaks(model, response) -> {"x": float, "y": float}`**: the largest peak over the braced nodes
(`Xt` / `Yt`) per direction. That's the measure stored in the paper's `Results/*_DispX/Y.txt`, used by the
CLI, the app and the validation.

## Design notes

- **Models as data.** The engine never executes the paper's scripts. `validation/convert_3d_models.py`
  runs them once with a recording stand-in for OpenSees and stores the model-building commands verbatim,
  so the models are the paper's and the conversion can be re-run if a script changes.
- **Convergence test.** A setting, defaulting to `EnergyIncr`. The paper's M01–M03 scripts use
  `RelativeEnergyIncr`, which can't converge from rest ([legacy_issues.md](../legacy_issues.md), A6). With
  `EnergyIncr`, the paper's stored 3D results are reproduced.
- **Cost.** One run takes about 30 s (M01–M03) to several minutes (M29–M63); histories of all
  recorded nodes are kept in memory (tens of MB).

## Tests

`tests/test_timehistory.py::test_3d_verification_reproduces_paper` (M01, IM10, both directions);
`validation/run_timehistory_validation.py` (all models).
