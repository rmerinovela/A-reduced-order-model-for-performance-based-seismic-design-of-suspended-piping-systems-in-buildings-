# `piperom/motions.py`: floor-motion sets

## Responsibility

The only access path to floor acceleration histories. It reads the catalogue `motions/motion_sets.yaml`
and loads individual records, converted to mm/s². Format: [input_files.md](../input_files.md#floor-motions).

## Interface

**`MotionSet`**: one catalogue entry.

| Member | Content |
|---|---|
| `name`, `description` | identifier and free text |
| `file_pattern` | relative to `motions/`, with `{record}` and `{level}` |
| `records` | record IDs as strings |
| `record_pairs` | whether consecutive records are the two components of one ground motion |
| `levels` | intensity levels, or `None` |
| `time_column`, `floors` | layout: time column; floor → column |
| `to_mm_s2` | unit factor |
| `path(record, level)` | the file path |
| `pairs()` | `[(x_record, y_record), …]` |
| `load(record, level, floor) -> FloorMotion` | reads one record |

**`FloorMotion`**:
- fields: `set_name`, `record`, `level`, `floor`, `dt` (first value of the time column), `acc` (mm/s²);
- `label`, `duration`.

Functions:
- `load_motion_sets(path=CATALOGUE) -> dict[str, MotionSet]`: an empty dict if there's no catalogue.
- `motion_set(name)`: one set; `InputError` listing the available sets if unknown.
- `select_runs(ms, levels=None, records=None) -> list[(record, level)]`: expands a selection. `None` means
  all; unknown levels or records raise `InputError`.

## Design notes

- Record IDs are strings; numeric IDs read from text files are normalised (`120111.0` → `"120111"`).
- The time step comes from the file (first time value), matching `NLTHA_SDOF.py`. For the provided sets
  it equals the record time step / 10 used by the paper's 3D scripts.
- Loading a 30,000-row file takes about 0.1–0.2 s; nothing is cached, to keep memory flat in batch runs.

## Tests

`tests/test_timehistory.py::test_motion_catalogue_and_selection`.
