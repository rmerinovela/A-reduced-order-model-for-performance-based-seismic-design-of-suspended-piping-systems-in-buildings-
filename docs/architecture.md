# Software architecture

## Repository layout

```
inputs/                     everything the engine reads (besides motions)
├── defaults/                 system.yaml, settings.yaml: the only place defaults are defined
├── trapezes/                 default trapeze files (Pinching4 CSV)
├── archetypes/               the 18 system files of the paper (M01x … M63y)
├── examples/                 example system files
└── models3d/                 the paper's 3D models as data (JSON)
motions/                    floor motions + motion_sets.yaml (catalogue); large files not in git
piperom/                    the engine (Python package)
app/streamlit_app.py        web app
validation/                 comparison with the paper's code and results; 3D model converter
tests/                      pytest suite
docs/                       this documentation
code implementation for paper/   the paper's original scripts and results (unchanged, reference only)
```

## Layers

```
          ┌──────────────────────┐      ┌───────────────────────────┐
 users ──►│  CLI  (piperom.cli)  │      │  App (app/streamlit_app)  │◄── users
          └──────────┬───────────┘      └─────────────┬─────────────┘
                     │                                 │ worker processes (piperom.jobs)
                     ▼                                 ▼
          ┌────────────────────────────────────────────────────────────┐
          │ analyses: pushover · sdof · timehistory · verification3d   │
          │ model:    static_model (OpenSees, equivalent static step)  │
          │ data:     inputs · trapeze · motions                       │
          └───────────────────────────────┬────────────────────────────┘
                                          │ reads only
                         ┌────────────────┴────────────────┐
                         ▼                                 ▼
                     inputs/                           motions/
```

- **Data layer** (`inputs`, `trapeze`, `motions`). Parses and validates files into typed objects. It's the
  only code that touches `inputs/` and `motions/`; it never runs OpenSees.
- **Model layer** (`static_model`). One OpenSees analysis of the reduced model, and the shape iteration.
- **Analysis layer** (`pushover`, `sdof`, `timehistory`, `verification3d`). Procedures built on the model
  layer, plus result objects that write their own CSV/YAML.
- **Interfaces** (`cli`, `jobs`, the app). Turn user requests into analysis calls. `jobs` wraps analyses so
  they can run in worker processes.

## Module dependencies

```
inputs ◄── trapeze
  ▲   ▲
  │   └──────── motions
  │                ▲
static_model       │
  ▲                │
pushover           │
  ▲                │
sdof ──────────────┤
  ▲                │
timehistory ◄──────┘      verification3d ◄── motions
  ▲                           ▲
  └────── jobs ───────────────┘
            ▲
     cli ───┘   app ──► jobs, inputs, motions, timehistory, verification3d
```

(`inputs` imports `trapeze`; `timehistory` and `verification3d` use the parsing helpers of `inputs`.)

## Data flow

| Step | Object | Produced by |
|---|---|---|
| system YAML (+ branch CSV, trapeze CSV) | `PipingSystem` | `inputs.load_system` / `PipingSystem.from_dict` |
| validated arrays, trapezes, trilinears | `ResolvedSystem` | `PipingSystem.resolve()` |
| settings YAML | `AnalysisSettings` (+ `TimeHistorySettings`, `Verification3DSettings`) | `inputs.load_settings` |
| one Δc | `ShapeResult` → `PushoverStep` | `static_model.iterate_shape`, `pushover.run_step` |
| Δc list | `PushoverResult` | `pushover.run_pushover` |
| Δc for SDOF | `SDOFParameters` → `SDOFModel` | `sdof.derive_sdof`, `SDOFModel.from_parameters` |
| floor motion | `MotionSet` → `FloorMotion` | `motions.motion_set(...).load(...)` |
| SDOF response | `SDOFResponse` | `timehistory.run_sdof_time_history` |
| 3D model + 2 motions | `Model3D` → `Response3D` | `verification3d.load_model3d`, `run_3d` |

## Design decisions

- **Faithful port, proven by regression.** `static_model` keeps the paper code's OpenSees commands,
  tags, command order and arithmetic. The tests check that every committed pushover result is reproduced
  bit for bit at the stored precision. Behaviour changes in the engine must keep these tests passing, or
  be deliberate and documented.
- **Single source of defaults.** Defaults live only in `inputs/defaults/*.yaml`. User files and app inputs
  are deep-merged over them (`inputs.deep_merge`). Dataclasses carry no default values for user-facing
  settings.
- **Engine data only from `inputs/` and `motions/`.** The paper folder is never read by `piperom`; only
  `validation/` and the tests read it.
- **Data-driven 3D models.** The paper's 3D scripts are converted once (`validation/convert_3d_models.py`)
  into lists of OpenSees commands, replayed by `verification3d`. The models are therefore exactly the
  paper's, without the engine executing the paper's scripts.
- **OpenSees isolation.** OpenSeesPy keeps one global model per process. Each analysis starts with
  `op.wipe()` and silences OpenSees output (`op.logFile(os.devnull)`). The app runs analyses in worker
  processes (`jobs` + `ProcessPoolExecutor` with the spawn context), so concurrent sessions can't
  corrupt each other's models.
- **Validated inputs, clear errors.** All user input passes through `inputs.parse_number` / `check_keys`; problems
  raise `InputError` with the offending entry, which the CLI and the app display.
- **Self-describing outputs.** Result writers include copies of the inputs (system, settings, custom
  trapezes), so a result folder can be re-run.

## Testing and validation

| Suite | Checks | Run time |
|---|---|---|
| `tests/test_regression.py` | 18 pushovers and the SDOF derivation against the paper's code | ~1 min |
| `tests/test_inputs.py` | equivalent input forms, validation errors, round-trips | <1 s |
| `tests/test_static_model.py` | equilibrium of the load pattern (consistent split) on all archetypes | <1 s |
| `tests/test_timehistory.py` | motion catalogue; SDOF and 3D against the paper's stored results (skipped without motions) | ~1 min |
| `tests/test_app.py` | headless app runs of every tab (time-history tab skipped without motions) | ~4 min |
| `validation/run_validation.py` | full static report → `validation/report.md` | ~2 min |
| `validation/run_timehistory_validation.py` | all SDOFs × records × IM1–10, 3D sample → `validation/timehistory_report.md` | ~30 min |

## Extending

- **New archetype or system.** Add a YAML file to `inputs/archetypes/` or `inputs/examples/`
  ([input_files.md](input_files.md)).
- **New motions.** Add files under `motions/` and a set to `motion_sets.yaml`.
- **New 3D model.** Write an OpenSees script with the conventions of the paper's 3D models (`nodesX`,
  `nodesY`, `nodesXt`, `nodesYt` lists, gravity pattern before the first `op.constraints`). Then convert
  it with `validation/convert_3d_models.py` and set `rom_systems` to its system files.
- **New analysis.** Build on `ResolvedSystem` / `SDOFModel`, return a result object with a `write()`
  method, add a job in `jobs`, a CLI command and an app tab.
