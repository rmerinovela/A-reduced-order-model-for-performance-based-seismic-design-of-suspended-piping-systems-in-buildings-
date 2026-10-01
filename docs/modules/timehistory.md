# `piperom/timehistory.py`: SDOF nonlinear time history

## Responsibility

Analyses the equivalent SDOF under a floor acceleration history and reports the response and the
support demands. It's a port of the paper's `NLTHA_SDOF.py`: same model, gravity step, damping,
integrator and fallback sequence.

## Interface

**`SDOFModel`**: what the analysis needs.

| Field | Content |
|---|---|
| `name`, `mass` | identifier and SDOF mass |
| `springs` | `Pinching4` springs acting in parallel |
| `gamma`, `support_phi`, `support_labels` | optional, for support demands |

`SDOFModel.from_parameters(p)` builds it from `SDOFParameters`, longitudinal springs first, as the
paper's script does. Validation builds `SDOFModel`s from the paper's hand-typed scripts
(`validation/legacy.hand_typed_sdof_model`).

**`TimeHistorySettings.from_dict(section)`**: the `sdof_time_history` settings (damping ratio, Rayleigh
factors, convergence test, fallback test parameters), merged with the defaults.

**`run_sdof_time_history(model, motion, settings) -> SDOFResponse`**:

1. Builds the model:
   - nodes 1 (fixed) and 2 (mass in x and y);
   - one Pinching4 per spring, combined into a `Parallel` material;
   - a zeroLength element, rigid in y and rotation.
2. Gravity: 10 load-control steps, then `loadConst`.
3. `eigen(1)` → ω; Rayleigh coefficients from the factors and ω.
4. Path time series of the floor acceleration (`-prependZero`) and a uniform excitation in x.
5. Newmark (0.5, 0.25) transient analysis of all points in one call.
6. On failure, the step-by-step fallbacks, as the paper does:
   - Newton with initial tangent;
   - Broyden;
   - Newton with line search;
   - Krylov–Newton.
7. Displacement and spring force recorded to temporary files and read back.

**`SDOFResponse`**:

| Field | Content |
|---|---|
| `motion`, `record`, `level` | which analysis |
| `period` | SDOF period |
| `time`, `u`, `force` | histories; `u` relative to the floor |
| `completed`, `end_time`, `duration` | analysis status |
| `peak_u` | stored at creation, so it survives when histories are dropped to save memory |

Other functions:
- `sdof_period(model) -> float`: period after the gravity step.
- `support_demands(model, peak_u) -> list[dict]`: per support, peak displacement Γ·φ·u and its ratios to
  the trapeze envelope deformations ePd1–ePd4.

## Side effects and constraints

- Uses OpenSees' global model (`op.wipe()` at start and end) and a temporary directory for recorders.
  Run concurrent analyses in separate processes.
- About 0.3 s per 30 s floor record (30,000 steps).

## Tests

`tests/test_timehistory.py` checks M01x and M01y against the paper's stored SDOF peaks.
`validation/run_timehistory_validation.py` covers every archetype, record and IM1–IM10.
