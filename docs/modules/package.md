# `piperom/__init__.py` and `piperom/__main__.py`

## Responsibility

`__init__` defines the package-wide **paths**, the only place where the engine's data locations are set.
`__main__` makes the package executable (`python -m piperom …`) by delegating to `cli.main`.

## Constants

| Name | Value | Used by |
|---|---|---|
| `PACKAGE_DIR` | `piperom/` | — |
| `REPO_DIR` | repository root | `motions` (motions folder) |
| `INPUTS_DIR` | `inputs/` | `jobs` (archetype systems), `verification3d` (3D models) |
| `DEFAULTS_DIR` | `inputs/defaults/` | `inputs`, `timehistory`, `verification3d` |
| `TRAPEZES_DIR` | `inputs/trapezes/` | `trapeze` |
| `__version__` | `"0.1.0"` | — |

## Invariants

- The engine reads data only below `INPUTS_DIR` and `REPO_DIR / "motions"`. Changing these constants
  relocates every data dependency at once.
- Importing the package has no side effects: no file access, no OpenSees calls.
