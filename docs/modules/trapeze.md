# `piperom/trapeze.py`: trapeze (brace) behaviour

## Responsibility

Single source of truth for brace behaviour:
- reads, validates and writes Pinching4 parameter files;
- converts parameters to and from OpenSees argument lists;
- derives the trilinear secant backbone used by the static procedure.

## Types

**`Pinching4`** (frozen dataclass): all 39 OpenSees Pinching4 parameters, with envelopes stored as
4-tuples.

| Method | Purpose |
|---|---|
| `from_parameters(params, name)` | from an unprefixed dict (`ePf1`, …); checks every parameter is present, numeric and consistent |
| `validate()` | envelope deformations monotonic and of the right sign, forces of the right sign, `dmgType` ∈ {cycle, energy} |
| `parameters()` | inverse of `from_parameters` |
| `opensees_args()` / `from_opensees_args(args)` | the argument list after the tag, in OpenSees order |
| `scaled(force_scale, disp_scale)` | copy with scaled envelope forces and deformations (used for SDOF springs) |
| `to_csv(prefix)` | file in the input format |

**`Trilinear`** (frozen dataclass):

| Member | Meaning |
|---|---|
| `d1`, `d2`, `f1`, `f2` | the two breakpoints |
| `k3_ratio` | third-branch slope as a fraction of `k1` (default `POST_YIELD_STIFFNESS_RATIO` = 0.01) |
| `k1`, `k2`, `k3` | branch stiffnesses (derived) |
| `secant_stiffness(disp)` | F/|d|, the quantity the static procedure uses; identical arithmetic to the paper's `trilinear_keff` |
| `force(disp)` | force at a displacement |

## Functions

- `parse_trapeze_csv(text, name)`: CSV → `Pinching4`. Accepts any single-letter prefix and rejects mixed
  prefixes.
- `load_trapeze(source, kind)`: `None`/`"default"` → the file in `DEFAULT_TRAPEZE_FILES[kind]`
  (`inputs/trapezes/`); a path → that file; a `Pinching4` passes through.
- `trilinear_from_pinching4(p)`: envelope points 2 and 3 of the positive envelope.

## Design notes

- Envelope point 1 (e.g. 600 N at 0.1 mm) isn't part of the trilinear. That matches the paper.
- The 1% post-yield ratio is a modelling constant of the paper, kept as a named module constant rather
  than a user input.
- `Pinching4` is immutable and hashable, so it can be passed to worker processes and compared by value
  (the app compares against the default to detect custom trapezes).

## Tests

`tests/test_inputs.py`:
- CSV round-trip and prefix independence;
- missing or inconsistent parameters;
- trilinear constants equal to the paper's transverse values;
- custom files changing results.

`tests/test_timehistory.py` checks the OpenSees argument round-trip.
