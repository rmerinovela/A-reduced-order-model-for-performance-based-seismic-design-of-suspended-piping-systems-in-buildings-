"""Floor-motion sets (read only from the ``motions/`` folder, described in ``motions/motion_sets.yaml``)."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np
import yaml

from . import REPO_DIR
from .inputs import InputError

MOTIONS_DIR = REPO_DIR / "motions"
CATALOGUE = MOTIONS_DIR / "motion_sets.yaml"


@dataclass
class FloorMotion:
    set_name: str
    record: str
    level: int | None
    floor: int
    dt: float
    acc: np.ndarray            # mm/s^2, first value at time dt (OpenSees Path series with -prependZero)

    @property
    def label(self) -> str:
        lv = "" if self.level is None else f"IM{self.level} "
        return f"{lv}{self.record} (floor {self.floor})"

    @property
    def duration(self) -> float:
        return self.dt * len(self.acc)


@dataclass
class MotionSet:
    name: str
    description: str
    file_pattern: str
    records: list[str]
    record_pairs: bool
    levels: list[int] | None
    time_column: int
    floors: dict[int, int]
    to_mm_s2: float

    def path(self, record: str, level: int | None = None) -> Path:
        if self.levels is not None and level is None:
            raise InputError(f"Motion set '{self.name}' needs an intensity level")
        return MOTIONS_DIR / self.file_pattern.format(record=record, level=level)

    def pairs(self) -> list[tuple[str, str]]:
        if not self.record_pairs:
            raise InputError(f"Motion set '{self.name}' has no record pairs")
        return [(self.records[i], self.records[i + 1]) for i in range(0, len(self.records) - 1, 2)]

    def load(self, record: str, level: int | None = None, floor: int = 4) -> FloorMotion:
        if record not in self.records:
            raise InputError(f"Record '{record}' is not in motion set '{self.name}'")
        if self.levels is not None and level not in self.levels:
            raise InputError(f"Level {level} is not available in motion set '{self.name}'")
        if floor not in self.floors:
            raise InputError(f"Floor {floor} is not available in motion set '{self.name}'")
        path = self.path(record, level)
        if not path.exists():
            raise InputError(f"Missing floor-motion file: {path.relative_to(REPO_DIR)}")
        data = np.loadtxt(path)
        return FloorMotion(self.name, record, level, floor, dt=float(data[0, self.time_column]),
                           acc=self.to_mm_s2 * data[:, self.floors[floor]])


def _records(spec, name: str) -> list[str]:
    if isinstance(spec, list):
        return [str(r) for r in spec]
    if isinstance(spec, dict) and "file" in spec:
        text = (MOTIONS_DIR / spec["file"]).read_text().split()
        return [str(int(float(v))) if float(v).is_integer() else v for v in text]
    if isinstance(spec, dict) and "range" in spec:
        a, b = spec["range"]
        return [str(i) for i in range(int(a), int(b) + 1)]
    raise InputError(f"Motion set '{name}': 'records' must be a list, {{file: ...}} or {{range: [a, b]}}")


def load_motion_sets(path: Path = CATALOGUE) -> dict[str, MotionSet]:
    if not path.exists():
        return {}
    data = yaml.safe_load(path.read_text()) or {}
    out = {}
    for name, d in data.items():
        try:
            out[name] = MotionSet(
                name=name, description=" ".join(str(d.get("description", "")).split()),
                file_pattern=d["file_pattern"], records=_records(d["records"], name),
                record_pairs=bool(d.get("record_pairs", False)),
                levels=None if d.get("levels") is None else [int(v) for v in d["levels"]],
                time_column=int(d.get("time_column", 0)),
                floors={int(k): int(v) for k, v in d["floors"].items()},
                to_mm_s2=float(d["to_mm_s2"]),
            )
        except (KeyError, TypeError, ValueError) as exc:
            raise InputError(f"Motion set '{name}' in {path.name} is invalid: {exc}") from None
    return out


def motion_set(name: str) -> MotionSet:
    sets = load_motion_sets()
    if name not in sets:
        raise InputError(f"Unknown motion set '{name}'. Available: {', '.join(sets) or 'none'}")
    return sets[name]


def select_runs(ms: MotionSet, levels: list[int] | None = None,
                records: list[str] | None = None) -> list[tuple[str, int | None]]:
    """(record, level) pairs to analyse; ``None`` means every record / every level of the set."""
    if ms.levels is None:
        lv: list[int | None] = [None]
    else:
        lv = list(levels) if levels else list(ms.levels)
        bad = [v for v in lv if v not in ms.levels]
        if bad:
            raise InputError(f"Levels {bad} are not available in motion set '{ms.name}'")
    recs = [str(r) for r in records] if records else list(ms.records)
    bad = [r for r in recs if r not in ms.records]
    if bad:
        raise InputError(f"Records {bad} are not in motion set '{ms.name}'")
    return [(r, l) for l in lv for r in recs]
