"""Command-line interface.

    python -m piperom check       SYSTEM.yaml
    python -m piperom pushover    SYSTEM.yaml [--settings S.yaml] [--out DIR]
    python -m piperom sdof        SYSTEM.yaml [--settings S.yaml] [--delta-c MM] [--out DIR]
    python -m piperom timehistory SYSTEM.yaml [--settings S.yaml] [--delta-c MM] [--set NAME] [--levels 1,2]
                                  [--records ID,ID] [--floor N] [--out DIR]
    python -m piperom verify3d    MODEL [--settings S.yaml] [--set NAME] [--level N] [--pair K | --records X,Y]
                                  [--floor N] [--out DIR]
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .inputs import InputError, load_settings, load_system
from .jobs import verification_job
from .motions import motion_set, select_runs
from .pushover import rows_to_csv, run_pushover
from .sdof import derive_sdof
from .timehistory import SDOFModel, TimeHistorySettings, run_sdof_time_history
from .verification3d import braced_peaks, load_model3d

OUTPUT_DIR = Path("piperom_output")


def _csv_list(text: str | None) -> list[str] | None:
    return [v.strip() for v in text.split(",") if v.strip()] if text else None


def cmd_check(args, settings) -> int:
    rs = load_system(args.system).resolve()
    print(f"{rs.name}: main line {rs.length:g} mm, {rs.n_pipes} pipes")
    print(f"  hangers ({rs.n_hangers}): {', '.join(f'{x:g}' for x in rs.hanger_x)}")
    print(f"  braced  ({int(rs.brace_mask.sum())}): {', '.join(f'{x:g}' for x in rs.hanger_x[rs.brace_mask == 1])}")
    for j in range(rs.n_branches):
        print(f"  branch {j + 1}: x={rs.branch_x[j]:g} length={rs.branch_length[j]:g} "
              f"pipes={rs.branch_n_pipes[j]} braces={rs.branch_n_braces[j]}")
    print(f"  trapezes: T={rs.transverse.name}  L={rs.longitudinal.name}")
    return 0


def cmd_pushover(args, settings) -> int:
    system = load_system(args.system)
    rs = system.resolve()

    def progress(k, n, step):
        flag = "" if step.converged else "  (NOT converged)"
        print(f"  step {k:3d}/{n}  delta_c={step.delta_c:8.3f}  Vb={step.base_shear:12.1f}  "
              f"gamma={step.gamma:.4f}  it={step.iterations}{flag}")

    result = run_pushover(rs, settings, progress)
    for f in result.write(args.out or OUTPUT_DIR / rs.name / "pushover", system, settings):
        print(f"wrote {f}")
    if result.n_not_converged:
        print(f"WARNING: {result.n_not_converged} step(s) did not converge", file=sys.stderr)
    return 0


def cmd_sdof(args, settings) -> int:
    rs = load_system(args.system).resolve()
    p = derive_sdof(rs, settings, args.delta_c)
    print(f"{rs.name} at delta_c={p.delta_c:g} mm: gamma={p.gamma:.4f}  M_eff={p.effective_mass:.4f} t  "
          f"u_sdof={p.u_sdof:.4f} mm" + ("" if p.converged else "  (shape NOT converged)"))
    for f in p.write(args.out or OUTPUT_DIR / rs.name / f"sdof_{p.delta_c:g}"):
        print(f"wrote {f}")
    return 0


def cmd_timehistory(args, settings) -> int:
    rs = load_system(args.system).resolve()
    sel = settings.motions
    ms = motion_set(args.set or sel.get("set"))
    levels = [int(v) for v in _csv_list(args.levels)] if args.levels else sel.get("levels")
    runs = select_runs(ms, levels, _csv_list(args.records) or sel.get("records"))
    floor = args.floor or int(sel.get("floor", 4))
    th = TimeHistorySettings.from_dict(settings.sdof_time_history)

    p = derive_sdof(rs, settings, args.delta_c)
    model = SDOFModel.from_parameters(p)
    print(f"{rs.name}: SDOF at delta_c={p.delta_c:g} mm (gamma={p.gamma:.4f}, M_eff={p.effective_mass:.3f} t); "
          f"{len(runs)} analyses on '{ms.name}', floor {floor}")
    rows = []
    for k, (record, level) in enumerate(runs):
        r = run_sdof_time_history(model, ms.load(record, level, floor), th)
        rows.append({"level": "" if level is None else level, "record": record, "peak_u_sdof": r.peak_u,
                     "peak_support_displacement": p.gamma * max(model.support_phi) * r.peak_u,
                     "completed": r.completed})
        print(f"  {k + 1:4d}/{len(runs)}  level={level}  record={record}  peak u={r.peak_u:8.3f} mm"
              + ("" if r.completed else "  (NOT completed)"))
    out = args.out or OUTPUT_DIR / rs.name / "timehistory"
    out.mkdir(parents=True, exist_ok=True)
    (out / "sdof_peaks.csv").write_text(rows_to_csv(rows, list(rows[0])))
    p.write(out)
    print(f"wrote {out}/sdof_peaks.csv and the SDOF parameters")
    return 0


def cmd_verify3d(args, settings) -> int:
    sel = settings.motions
    ms = motion_set(args.set or sel.get("set"))
    level = None if ms.levels is None else (args.level if args.level is not None else (sel.get("levels") or [None])[0])
    try:
        rx, ry = _csv_list(args.records) if args.records else ms.pairs()[args.pair]
    except (ValueError, IndexError):
        raise InputError("Give --pair as a valid ground-motion index, or --records as 'X_ID,Y_ID'") from None
    floor = args.floor or int(sel.get("floor", 4))

    print(f"3D model {args.model}: x <- {rx}, y <- {ry}, level {level}, floor {floor}")
    res = verification_job(args.model, ms.name, rx, ry, level, floor, settings)
    r = res.response
    print(f"  3D {'completed' if r.completed else f'NOT completed (stopped at {r.end_time:.3f} s)'}; "
          f"T1 = {r.periods[0]:.4f} s")
    for d, peak in braced_peaks(load_model3d(args.model), r).items():
        line = f"  {d}: 3D max peak at braced nodes {peak:.3f} mm"
        if d in res.rom:
            rom = res.rom[d].peak_support_displacement
            line += f" | ROM ({res.rom[d].system}) gamma*phi_max*u = {rom:.3f} mm (ratio {rom / peak:.3f})"
        print(line)
    out = args.out or OUTPUT_DIR / f"3d_{args.model}"
    out.mkdir(parents=True, exist_ok=True)
    rows = ([{"direction": "x", "node": n, "peak_displacement": v} for n, v in zip(r.nodes_x, r.peak_x)]
            + [{"direction": "y", "node": n, "peak_displacement": v} for n, v in zip(r.nodes_y, r.peak_y)])
    (out / "peaks_3d.csv").write_text(rows_to_csv(rows, ["direction", "node", "peak_displacement"]))
    print(f"wrote {out}/peaks_3d.csv")
    return 0


COMMANDS = {"check": cmd_check, "pushover": cmd_pushover, "sdof": cmd_sdof, "timehistory": cmd_timehistory,
            "verify3d": cmd_verify3d}


def build_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(prog="piperom", description="Reduced-order model of suspended piping systems")
    sub = ap.add_subparsers(dest="command", required=True)

    def command(name, help, target="system"):
        p = sub.add_parser(name, help=help)
        if target == "system":
            p.add_argument("system", type=Path, help="piping-system YAML file")
        else:
            p.add_argument("model", help="3D model name in inputs/models3d/ (e.g. M01)")
        p.add_argument("--settings", type=Path, help="analysis-settings YAML file (defaults if omitted)")
        return p

    command("check", "validate a system file and print its resolved layout")
    p = command("pushover", "run the adaptive pseudo-pushover")
    p.add_argument("--out", type=Path, help="output directory (default: piperom_output/<name>/pushover)")
    for name, help in (("sdof", "derive equivalent SDOF parameters at a target displacement"),
                       ("timehistory", "SDOF nonlinear time-history analyses under floor motions")):
        p = command(name, help)
        p.add_argument("--delta-c", type=float, help="Delta_c defining the SDOF in mm (default: settings sdof.delta_c)")
        p.add_argument("--out", type=Path, help="output directory (default: piperom_output/<name>/...)")
    p.add_argument("--levels", help="comma-separated intensity levels (default: settings motions.levels)")
    p.add_argument("--records", help="comma-separated record IDs (default: all records of the set)")
    p3 = command("verify3d", "full 3D analysis of a paper archetype, with the ROM prediction", target="model")
    p3.add_argument("--level", type=int, help="intensity level (default: first of settings motions.levels)")
    p3.add_argument("--pair", type=int, default=0, help="ground-motion pair index (x = first component)")
    p3.add_argument("--records", help="explicit 'X_ID,Y_ID' records instead of --pair")
    p3.add_argument("--out", type=Path, help="output directory (default: piperom_output/3d_<model>)")
    for q in (p, p3):
        q.add_argument("--set", help="motion set in motions/motion_sets.yaml (default: settings motions.set)")
        q.add_argument("--floor", type=int, help="floor (default: settings motions.floor)")
    return ap


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        return COMMANDS[args.command](args, load_settings(args.settings))
    except (ValueError, FileNotFoundError) as exc:   # InputError, malformed trapeze files
        print(f"Input error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
