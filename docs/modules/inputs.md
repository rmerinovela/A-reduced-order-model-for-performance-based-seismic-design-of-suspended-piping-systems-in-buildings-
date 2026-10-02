# `piperom/inputs.py`: system and settings definitions

## Responsibility

Turns user input (YAML files, CSV files or dictionaries from the app) into **validated, typed objects**:
- the piping system of one loading direction;
- the analysis settings.

It's the only module that applies defaults (from `inputs/defaults/*.yaml`) and the only place where
input validation rules live. File format reference: [input_files.md](../input_files.md).

## Main types

| Type | Role |
|---|---|
| `InputError(ValueError)` | every invalid-input condition; the message names the offending entry |
| `PipeProperties` | pipe section, material, densities, mass factor; `effective_fluid_density` applies the `density / 7.8` rule |
| `Branch` | `x`, `length`, `n_pipes`, `n_braces` |
| `PipingSystem` | the system **as specified**: hangers as a grid *or* positions, braces as mask *or* positions *or* count, trapezes as `"default"`, a path or a `Pinching4` |
| `ResolvedSystem` | the system **as analysed**: numpy arrays of hanger x, brace mask, branch data, plus loaded `Pinching4` and derived `Trilinear` for each trapeze type |
| `AnalysisSettings` | pushover, shape-iteration, static-solver, branch-split and SDOF settings as typed fields; the `motions`, `sdof_time_history` and `verification_3d` sections as dictionaries, parsed by their modules |

## Lifecycle

```
YAML ──load_system──► PipingSystem.from_dict ──(deep_merge with defaults, key/number checks)──► PipingSystem
PipingSystem.resolve() ──(geometry rules, trapeze loading)──► ResolvedSystem ──► analyses
PipingSystem.to_dict() / to_yaml() ──► YAML (round-trips through from_dict)
```

`PipingSystem` stays close to the user's input, so the app can edit it and write it back. `ResolvedSystem`
is immutable in practice and is what every analysis consumes. `resolve()` is cheap and is called again
whenever an analysis starts.

## Key functions

- `load_system(path)`: reads YAML. Relative paths inside it (branch CSV, trapeze CSVs) resolve against the
  file's folder.
- `load_settings(path=None)` / `AnalysisSettings.from_dict(data)`: defaults merged with user values;
  `delta_c()` returns the Δc array.
- `PipingSystem.hanger_x()`: hanger positions. Grid mode reproduces the paper code exactly, including the
  end-clearance rule. Coordinates are rounded to 1e-6 mm.
- `PipingSystem.brace_mask_array(hanger_x)`: converts any brace definition to a 0/1 mask.
- `evenly_spaced_brace_mask(hanger_x, length, count)`: port of the paper's `compute_stiff_mask`, applied to
  the model's own hanger list.
- `read_branches_csv(text)`, `deep_merge(base, override)`, `dump_yaml(data)`: helpers. `dump_yaml` writes
  numpy values and integral floats as plain YAML.
- `check_keys`, `parse_number`, `read_yaml`, `parse_rayleigh`: validation helpers, also used by
  `timehistory` and `verification3d` so all settings are validated the same way.

## Validation rules enforced by `resolve()`

- Hangers: at least one, strictly increasing, strictly inside the main line; at most `MAX_HANGERS` (299).
- Brace mask length = number of hangers; brace positions must be hangers; count ≤ hangers.
- At least one branch, at most `MAX_BRANCHES`, each on the main line and not within 1e-2 mm of a braced
  hanger.
- Inner diameter smaller than outer diameter; all lengths, counts and moduli positive; NaN treated as
  missing.
- Unknown keys anywhere are rejected.

## Design notes

- Defaults come only from the YAML files, so the dataclasses have no default values for user-facing
  entries. Changing a default means editing one file.
- `to_dict()` writes custom `Pinching4` trapezes as `custom_<kind>.csv`. The app saves those CSVs next to
  the system file in its downloads.

## Tests

`tests/test_inputs.py`:
- equivalent definitions give identical models (grid vs positions; mask vs positions vs count; list vs
  CSV branches);
- every validation error;
- YAML round-trips of all archetypes;
- settings overrides.
