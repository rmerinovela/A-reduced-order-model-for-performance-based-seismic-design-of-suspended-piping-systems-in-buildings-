# The paper's original code

`code implementation for paper/` holds the scripts and results used for the paper, unchanged. `piperom`
doesn't read from it; only `validation/` and the tests do, to check that the engine reproduces it.

| Folder | Content |
|---|---|
| `code_proposed_procedure/` | The full procedure of Section 3. `equivalent_static.py` performs the equivalent static procedure to find the displaced shape of a suspended piping system. `NLTHA_SDOF.py` uses that shape to build an equivalent SDOF system and runs nonlinear time-history analyses. |
| `Section2/` | The OpenSees model used in the demonstration of Section 2. |
| `Pushover2D/` | The equivalent static procedure and the adaptive pushover based on it, for all archetypes of the paper (`Functions.py` + one driver per archetype and direction), with their results. |
| `Pushover_SDOF/` | The resulting equivalent SDOF systems (cyclic pushover), with their results. |
| `Results/` | Displacements and displaced shapes of all archetypes (3D and SDOF), and the notebooks comparing them. |
| `3D_models/` | The full 3D models of all archetypes. |
| `trapeze_model_parameters/` | Pinching4 parameters of the transverse and longitudinal trapeze supports (CSV). Copies are the engine's default trapezes (`inputs/trapezes/`). |

Running the scripts as committed needs path changes. They read motions from absolute Windows paths;
`motions/` holds the same data. Known problems, inconsistencies and how `piperom` handles each:
[legacy_issues.md](legacy_issues.md).

Where `piperom` replaces each part:

| Paper code | `piperom` |
|---|---|
| `Pushover2D/Functions.py`, `equivalent_static.py` | `static_model`, `pushover` |
| hand-typed constants in `Pushover_SDOF/*.py` | `sdof` (derived at a chosen Δc) |
| `NLTHA_SDOF.py` | `timehistory` |
| `3D_models/*.py` | `inputs/models3d/*.json` + `verification3d` |
| `trapeze_model_parameters/` | `inputs/trapezes/` + `trapeze` |
