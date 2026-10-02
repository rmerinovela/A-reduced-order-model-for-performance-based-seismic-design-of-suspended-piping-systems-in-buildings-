# The app

`app/streamlit_app.py` is a Streamlit front end to the whole engine: define a system, run every
analysis, inspect results and download inputs and outputs.

```
source .venv/bin/activate
streamlit run app/streamlit_app.py          # opens http://localhost:8501
```

Use `--server.port 8502` if the port is taken.

## Workflow

```
Sidebar: load a system ─► Geometry ─► Trapezes ─► Settings ─► Pseudo-pushover
                                                            └► SDOF parameters ─► SDOF time history
                                                                                 └► 3D verification
```

Every tab reads the current inputs. Results stay visible after inputs change, with a notice that they
refer to the previous inputs, until the analysis is run again.

## Sidebar

- **Start from:**
  - an archetype (`inputs/archetypes/`) or an example (`inputs/examples/`), then **Load**; or
  - **Upload file**: a system YAML. Files it references can't be resolved, so referenced trapezes fall
    back to the defaults.
- **Settings file:** upload a settings YAML and **Load settings**, or **Default settings**.

## Geometry

- **Main line and pipe properties:**
  - name, description, length, number of pipes;
  - pipe section, material and densities (fluid density defaults to density / 7.8);
  - mass factor and branch participation factor.
- **Hangers:** a regular grid (first, spacing, end clearance) or explicit positions (comma-separated).
- **Transverse braces:**
  - *Select hangers*: tick braced hangers in a table that follows the current hanger list; or
  - *Evenly spaced*: a number of braces, placed as in the paper's `compute_stiff_mask`.
- **Branches:** an editable table (x, length, pipes, longitudinal braces). Add and delete rows freely.
- **Plan view:**
  - main line, gravity hangers and braces;
  - branches drawn to scale, labelled with their longitudinal brace count (branches sharing an x
    alternate sides);
  - the loading direction.
- **Validation:** problems (e.g. a branch on a braced hanger) are reported here and block the analyses.
- **Download inputs:** a zip with `system.yaml`, `settings.yaml` and any custom trapeze CSVs, usable
  directly with the CLI.

## Trapezes

One panel per brace type (transverse, longitudinal):
- **Source:** the default file, an uploaded CSV ("Use uploaded file"), or values edited in the
  parameter table. **Reset to default** restores the file.
- **Plot:** the Pinching4 envelope (both signs) and the trilinear backbone used by the static procedure.
- **Download CSV** of the current definition.

## Settings

| Section | Settings |
|---|---|
| Pseudo-pushover | Δc range or explicit list, warm start |
| Shape iteration and static solver | iterations, tolerances, convergence test; branch-force split (`consistent`, or `legacy` to reproduce the paper's code) |
| Equivalent SDOF | the Δc defining the SDOF |
| SDOF time history | damping ratio, convergence test, tolerance, iterations |
| 3D verification | damping ratio, main and fallback convergence tests and tolerances |

Other entries (Rayleigh factors, fallback iterations) come from the loaded settings file.
**Download settings** saves a YAML.

## Pseudo-pushover

**Run pseudo-pushover** runs all Δc steps, with a progress bar. Then:
- **Capacity curve:** base shear against u_SDOF or Δc. Once SDOF parameters are derived, the SDOF
  backbone is overlaid.
- **Γ and effective-mass ratio** against Δc.
- **Displaced shape** at any Δc (slider), normalised or in mm, with braces and branch DOFs marked; base
  shear, Γ, effective mass and iteration count for that step.
- **Table and downloads:** curve CSV, or a zip with the curve, the shapes and the inputs.

Steps that didn't reach the shape tolerance are reported.

## SDOF parameters

**Derive SDOF parameters** runs the equivalent static procedure at the Settings Δc and shows:
- Γ, effective mass, mass ratio, u_SDOF and base shear;
- the support table (kind, position, φ, number of trapezes, Γ·φ, scaled envelope points);
- the SDOF backbone.

Downloads: `sdof_parameters.yaml` or a zip with the springs CSV and the inputs.

## SDOF time history

Uses the SDOF parameters of the current inputs (derive them here if needed). Choose:
- a motion set (`motions/motion_sets.yaml`) and the floor;
- intensity levels (for sets with levels);
- all records, or a selection.

**Run SDOF time histories** (about 0.3 s per analysis) gives:
- **Peaks plot:** peak support displacement (Γ · max φ · peak u) per record. With several levels it's
  plotted against level, with the median.
- **Results table** and CSV download; analyses that stopped early are flagged.
- **Response history** of any record (batches of up to 100 analyses):
  - SDOF displacement against time;
  - hysteresis loop;
  - support demand table (peak displacement Γ·φ·u and ratio to envelope points ePd1–ePd4).

## 3D verification

For the paper's archetypes (`inputs/models3d/`); defaults to the model matching the loaded system.

**Choose:**
- a motion set with record pairs, an intensity level and a floor;
- the ground motion and its orientation (which component acts in x).

**Run 3D verification:**
- runs the full 3D model under both components;
- runs the reduced-order prediction for each direction (archetype system file, SDOF at the Settings Δc,
  default trapezes) under its component;
- takes about 30 s for M01–M03 and several minutes for the larger models.

**Results:**
- **Comparison table** per direction:
  - 3D peak over all nodes and over the braced nodes (the paper's measure);
  - Γ, max φ, SDOF peak u and the ROM prediction Γ·φ·u;
  - the ratio ROM / 3D.
- **The 3D model's periods.**
- **Plan views** of the recorded nodes, coloured by peak displacement in x and y.
- **Displacement history** of any recorded node, and a CSV of the peaks.

## Running analyses

Analyses run in worker processes (two at a time), never in the web server process. OpenSees keeps
one global model per process, so concurrent sessions or tabs can't interfere. A run can't be cancelled
from the page. A worker that's mid-analysis finishes that analysis even after the app stops, so
after stopping the app during a long 3D run, check for leftover `multiprocessing.spawn` processes.

## Limitations

- Floor motions must be in `motions/` and described in `motion_sets.yaml`; they can't be uploaded.
- 3D verification is limited to the archetypes with a 3D model.
- Results live in the browser session; download what you want to keep.
