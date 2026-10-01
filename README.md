# A reduced-order model for performance-based seismic design of suspended piping systems in buildings

Data and code in support of the publication "A reduced-order model for performance-based seismic design
of suspended piping systems in buildings", by Roberto J. Merino, Roberto Gentile and Carmine Galasso.

The repository contains:
- **the paper's original code and results**, unchanged, in `code implementation for paper/`;
- **`piperom`**, a reusable engine and web app implementing the same reduced-order model with
  file-based inputs. It's validated against the paper's code and results.

## Quick start

Requires Python 3.12 (tested on macOS arm64).

```bash
python3.12 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# command line: pushover and SDOF of a paper archetype
python -m piperom pushover inputs/archetypes/M01x.yaml      # → piperom_output/M01x/pushover/
python -m piperom sdof     inputs/archetypes/M01x.yaml --delta-c 12

# web app
streamlit run app/streamlit_app.py                          # → http://localhost:8501
```

The time-history analyses also need the floor motions in `motions/floor_motions/` (2.2 GB, not in git).
Then:

```bash
python -m piperom timehistory inputs/archetypes/M01x.yaml --levels 1,5,10
python -m piperom verify3d M01 --level 10 --pair 0
```

Checks: `pytest`, `python validation/run_validation.py`, `python validation/run_timehistory_validation.py`.

## Documentation

All documentation is in [`docs/`](docs/).

| Document | Summary |
|---|---|
| [Methodology](docs/methodology.md) | **What the engine computes.** A system file describes one loading direction: a straight main line on gravity hangers, transverse trapezes at chosen hangers, and orthogonal branches lumped into one DOF each. The engine runs (1) the iterative equivalent static procedure at a target displacement Δc, (2) an adaptive pseudo-pushover over a Δc range, (3) the equivalent SDOF at a chosen Δc (effective mass, Pinching4 springs scaled by Γ·φ), (4) SDOF nonlinear time histories under floor motions, with support demands, and (5) a verification against the paper's full 3D models. Also covers scope, limits and validation status. |
| [Software architecture](docs/architecture.md) | **How the code is organised.** Data layer (`inputs`, `trapeze`, `motions`), model layer (`static_model`, OpenSees), analysis layer (`pushover`, `sdof`, `timehistory`, `verification3d`), interfaces (`cli`, `jobs`, app). The engine reads only `inputs/` and `motions/`; defaults are defined once; the port is exact and regression-tested; OpenSees runs in worker processes for the app. |
| [Modules](docs/modules/) | **One file per `piperom` module:** [package](docs/modules/package.md) · [cli](docs/modules/cli.md) · [inputs](docs/modules/inputs.md) · [trapeze](docs/modules/trapeze.md) · [static_model](docs/modules/static_model.md) · [pushover](docs/modules/pushover.md) · [sdof](docs/modules/sdof.md) · [timehistory](docs/modules/timehistory.md) · [motions](docs/modules/motions.md) · [verification3d](docs/modules/verification3d.md) · [jobs](docs/modules/jobs.md). Responsibility, interface, design notes and tests of each. |
| [Inputs](docs/input_files.md) | **How to provide inputs, from the CLI and the app.** System YAML (hangers as grid or positions; braces as mask, positions or count; branches as list or CSV), trapeze CSV (Pinching4 format), settings YAML (all defaults in `inputs/defaults/`), the floor-motion catalogue `motions/motion_sets.yaml`, 3D model files; every CLI command and its outputs. |
| [App](docs/app.md) | **The web app, tab by tab.** Load or upload a system, edit geometry and trapezes with a plan view, adjust settings, run the pseudo-pushover, derive the SDOF, run SDOF time histories over chosen motion sets, levels and records, and run the 3D verification against the reduced-order prediction. Inputs and results can be downloaded. |
| [Validation](docs/validation.md) | **The engine against the paper's code and results.** Pseudo-pushover of all 18 archetypes identical to the paper's files (49,050 values); SDOF parameters identical to the paper's procedure; SDOF time histories match for 14 of 18 SDOFs (M61/M62 results can't be traced to any SDOF in the repository); 3D verification reproduces the paper's 3D results. How to rerun every check. |
| [Paper code](docs/paper_code.md) | The contents of `code implementation for paper/` and what replaces each part in `piperom`. |
| [Known issues of the paper code](docs/legacy_issues.md) | Bugs and inconsistencies found in the original scripts, and how `piperom` handles each. |

## Repository layout

```
code implementation for paper/   original scripts and results (reference only)
inputs/                          engine inputs: defaults, trapezes, archetypes, examples, 3D models
motions/                         floor motions and their catalogue (motion_sets.yaml)
piperom/                         engine (Python package, CLI: python -m piperom)
app/                             Streamlit app
validation/                      comparison with the paper (reports, 3D model converter)
tests/                           pytest suite
docs/                            documentation
```
