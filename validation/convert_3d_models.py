"""Convert the paper's 3D models into data files read by the engine (``inputs/models3d/<name>.json``).

Each script in ``code implementation for paper/3D_models/`` is executed with a recording stand-in for
OpenSees until its first analysis command. The recorded commands (nodes, materials, elements,
constraints and the gravity load pattern) are stored unchanged, with the node lists the script
records in x and y.

    python validation/convert_3d_models.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from validation.legacy import PAPER, REPO, capture_opensees_calls  # noqa: E402

OUT = REPO / "inputs" / "models3d"
NODE_GROUPS = {"X": "nodesX", "Y": "nodesY", "Xt": "nodesXt", "Yt": "nodesYt", "Xp": "nodesXp", "Yp": "nodesYp"}


def plain(v):
    if isinstance(v, (np.integer,)):
        return int(v)
    if isinstance(v, (np.floating,)):
        return float(v)
    if isinstance(v, (list, tuple)):
        return [plain(x) for x in v]
    return v


def convert(script: Path) -> dict:
    calls, ns = capture_opensees_calls(script, stop_at={"constraints"})
    name = script.stem.replace("_biron", "")
    return {
        "name": name,
        "description": f"Full 3D model of archetype {name} (converted from {script.relative_to(REPO)})",
        "units": "N, mm, s",
        "rom_systems": {"x": f"{name}x", "y": f"{name}y"},
        "node_groups": {k: [int(n) for n in ns[v]] for k, v in NODE_GROUPS.items() if v in ns},
        "commands": [[cmd, plain(list(args))] for cmd, args in calls],
    }


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for script in sorted((PAPER / "3D_models").glob("M*_biron.py")):
        model = convert(script)
        path = OUT / f"{model['name']}.json"
        path.write_text(json.dumps(model, indent=None, separators=(",", ":")) + "\n")
        counts = {c: sum(1 for k, _ in model["commands"] if k == c) for c in ("node", "element", "uniaxialMaterial")}
        print(f"{path.relative_to(REPO)}: {counts}, recorded nodes x/y: "
              f"{len(model['node_groups'].get('X', []))}/{len(model['node_groups'].get('Y', []))}")


if __name__ == "__main__":
    main()
