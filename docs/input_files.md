# Inputs: files, command line and app

Units: N, mm, s (masses in tonnes, densities in t/mm³). The engine reads data only from `inputs/` and
`motions/`.

| Input | Format | Location | Required |
|---|---|---|---|
| [Piping system](#system-file) | YAML | anywhere (examples in `inputs/archetypes/`, `inputs/examples/`) | yes |
| [Branch table](#branch-table) | CSV | next to the system file | optional (instead of the list) |
| [Trapeze](#trapeze-files) | CSV | `inputs/trapezes/` (defaults) or anywhere | optional (defaults) |
| [Analysis settings](#settings-file) | YAML | anywhere | optional (defaults) |
| [Floor motions](#floor-motions) | text + `motions/motion_sets.yaml` | `motions/` | for time histories |
| [3D models](#3d-models) | JSON | `inputs/models3d/` | for 3D verification |

Defaults for every optional entry are in `inputs/defaults/system.yaml` and `inputs/defaults/settings.yaml`,
the only place defaults are defined. A user file only needs the entries that differ.

## System file

One file describes one loading direction: a straight main line along x, loaded transversely, and the
branches framing into it, loaded along their axis ([methodology.md](methodology.md)).

```yaml
name: M01x
description: free text

main_line:
  length: 18000            # mm
  n_pipes: 3               # identical pipes in the bundle

pipe:                      # optional; defaults shown
  outer_diameter: 127.0
  inner_diameter: 113.0
  elastic_modulus: 210000.0
  shear_modulus: 81000.0
  density: 7.85e-9         # t/mm³
  fluid_density: null      # null -> density / 7.8 (water in steel pipes)
  mass_factor: 1.35        # multiplier on (pipe + fluid) mass

hangers:                   # gravity hangers: a regular grid ...
  first: 1000
  spacing: 3000
  end_clearance: 1000      # optional: last grid hanger at least this far from the end
# hangers:                 # ... or explicit positions (0 < x < length, increasing)
#   positions: [800, 3500, 6000]

braces:                    # transverse trapezes, always at hangers; exactly one of:
  mask: [0, 1, 0, 1, 0, 1] #   one 0/1 per hanger
# positions: [4000, 10000] #   x of the braced hangers
# count: 3                 #   evenly spaced (length/count, starting at half a spacing), snapped to hangers

branches:                  # at least one; a list ...
  - {x: 18000, length: 36000, n_pipes: 3, n_braces: 4}
# branches: my_branches.csv   # ... or a CSV file (path relative to this file)

branch_participation: 1.0  # optional factor on branch mass and stiffness

trapezes:                  # optional: "default" or a CSV path (relative to this file)
  transverse: default
  longitudinal: default
```

Rules:

- A branch can't be at a braced hanger. It can be at an unbraced hanger or anywhere else on the main
  line (0 ≤ x ≤ length). Several branches can share the same x.
- Branches use the main line's pipe section; only their number of pipes differs.
- The **last branch in the list** is the reference DOF used to normalise the shape.
- At most 299 hangers (OpenSees tag numbering).
- Unknown entries are rejected, so typos don't pass silently.

Provided files:
- `inputs/archetypes/M01x.yaml … M63y.yaml`: the 18 systems of the paper.
- `inputs/examples/equivalent_static_example.yaml`: braces given as a count.
- `inputs/examples/explicit_layout.yaml`: irregular hangers, braces by position, branches from CSV, a
  custom trapeze and non-default pipe properties.

## Branch table

```
x,length,n_pipes,n_braces
12500,15000,2,2
30000,9000,2,1
```

## Trapeze files

These use the format of `inputs/trapezes/pinching4_C-TPS-T.csv`: columns `parameter,value,description`,
with one row per OpenSees Pinching4 parameter. Every name carries the same one-letter prefix (`TePf1`, …,
`TdmgType`; any letter is accepted).

| Parameters | Meaning |
|---|---|
| `ePf1-4`, `ePd1-4` | positive envelope forces (N) and deformations (mm), deformations increasing |
| `eNf1-4`, `eNd1-4` | negative envelope |
| `rDispP/N`, `rForceP/N`, `uForceP/N` | pinching (reloading/unloading) ratios |
| `gK*`, `gD*`, `gF*`, `gE`, `dmgType` | cyclic degradation (`dmgType` = `cycle` or `energy`) |

All braces of one type share the file. The static procedure uses the trilinear envelope through points
2 and 3 (then 1% of the initial slope); the time histories use the full Pinching4.

## Settings file

Optional. Every entry and its default is in `inputs/defaults/settings.yaml`:

```yaml
pushover:
  delta_c_start: 0.1       # mm
  delta_c_stop: 50.0
  n_steps: 50
  delta_c_values: null     # or an explicit list, e.g. [1, 2, 5, 10, 20]
  warm_start: false        # start each step from the previous shape
shape_iteration: {max_iterations: 50, tolerance: 1.0e-3}
static_solver: {test: NormDispIncr, tolerance: 1.0e-8, max_iterations: 50}
equivalent_static:
  branch_split: consistent  # or legacy: the paper code's split of branch forces (docs/legacy_issues.md, A2)
sdof:
  delta_c: 12.0            # Δc defining the equivalent SDOF

motions:                   # default floor-motion selection
  set: S4_IM
  levels: [12]
  records: null            # null = every record of the set
  floor: 4

sdof_time_history:
  damping_ratio: 0.02
  rayleigh: {mass: 0.0, current_stiffness: 1.0, committed_stiffness: 0.0, initial_stiffness: 0.0}
  test: EnergyIncr
  tolerance: 1.0e-8
  max_iterations: 50
  fallback_tolerance: 1.0e-6
  fallback_max_iterations: 100000

verification_3d:
  gravity_steps: 10
  damping_ratio: 0.02
  rayleigh_modes: [1, 2]
  rayleigh: {mass: 1.0, current_stiffness: 0.0, committed_stiffness: 1.0, initial_stiffness: 0.0}
  test: EnergyIncr          # M01-M03 paper scripts use RelativeEnergyIncr, which fails from rest
  tolerance: 1.0e-4
  max_iterations: 500
  fallback_test: EnergyIncr
  fallback_tolerance: 1.0e-3
  fallback_max_iterations: 3000
```

The `rayleigh` entries are factors (0 or 1 in the paper) on the mass and stiffness terms of Rayleigh
damping.

## Floor motions

`motions/motion_sets.yaml` describes each set of floor acceleration files; the engine finds files only
through it.

```yaml
S4_IM:
  description: ...
  file_pattern: floor_motions/ResultsS4/FloorAcc_IM{level}_{record}.txt   # relative to motions/
  records: {file: ground_motions/Names.txt}     # or a list, or {range: [1, 150]}
  record_pairs: true          # consecutive records = two horizontal components of one ground motion
  levels: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]   # or null if the pattern has no {level}
  time_column: 0              # time step = first time value
  floors: {1: 1, 2: 2, 3: 3, 4: 4}   # floor -> column
  to_mm_s2: 1000.0            # file units -> mm/s²
```

| Set | Files | Records | Levels | Used by the paper in |
|---|---|---|---|---|
| `S4_IM` | `floor_motions/ResultsS4/FloorAcc_IM{k}_{name}.txt` | 44 (22 pairs, `ground_motions/Names.txt`) | 1–12 | 3D models; SDOF results (IM1–IM10) |
| `S4_150` | `floor_motions/ResultsS4/FloorAcc_{n}.txt` | 150 | — | `NLTHA_SDOF.py` |

Content of the provided files, checked:
- **Columns:** 5 (time, then floors 1–4); accelerations in m/s².
- **Time step:** `S4_IM` files use the record time step / 10 (`ground_motions/Timesteps.txt`), with
  10 × the ground record length in rows.
- **Ground records:** `ground_motions/Scaled_Records/{name}_Scaled.txt` (single column, presumably g)
  aren't used by the engine.
- **Size:** the floor files total 2.2 GB and aren't tracked by git.

To add motions:
1. Put the files under `motions/`.
2. Add a set to `motion_sets.yaml`.

They then appear in the CLI (`--set`) and the app.

## 3D models

`inputs/models3d/<name>.json` holds the paper's 3D models for the 3D verification:

| Entry | Content |
|---|---|
| `commands` | the OpenSees commands building the model (nodes, materials, elements, constraints, gravity pattern), recorded unchanged from the paper's scripts by `validation/convert_3d_models.py` |
| `node_groups` | nodes recorded in x (`X`) and y (`Y`); braced nodes (`Xt`, `Yt`) |
| `rom_systems` | system files of the x and y directions (`{"x": "M01x", "y": "M01y"}`) |

## Command line

```
python -m piperom check       SYSTEM.yaml
python -m piperom pushover    SYSTEM.yaml [--settings S.yaml] [--out DIR]
python -m piperom sdof        SYSTEM.yaml [--settings S.yaml] [--delta-c MM] [--out DIR]
python -m piperom timehistory SYSTEM.yaml [--settings S.yaml] [--delta-c MM] [--set NAME]
                              [--levels 1,5,10] [--records ID,ID] [--floor N] [--out DIR]
python -m piperom verify3d    MODEL [--settings S.yaml] [--set NAME] [--level N]
                              [--pair K | --records X_ID,Y_ID] [--floor N] [--out DIR]
```

Command-line options override the settings file, which overrides the defaults. Outputs go to
`piperom_output/<name>/...` unless `--out` is given:

| Command | Writes |
|---|---|
| `check` | nothing; prints the resolved hangers, braces, branches and trapezes |
| `pushover` | `pushover_curve.csv` (one row per Δc), `pushover_shapes.csv` (one row per Δc and DOF), `system.yaml`, `settings.yaml` |
| `sdof` | `sdof_parameters.yaml` (Γ, masses, supports with scaled Pinching4), `sdof_springs.csv` |
| `timehistory` | `sdof_peaks.csv` (record, level, peak u, peak support displacement, completed), SDOF parameters |
| `verify3d` | `peaks_3d.csv`; prints the 3D peaks and the ROM prediction per direction |

Exit code 2 means invalid input; the message names the offending entry.

## In the app

See [app.md](app.md):
- **Load a system:** pick an archetype or example, or upload a system YAML.
- **Settings:** upload a settings YAML or use the defaults.
- **Edit:** every input can be edited in the app.
- **Download:** "Download inputs" saves the current inputs as files (system YAML, settings YAML and custom
  trapeze CSVs), ready for the CLI.

Uploaded system files can't reference other files: branch CSVs and trapeze paths aren't resolved.
Upload custom trapezes in the Trapezes tab instead.
