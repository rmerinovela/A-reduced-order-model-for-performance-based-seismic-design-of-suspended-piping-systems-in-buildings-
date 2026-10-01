# `piperom/jobs.py`: analyses as process-safe jobs

## Responsibility

Entry points that bundle a complete analysis into one picklable function call, so callers can run it in a
worker process. The app runs analyses through them; `cli verify3d` uses `verification_job` directly.

OpenSeesPy keeps a single global model per Python process. A web server serving several sessions from
threads would otherwise let concurrent analyses overwrite each other's models.

## Interface

All jobs take picklable arguments (dataclasses, strings, numbers) and an optional `queue`. Progress
messages are `(k, n)` tuples: step k of n, or a fraction `(f, 1.0)` for the 3D analysis.

| Job | Does | Returns |
|---|---|---|
| `pushover_job(system, settings, queue=None)` | `pushover.run_pushover` | `PushoverResult` |
| `sdof_job(system, settings, delta_c)` | `sdof.derive_sdof` | `SDOFParameters` |
| `sdof_time_history_job(model, set_name, runs, floor, settings, queue=None)` | one `run_sdof_time_history` per `(record, level)` | `list[SDOFResponse]`; histories dropped when there are more than `MAX_STORED_HISTORIES` (100) runs |
| `verification_job(model_name, set_name, record_x, record_y, level, floor, settings, queue=None)` | for each direction: archetype system → `derive_sdof` (settings Δc) → SDOF time history under that direction's component; then `run_3d` | `VerificationResult` |

Result types:
- **`VerificationResult`**: `response` (`Response3D`) and `rom` (`{"x": RomPrediction, "y": …}`).
- **`RomPrediction`**:
  - `system`, `record`, `gamma`, `phi_max` (max φ over the supports), `peak_u`, `completed`;
  - `peak_support_displacement` = Γ·φ_max·u_peak, the quantity compared with the 3D model.

## Usage pattern (as in the app)

```python
from concurrent.futures import ProcessPoolExecutor
import multiprocessing as mp

ctx = mp.get_context("spawn")
pool, manager = ProcessPoolExecutor(2, mp_context=ctx), ctx.Manager()
q = manager.Queue()
future = pool.submit(pushover_job, system, settings, q)
while not future.done():
    k, n = q.get()          # update a progress bar
result = future.result()
```

## Design notes

- Jobs resolve inputs themselves (motion sets, 3D models, archetype systems) from names, so only small
  arguments cross the process boundary.
- The ROM prediction inside `verification_job` always uses the archetype system file of each direction
  and the default trapezes, independent of what's loaded in the app, so it's a like-for-like comparison
  with the paper's models.
