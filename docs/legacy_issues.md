# Known issues in the original scripts

The scripts are kept unchanged in `code implementation for paper/`; paths below are relative to that folder. This file lists what was found while reimplementing them in `piperom`.
"Handled in piperom" says how the new code deals with each issue. Results-changing items are kept
consistent with the scripts unless stated.

## A. Errors that change results

| # | Where | Issue | Handled in piperom |
|---|---|---|---|
| A1 | `Pushover2D/Functions.py:43`, `code_proposed_procedure/equivalent_static.py:87` | The static procedure's longitudinal trilinear uses **11500 N at 24 mm**. The Pinching4 parameters (CSV, SDOF scripts, 3D models) have **10000 N at 24 mm** (11500 N is at 61 mm). The transverse values agree. | The trilinear is derived from the CSV files, so defaults use 10000 N. The legacy value is in `validation/legacy_static_C-TPS-L.csv`. Effect: base shear 4–18% lower (`validation/report.md` §4). **Decision needed.** |
| A2 | `Functions.py:630-830`, `equivalent_static.py:670-870` | Branch force split: the "stay" share includes the main-line junction mass in its denominator; the "pass" share excludes it (line 788 commented out). Stay + pass ≠ branch force, so applied loads and the reported base shear don't equal the support reactions implied by the shape. | **Fixed** (default `equivalent_static.branch_split: consistent`): the junction node mass is part of the main-line share, so stay + pass = branch force. `branch_split: legacy` reproduces the paper's code and is used by the validation. Effect on the capacity curves: `validation/report.md` §4. |
| A3 | `NLTHA_SDOF.py:193` | Longitudinal strength per branch = `nL / n_ortho`, while the static model gives every branch its own `n_braces`. Wrong for more than one branch; the hand-made M61y SDOF uses per-branch counts instead. | `sdof` uses each branch's `n_braces`. |
| A4 | `Pushover_SDOF/*.py` | The hand-typed SDOF constants aren't consistently derived from the 2D pushover results: | `piperom sdof` derives them from the inputs at a user-given Δc. |
|    | | • The Δc each set corresponds to varies by archetype (0.1–45 mm) and isn't recorded. | |
|    | | • The mass is 1–12% below the effective mass of the 2D model. | |
|    | | • Shapes of M01x, M03x, M29y–M31y and M61x–M62y match no step of the current 2D results (probably an earlier code version). | |
|    | | • M29x–M31x are rigid-body SDOFs (shape = 1) with 15 transverse braces their 2D model doesn't have. | |
|    | | • nL differs from the 2D model in M30x (2 vs 3), M61x (9 vs 4), M62x (8 vs 4) and M63x (6 vs 3). | |
|    | | • M62y and M63y use one longitudinal material with the total nL and the φ of the last branch only, ignoring the other branch (φ = 0.69 vs 1.0 in M63y). | |
|    | | See `validation/report.md` §3. | |
| A5 | `Pushover_SDOF/*.py:238,246,254` | Fallbacks call `op.analyze(1, dsteps/2)` in a **static** analysis, where the second argument is ignored, so the smaller step is never used. After a fallback the test also switches from `EnergyIncr` to `RelativeEnergyIncr` for the rest of the analysis. | Not applicable (SDOF analysis not implemented yet). |
| A6 | `3D_models/M01-M03_biron.py` (transient analysis) | The convergence test `RelativeEnergyIncr` (1e-4) never converges from rest: the first time step fails, every fallback fails, and the run stops at t ≈ 0.002 s. Same with OpenSees 3.4.0 and 3.8.0. M29–M63 use `EnergyIncr` for the main test, but their fallbacks mix the two types. With `EnergyIncr` the paper's `Results/` are reproduced (`validation/timehistory_report.md`), so the committed M01–M03 scripts aren't the ones that produced them. | The 3D test type is a setting, default `EnergyIncr` (1e-4, 500 iterations; fallback 1e-3, 3000). |
| A7 | `Pushover_SDOF/M61*_SDOF.py`, `M62*_SDOF.py` vs `Results/M61_*`, `M62_*` | The paper's SDOF peak displacements for M61x, M61y, M62x and M62y aren't reproduced by the SDOFs typed into these scripts: median difference 4–20%, up to 45%. They aren't reproduced by SDOFs derived from the 2D model at any Δc either. The other 14 SDOFs reproduce the paper (median difference 0). The SDOF definitions behind the M61/M62 results aren't in the repository. | Reported in [validation.md](validation.md). |

## B. Crashes and dead code paths

| # | Where | Issue | Handled in piperom |
|---|---|---|---|
| B1 | `NLTHA_SDOF.py:72` | `nT`, `nL` used before definition (`nt = 4` on line 68 is a different variable): `NameError`. | n/a |
| B2 | `Functions.py:702-714`, `equivalent_static.py:742-754` | `seg_bounds`, `x_d`, `d_d`, `Fy_full` are only defined inside `for j in range(n_orth)`: a system **without branches** crashes. `d_all / d_all[-1]` also assumes the last DOF is a branch. | Clear input error: at least one branch is required. |
| B3 | `Functions.py:448` | A branch with zero length, pipes or braces (or `alpha <= 0`) is skipped, leaving `None` in the node list: `int(None)` crashes later. | Input validation rejects these values. |
| B4 | `equivalent_static.py:9-44` | `compute_stiff_mask` builds its own hanger list without the 1 m end clearance used by `build_model`. For some length/first/spacing combinations the mask length doesn't match the hangers, e.g. L = 37000, first = 1000, spacing = 3000: 13 vs 12. | Uses the model's hanger list. |
| B5 | `Functions.py` (tags) | Node/element tags overlap above ~300 hangers: main nodes `100+i` vs hanger tops `400+i`; hanger elements `700+i` vs beams `1000+i`. | Limit checked (299 hangers). |
| B6 | `Functions.py:1057-1077` | `iterate_shape_from_static` calls `build_model` once before the loop and discards the result. | Removed (results unchanged). |
| B7 | `Pushover2D/CS_*.py:116` | `d_init_current` is updated but `d0` is always passed, so every Δc step restarts from a uniform shape. | `warm_start` setting, default `false` as in the scripts. |

## C. Input/output and portability

| # | Where | Issue |
|---|---|---|
| C1 | `NLTHA_SDOF.py:346`, `3D_models/M01-M03`, `Results/*.ipynb` | Hard-coded `C:/Users/rmeri/...` paths. M29–M63 read `Names.txt`, `Timesteps.txt` and `ResultsS4/` relative to the working directory. The motions are now in `motions/` (see [input_files.md](input_files.md#floor-motions)); the scripts still need path changes to find them. |
| C2 | `Pushover2D/CS_*.py` | Output column order is inconsistent. Only M30y and M62y sort DOFs by position; M29y and M31y (same layout) write DOF order (hangers, then branches in input order). |
| C3 | `equivalent_static.py:1301`, `NLTHA_SDOF.py:72` | Hand-off through `Results/EquivStatic` relative to the working directory: both scripts must run from the same folder, and from the repo root they write into the data folder `Results/`. |
| C4 | `Functions.py:127-130, 874-892` | Debug prints on every iteration. `equivalent_static.py` duplicates `Functions.py`. |
| C5 | `Section2/ContinuousSystem_3DOF.py` | `vfo` 0.0.19 fails with numpy ≥ 2 when plotting (the model runs). |
| C6 | `Pushover_SDOF/Results*/*.out` | Committed with Windows line endings. The values are identical to a re-run. |
| C7 | `Results/*_DispX.txt`, `*_DispY.txt` | Undocumented. Determined: largest peak displacement over the braced nodes (`nodesXt` / `nodesYt`); row = index in `Names.txt` of the record applied in that direction; columns = IM1–IM10. `*_peak_displacements.npy`: SDOF peak displacement, same rows and columns. |
| C8 | `NLTHA_SDOF.py:346` | Reads 150 records from `.../Surrogate_Modelling/RCFrames/ResultsS4/`. The provided `motions/floor_motions/ResultsS4/` contains `FloorAcc_1`–`150.txt` with the same names and layout; that they're the same set is assumed, not verified. |

## D. Worth checking (possibly intentional)

| # | Where | Observation |
|---|---|---|
| D1 | `3D_models/*.py:316-317` | `MinMax` caps: longitudinal ±35 mm (envelope extends to 61 mm), transverse ±60 mm (envelope ends at 36 mm). They look swapped. |
| D2 | `Results/M01_biron.ipynb` cell 22 | `np.flip(POx[:,6:13])` flips **both** axes, so `Dstaticx[10]` is pushover row 39 (Δc ≈ 39.8 mm), not row 10. |
| D3 | `Results/M01_biron.ipynb` cells 9 and 11 | x-direction scaling uses Γ·φ = 0.92·1.14 in one plot and 0.92·1.216 in the error plot. |
| D4 | `NLTHA_SDOF.py` vs `3D_models` | Different damping models: 2% stiffness-proportional (current K) for the SDOF; mass + committed-K Rayleigh (modes 1–2) for the 3D benchmark. |
| D5 | `NLTHA_SDOF.py:285-290` | "Gravity" load `Meff*9805` applied upward in DOF 2, which is rigid (no effect). The run always prints "Floor Motion Done" even if it failed. |
| D6 | `Functions.py:93`, docstrings | `trilinear_keff` returns the **secant** stiffness; comments call it "tangent". |
