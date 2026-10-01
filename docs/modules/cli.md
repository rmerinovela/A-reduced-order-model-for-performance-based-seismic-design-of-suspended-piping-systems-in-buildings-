# `piperom/cli.py`: command-line interface

## Responsibility

Parses command-line arguments, loads inputs, calls the analyses, prints progress and summaries, and writes
results. It contains no analysis logic. User-facing usage: [input_files.md](../input_files.md#command-line).

## Interface

`main(argv: list[str] | None = None) -> int` is the entry point (`python -m piperom`). It returns the process exit
code: 0 on success, 2 on invalid input.

| Command | Calls | Output files |
|---|---|---|
| `check SYSTEM` | `load_system`, `resolve` | — (prints the resolved layout) |
| `pushover SYSTEM` | `pushover.run_pushover` (with a printing progress callback) | `PushoverResult.write` |
| `sdof SYSTEM` | `sdof.derive_sdof` | `SDOFParameters.write` |
| `timehistory SYSTEM` | `derive_sdof` → `SDOFModel.from_parameters` → `timehistory.run_sdof_time_history` per run | `sdof_peaks.csv` + SDOF parameters |
| `verify3d MODEL` | `jobs.verification_job` | `peaks_3d.csv` |

Structure:
- `build_parser()` defines the commands and options.
- Each command is a function `cmd_<name>(args, settings) -> int`, selected through the `COMMANDS` table.
- `main` loads the settings, dispatches, and turns input errors into exit code 2.
- The time-history commands resolve the motion selection (command-line option → settings `motions` →
  defaults) with `motions.select_runs`.
- `verify3d` reports the paper's measure: the largest peak over the braced nodes
  (`verification3d.braced_peaks`).

## Behaviour

- **Precedence:** command-line options > settings file (`--settings`) > `inputs/defaults/settings.yaml`.
- **Default output folder:** `piperom_output/<system name>/<analysis>` (ignored by git).
- **Errors:** `ValueError` (including `InputError` and malformed trapeze files) and `FileNotFoundError` are
  caught and printed as `Input error: …` (exit 2). Numerical failures (`RuntimeError`) propagate with a
  traceback, since they indicate a bug or a non-converging model, not bad input.
- **Analyses run in the calling process** (no worker processes): the CLI runs one analysis at a time, so
  OpenSees' global state is safe.

## Tests

Exercised indirectly by the regression and validation scripts, which call the same functions;
`tests/test_inputs.py` covers the input paths used by `check`.
