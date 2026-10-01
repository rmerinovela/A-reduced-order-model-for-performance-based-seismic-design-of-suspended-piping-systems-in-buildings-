# Validation against the paper's code and results

This file records how `piperom` was checked against the paper's scripts and stored results
(`code implementation for paper/`), what matches, and what can't be reproduced. Results are regenerated
by the scripts in `validation/`; the tables below summarise them.

| Part of the engine | Reference | Sample | Result |
|---|---|---|---|
| [Pseudo-pushover](#1-equivalent-static-procedure-and-pseudo-pushover) | `Pushover2D/pushover_results_*.txt` | 18 archetypes × 50 Δc, every stored value | **identical** at the stored precision |
| [SDOF parameters](#2-equivalent-sdof-parameters) | `equivalent_static.py` → `NLTHA_SDOF.py` | the scripts' example system | **identical** (relative difference 0) |
| [SDOF parameters](#hand-typed-sdof-constants) | constants typed into `Pushover_SDOF/*.py` | 18 SDOFs | only partly consistent with the 2D results (paper-side issue) |
| [SDOF time history](#3-sdof-time-history) | `Results/<M>_peak_displacements.npy` | 18 SDOFs × 4 records × IM1–IM10 | **14 SDOFs match** (median 0, max 0.5%); M61x/y, M62x/y don't (paper-side issue) |
| [3D verification](#4-3d-verification) | `Results/<M>_biron_DispX/Y.txt` | 9 models × 1 ground motion × 2 orientations at IM10 | see [§4](#4-3d-verification) |

## How to reproduce

| Command | Covers | Output | Time* |
|---|---|---|---|
| `pytest` | regressions, inputs, time histories (M01), app | — | ~6 min |
| `python validation/run_validation.py` | §1–2 | `validation/report.md` | ~3 min |
| `python validation/run_timehistory_validation.py [--only sdof\|3d]` | §3–4 | `validation/timehistory_report.md` | SDOF ~5 min; 3D up to ~1 h |

\* On the development machine (10 cores). The run times written into the reports depend on machine
load.

Helpers in `validation/legacy.py`:
- **Paper result readers:** load the paper's stored results.
- **`capture_opensees_calls`:** runs a paper script with a recording stand-in for OpenSees. It's used to
  read the hand-typed SDOFs, and by `convert_3d_models.py` to extract the 3D models, without executing
  any analysis.
- **`legacy_static_C-TPS-L.csv`:** the longitudinal trapeze with the value the paper's static code
  actually used ([§1](#1-equivalent-static-procedure-and-pseudo-pushover)).

## 1. Equivalent static procedure and pseudo-pushover

**Method.** Each archetype file in `inputs/archetypes/` was generated from its paper driver
(`Pushover2D/CS_Lumped_Iter_<M>_cont_PO.py`). `piperom` runs it with the default settings, which equal
the drivers' settings. Every value of the paper's result file is compared after formatting the new
value with 3 decimals, as the paper's files were written:
- Δc, Γ, M_eff, V_b, mass ratio, u_SDOF;
- for every DOF: normalised shape, scaled shape and load pattern.

The two drivers that sort their DOF columns (M30y, M62y) are compared after the same sorting.

**Input used.** The paper's static code hard-codes a longitudinal backbone point of 11500 N at 24 mm.
The paper's trapeze file has 10000 N there ([legacy_issues.md](legacy_issues.md), A1). The comparison
therefore uses `validation/legacy_static_C-TPS-L.csv`, which differs from the file only in that value.
`piperom`'s default stays the file as published.

**Result.** All **49,050 values** of the 18 files are identical. The largest raw difference is 5.0e-4, the
rounding of the stored values.

| Archetypes | Values compared | Differing |
|---|---|---|
| M01x–M03y (6) | 10,800 | 0 |
| M29x–M31y (6) | 15,300 | 0 |
| M61x–M63y (6) | 22,950 | 0 |

**Effect of the published trapeze file** (default inputs): base shears 4–18% lower than the paper's
static results, Γ almost unchanged. Per-archetype values: `validation/report.md` §4.

## 2. Equivalent SDOF parameters

**Against the paper's procedure.** `code_proposed_procedure/equivalent_static.py` was run unchanged
(Δc = 12 mm), and its output compared with `piperom sdof` on `inputs/examples/equivalent_static_example.yaml`.
That file defines the same system, with braces given as `count: 4`.

| Quantity | Relative difference |
|---|---|
| brace placement (`compute_stiff_mask`) | identical mask |
| Γ, effective mass, u_SDOF | 0 |
| full displaced shape, support shape (`DispShape`) | 0 |
| scaled Pinching4 envelope of every spring (as built by `NLTHA_SDOF.py`) | < 1e-12 |

### Hand-typed SDOF constants

The SDOF scripts in `Pushover_SDOF/` hold Γ, mass and support shape typed by hand. Comparing them with
the 2D results (`validation/report.md` §3):

| Finding | Archetypes |
|---|---|
| Γ and shape match a pushover step, each at a different, unrecorded Δc | M01y, M02x, M02y, M03y, M63x, M63y |
| shape matches but Γ doesn't | M01x |
| no step matches | M03x, M29y, M30y, M31y, M61x, M61y, M62x, M62y |
| rigid-body SDOF with 15 transverse braces absent from the 2D model | M29x, M30x, M31x |
| typed mass vs 2D effective mass | always 1–12% lower |
| typed longitudinal brace count ≠ 2D model | M30x, M61x, M62x, M63x |

`piperom sdof` replaces these constants with values derived at a user-chosen Δc. The hand-typed SDOFs
are still used in §3, because they're what produced the paper's SDOF results.

## 3. SDOF time history

**Method.** Each SDOF defined in `Pushover_SDOF/<M>_SDOF.py` (mass and springs exactly as typed, read
with `capture_opensees_calls`) is analysed by `piperom.timehistory` with the default settings, which
follow `NLTHA_SDOF.py`. The sample is the first 4 records of `S4_IM` (two ground motions, both
components) at IM1–IM10. Peaks are compared with `Results/<M>_peak_displacements.npy`.

**What the paper's arrays are** (established by this comparison):
- columns = IM1–IM10;
- rows = the 44 records in `Names.txt` order;
- values = peak SDOF displacement.

| SDOF | Values | Median rel. diff. | Max rel. diff. |
|---|---|---|---|
| M01x, M01y | 40 each | 0 | 4.1e-4 |
| M02x, M02y | 40 each | 0 | 5.1e-3 |
| M03x, M03y | 40 each | 0 | 1.7e-4 |
| M29x, M29y | 40 each | 0 | 3.7e-4 |
| M30x, M30y | 40 each | 0 | 8.5e-4 |
| M31x, M31y | 40 each | 0 | 1.4e-3 |
| M63x, M63y | 40 each | 0 | 8.4e-6 |
| **M61x** | 40 | 8.1e-2 | 4.2e-1 |
| **M61y** | 40 | 3.9e-2 | 3.8e-1 |
| **M62x** | 40 | 2.0e-1 | 4.1e-1 |
| **M62y** | 40 | 1.0e-1 | 4.5e-1 |

**Matching SDOFs (14 of 18).** The engine reproduces the paper's results: most values are identical,
and none differs by more than 0.5%.

**M61x, M61y, M62x, M62y.** The paper's peaks don't come from the committed SDOF scripts. They don't
come from SDOFs derived from the 2D model at any Δc either (tested from 0.1 to 50 mm: off by a factor of
6–8). The SDOF definitions behind them aren't in the repository ([legacy_issues.md](legacy_issues.md),
A7). This is a gap in the paper's data, not an engine issue: the same engine reproduces the other 14
SDOFs exactly.

`tests/test_timehistory.py` checks M01x and M01y on every test run.

## 4. 3D verification

**Method.** The 3D models in `inputs/models3d/` were extracted from the paper's `3D_models/<M>_biron.py`
by recording their OpenSees commands; nothing in the models was changed. Each model is analysed by
`piperom.verification3d` with the default settings at IM10, under the first ground motion
(records 120111 / 120112) in both orientations.

The compared quantity is the paper's: the largest peak displacement over the braced nodes, per
direction. Row r of `DispX`/`DispY` is the index in `Names.txt` of the record applied in that direction.

**Convergence test.** The paper's M01–M03 scripts use `RelativeEnergyIncr`, which fails at the first time
step from rest. The engine uses `EnergyIncr`, as M29–M63 do ([legacy_issues.md](legacy_issues.md), A6).

| Model | x / y records | x: engine / paper (mm) | y: engine / paper (mm) |
|---|---|---|---|
| M01 | 120111 / 120112 | 11.770 / 11.77 | 15.837 / 15.84 |
| M01 | 120112 / 120111 | 16.330 / 16.33 | 11.449 / 11.45 |
| M02 | 120111 / 120112 | 16.937 / 16.93 | 23.111 / 23.11 |
| M02 | 120112 / 120111 | 458.072 / 458.07 | 14.603 / 14.60 |
| M03 | 120111 / 120112 | 526.719 / 526.72 | 260.188 / 260.19 |
| M03 | 120112 / 120111 | 259.647 / 259.65 | 490.881 / 490.88 |
| M29 | 120111 / 120112 | 11.159 / 11.16 | 11.574 / 11.57 |
| M29–M63 (other runs) | | pending | pending |

The engine reproduces the paper's 3D results to the precision stored (2 decimals). That includes runs
where trapezes reach their failure cap and displacements exceed 250 mm (M02, M03). It also shows that
the paper's M01–M03 results were produced with `EnergyIncr`, not with the committed `RelativeEnergyIncr`.

`tests/test_timehistory.py` checks M01 on every test run.

## What isn't validated

- **SDOF cyclic pushover** (`Pushover_SDOF/Results*/*_CPO.out`): the engine doesn't run cyclic SDOF
  pushovers. The paper's scripts were re-run and reproduce their own committed outputs.
- **`NLTHA_SDOF.py` with the 150-record set:** the script can't run as committed, and no results of it
  are stored.
- **`Section2/`** (demonstration model) and **the notebooks** in `Results/`: not part of the engine.
- **Time histories on the full motion set:** §3 and §4 use samples (4 records and 1 ground motion). The
  scripts run the full set with larger `RECORDS` or more pairs, at higher cost.
