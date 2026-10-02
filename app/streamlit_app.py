"""Interactive front end for the reduced-order model of suspended piping systems.

    streamlit run app/streamlit_app.py
"""

from __future__ import annotations

import hashlib
import io
import multiprocessing as mp
import sys
import zipfile
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
import yaml

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from piperom.inputs import (AnalysisSettings, InputError, PipingSystem,  # noqa: E402
                            dump_yaml, load_system)
from piperom.jobs import pushover_job, sdof_job, sdof_time_history_job, verification_job  # noqa: E402
from piperom.motions import load_motion_sets, select_runs  # noqa: E402
from piperom.timehistory import SDOFModel, support_demands  # noqa: E402
from piperom.verification3d import braced_peaks, list_models3d, load_model3d, model3d_for_system  # noqa: E402
from piperom.pushover import CURVE_COLUMNS, SHAPE_COLUMNS, rows_to_csv  # noqa: E402
from piperom.trapeze import (PARAMETER_NAMES, Pinching4, load_trapeze, parse_trapeze_csv,  # noqa: E402
                             trilinear_from_pinching4)

INPUT_DIRS = {"Archetype": REPO / "inputs" / "archetypes", "Example": REPO / "inputs" / "examples"}
KINDS = {"transverse": "Transverse (C-TPS-T)", "longitudinal": "Longitudinal (C-TPS-L)"}
PREFIX = {"transverse": "T", "longitudinal": "L"}
C_MAIN, C_BRACE, C_BRANCH, C_MUTED = "#1f77b4", "#d62728", "#2ca02c", "#9e9e9e"

st.set_page_config(page_title="Suspended piping ROM", layout="wide")


# ============================================================================ worker process
@st.cache_resource
def executor() -> ProcessPoolExecutor:
    # OpenSees state is global per process: analyses run in worker processes, one at a time each.
    return ProcessPoolExecutor(max_workers=2, mp_context=mp.get_context("spawn"))


@st.cache_resource
def manager():
    return mp.get_context("spawn").Manager()


# ============================================================================ state
def load_into_state(system: PipingSystem, trapezes: dict[str, Pinching4] | None = None) -> None:
    ss = st.session_state
    ss.v = ss.get("v", 0) + 1
    ss.name, ss.description = system.name, system.description
    ss.length, ss.n_pipes = float(system.length), int(system.n_pipes)
    for k, v in vars(system.pipe).items():
        ss[f"pipe_{k}"] = v
    ss.branch_participation = system.branch_participation
    if system.hanger_positions is not None:
        ss.h_mode = "Explicit positions"
        ss.h_positions = ", ".join(f"{x:g}" for x in system.hanger_positions)
    else:
        ss.h_mode = "Regular grid"
        ss.h_positions = ""
    ss.h_first = float(system.hanger_first or 1000.0)
    ss.h_spacing = float(system.hanger_spacing or 3000.0)
    ss.h_clearance = float(system.hanger_end_clearance)
    if system.brace_count is not None:
        ss.b_mode, ss.b_count, ss.brace_pos = "Evenly spaced", int(system.brace_count), []
    else:
        hx = system.hanger_x()
        mask = system.brace_mask_array(hx)
        ss.b_mode, ss.b_count, ss.brace_pos = "Select hangers", int(mask.sum()), [float(x) for x in hx[mask == 1]]
    ss.branches_df = pd.DataFrame([vars(b) for b in system.branches], columns=["x", "length", "n_pipes", "n_braces"])
    trapezes = trapezes or {}
    ss.trapeze_base = {k: trapezes.get(k) or load_trapeze(system.trapezes.get(k), k) for k in KINDS}
    ss.trapeze_source = {k: (Path(str(system.trapezes.get(k))).name
                             if system.trapezes.get(k) not in (None, "default") else "default file")
                         for k in KINDS}


def load_settings_into_state(s: AnalysisSettings) -> None:
    ss = st.session_state
    ss.s_explicit = s.delta_c_values is not None
    ss.s_values = ", ".join(f"{v:g}" for v in (s.delta_c_values or []))
    ss.s_start, ss.s_stop, ss.s_n = s.delta_c_start, s.delta_c_stop, s.n_steps
    ss.s_warm = s.warm_start
    ss.s_maxit, ss.s_tol = s.max_iterations, s.tolerance
    ss.s_test, ss.s_stol, ss.s_smaxit = s.solver_test, s.solver_tolerance, s.solver_max_iterations
    ss.s_sdof_dc = s.sdof_delta_c
    ss.s_split = s.branch_split
    ss.s_raw = {k: s.to_dict()[k] for k in ("motions", "sdof_time_history", "verification_3d")}
    th, v3, mo = s.sdof_time_history, s.verification_3d, s.motions
    ss.th_xi, ss.th_test, ss.th_tol, ss.th_maxit = th["damping_ratio"], th["test"], th["tolerance"], th["max_iterations"]
    ss.v3_xi, ss.v3_test, ss.v3_tol, ss.v3_maxit = v3["damping_ratio"], v3["test"], v3["tolerance"], v3["max_iterations"]
    ss.v3_fb_test, ss.v3_fb_tol = v3["fallback_test"], v3["fallback_tolerance"]
    ss.m_set, ss.m_levels, ss.m_floor = mo.get("set"), list(mo.get("levels") or []), int(mo.get("floor", 4))


if "v" not in st.session_state:
    load_into_state(load_system(INPUT_DIRS["Archetype"] / "M01y.yaml"))
    load_settings_into_state(AnalysisSettings.from_dict())

# Streamlit drops the state of widgets that are not rendered in a run (e.g. grid inputs while explicit
# hanger positions are selected); re-assigning keeps every input across mode switches.
PERSISTENT = ["name", "description", "length", "n_pipes", "branch_participation", "h_mode", "h_positions",
              "h_first", "h_spacing", "h_clearance", "b_mode", "b_count", "s_explicit", "s_values", "s_start",
              "s_stop", "s_n", "s_warm", "s_maxit", "s_tol", "s_test", "s_stol", "s_smaxit", "s_sdof_dc", "s_split",
              "th_xi", "th_test", "th_tol", "th_maxit", "v3_xi", "v3_test", "v3_tol", "v3_maxit", "v3_fb_test",
              "v3_fb_tol", "m_set", "m_levels", "m_floor",
              *(f"pipe_{k}" for k in ("outer_diameter", "inner_diameter", "elastic_modulus", "shear_modulus",
                                      "density", "mass_factor"))]
for _k in PERSISTENT:
    if _k in st.session_state:
        st.session_state[_k] = st.session_state[_k]


def parse_list(text: str) -> list[float]:
    return [float(v) for v in text.replace(";", ",").replace("\n", ",").split(",") if v.strip()]


# ============================================================================ sidebar
with st.sidebar:
    st.header("Inputs")
    src = st.radio("Start from", ["Archetype", "Example", "Upload file"], horizontal=True)
    if src == "Upload file":
        up = st.file_uploader("System file (YAML)", type=["yaml", "yml"])
        st.caption("Trapeze or branch files referenced by the YAML can't be resolved from an upload; "
                   "upload custom trapezes in the Trapezes tab instead.")
        if up is not None and st.button("Load system", type="primary"):
            try:
                data = yaml.safe_load(up.getvalue()) or {}
                for kind in KINDS:   # referenced files are not available
                    if isinstance((data.get("trapezes") or {}).get(kind), str):
                        data["trapezes"][kind] = "default"
                load_into_state(PipingSystem.from_dict(data))
                st.rerun()
            except Exception as exc:  # noqa: BLE001
                st.error(f"Could not load: {exc}")
    else:
        files = sorted(INPUT_DIRS[src].glob("*.yaml"))
        choice = st.selectbox(src, [f.stem for f in files])
        if st.button("Load", type="primary"):
            load_into_state(load_system(INPUT_DIRS[src] / f"{choice}.yaml"))
            st.rerun()

    st.divider()
    up_s = st.file_uploader("Settings file (YAML, optional)", type=["yaml", "yml"])
    c1, c2 = st.columns(2)
    if c1.button("Load settings", disabled=up_s is None):
        try:
            load_settings_into_state(AnalysisSettings.from_dict(yaml.safe_load(up_s.getvalue()) or {}))
            st.rerun()
        except Exception as exc:  # noqa: BLE001
            st.error(f"Could not load settings: {exc}")
    if c2.button("Default settings"):
        load_settings_into_state(AnalysisSettings.from_dict())
        st.rerun()
    st.divider()
    st.caption("Units: N, mm, s. Masses in tonnes.")

ss = st.session_state
v = ss.v
st.title("Suspended piping systems: reduced-order model")
tab_geo, tab_trap, tab_set, tab_po, tab_sdof, tab_th, tab_3d = st.tabs(
    ["Geometry", "Trapezes", "Settings", "Pseudo-pushover", "SDOF parameters", "SDOF time history",
     "3D verification"])


# ============================================================================ geometry
def hangers_from_state() -> dict:
    if ss.h_mode == "Explicit positions":
        try:
            return {"end_clearance": ss.h_clearance, "positions": parse_list(ss.h_positions)}
        except ValueError:
            raise InputError("Hanger positions must be numbers separated by commas") from None
    return {"end_clearance": ss.h_clearance, "first": ss.h_first, "spacing": ss.h_spacing}


def system_from_state() -> tuple[PipingSystem | None, str | None]:
    try:
        hangers = hangers_from_state()
    except InputError as exc:
        return None, str(exc)
    braces = {"count": int(ss.b_count)} if ss.b_mode == "Evenly spaced" else {"positions": list(ss.brace_pos)}
    br = ss.branches_edit.dropna(how="all") if "branches_edit" in ss else ss.branches_df
    pipe = {k: ss[f"pipe_{k}"] for k in ("outer_diameter", "inner_diameter", "elastic_modulus", "shear_modulus",
                                         "density", "fluid_density", "mass_factor")}
    data = {"name": ss.name, "description": ss.description,
            "main_line": {"length": ss.length, "n_pipes": ss.n_pipes}, "pipe": pipe,
            "hangers": hangers, "braces": braces,
            "branches": br.to_dict("records"), "branch_participation": ss.branch_participation}
    try:
        system = PipingSystem.from_dict(data)
        system.trapezes = dict(ss.get("trapezes", {}))
        system.resolve()
        return system, None
    except (InputError, ValueError) as exc:
        return None, str(exc)


def plan_view(system: PipingSystem) -> go.Figure:
    rs = system.resolve()
    fig = go.Figure()
    L = rs.length / 1000
    fig.add_trace(go.Scatter(x=[0, L], y=[0, 0], mode="lines", line=dict(color=C_MAIN, width=4), name="Main line"))
    hx = rs.hanger_x / 1000
    fig.add_trace(go.Scatter(x=hx[rs.brace_mask == 0], y=0 * hx[rs.brace_mask == 0], mode="markers",
                             marker=dict(symbol="line-ns-open", size=14, color=C_MUTED, line=dict(width=2)),
                             name="Gravity hanger"))
    fig.add_trace(go.Scatter(x=hx[rs.brace_mask == 1], y=0 * hx[rs.brace_mask == 1], mode="markers",
                             marker=dict(symbol="triangle-up", size=13, color=C_BRACE), name="Transverse brace"))
    seen: dict[float, int] = {}
    for j in range(rs.n_branches):
        x = rs.branch_x[j] / 1000
        side = 1 if seen.get(x, 0) % 2 == 0 else -1
        seen[x] = seen.get(x, 0) + 1
        y_end = side * rs.branch_length[j] / 1000
        fig.add_trace(go.Scatter(
            x=[x, x], y=[0, y_end], mode="lines", line=dict(color=C_BRANCH, width=3), name="Branch",
            legendgroup="branch", showlegend=j == 0,
            hovertext=f"Branch {j + 1}: x={x:g} m, L={rs.branch_length[j] / 1000:g} m, "
                      f"{rs.branch_n_pipes[j]} pipes, {rs.branch_n_braces[j]} longitudinal braces",
            hoverinfo="text"))
        fig.add_annotation(x=x, y=y_end, text=f"{rs.branch_n_braces[j]}L", showarrow=False,
                           yshift=10 * side, font=dict(color=C_BRANCH, size=11))
    fig.add_annotation(x=L * 0.5, y=0, ax=0, ay=-45, text="loading direction", showarrow=True, arrowhead=2,
                       arrowcolor="#555", font=dict(color="#555"), yshift=-6)
    fig.update_layout(height=420, margin=dict(l=10, r=10, t=30, b=10), legend=dict(orientation="h", y=1.08),
                      xaxis_title="x (m)", yaxis_title="y (m)")
    fig.update_yaxes(scaleanchor="x", scaleratio=1)
    return fig


with tab_geo:
    c1, c2 = st.columns([1, 2])
    with c1:
        st.text_input("Name", key="name")
        st.text_area("Description", key="description", height=68)
        st.subheader("Main line")
        st.number_input("Length (mm)", min_value=1.0, step=500.0, key="length")
        st.number_input("Number of pipes", min_value=1, step=1, key="n_pipes")
        with st.expander("Pipe properties"):
            st.number_input("Outer diameter (mm)", min_value=0.1, key="pipe_outer_diameter")
            st.number_input("Inner diameter (mm)", min_value=0.0, key="pipe_inner_diameter")
            st.number_input("Elastic modulus (MPa)", min_value=1.0, key="pipe_elastic_modulus")
            st.number_input("Shear modulus (MPa)", min_value=1.0, key="pipe_shear_modulus")
            st.number_input("Density (t/mm³)", min_value=0.0, format="%.3e", key="pipe_density")
            fluid_default = st.checkbox("Fluid density = density / 7.8 (water in steel)",
                                        value=ss.pipe_fluid_density is None, key=f"fluid_default_{v}")
            if fluid_default:
                ss.pipe_fluid_density = None
            else:
                ss.pipe_fluid_density = st.number_input(
                    "Fluid density (t/mm³)", min_value=0.0, format="%.3e",
                    value=float(ss.pipe_fluid_density if ss.pipe_fluid_density is not None
                                else ss.pipe_density / 7.8), key=f"fluid_{v}")
            st.number_input("Mass factor", min_value=0.01, key="pipe_mass_factor")
            st.number_input("Branch participation factor", min_value=0.01, key="branch_participation")

        st.subheader("Hangers")
        st.radio("Definition", ["Regular grid", "Explicit positions"], key="h_mode", horizontal=True)
        if ss.h_mode == "Regular grid":
            g1, g2, g3 = st.columns(3)
            g1.number_input("First (mm)", min_value=0.0, step=100.0, key="h_first")
            g2.number_input("Spacing (mm)", min_value=1.0, step=100.0, key="h_spacing")
            g3.number_input("End clearance (mm)", min_value=0.0, step=100.0, key="h_clearance")
        else:
            if not ss.h_positions.strip():   # start from the current grid
                try:
                    grid = PipingSystem.from_dict({"main_line": {"length": ss.length, "n_pipes": 1}, "braces": {"count": 0},
                                                   "hangers": {"first": ss.h_first, "spacing": ss.h_spacing,
                                                               "end_clearance": ss.h_clearance}}).hanger_x()
                    ss.h_positions = ", ".join(f"{x:g}" for x in grid)
                except (InputError, ValueError):
                    pass
            st.text_area("Positions along the main line (mm, comma separated)", key="h_positions")

    with c2:
        st.subheader("Transverse braces")
        st.radio("Placement", ["Select hangers", "Evenly spaced"], key="b_mode", horizontal=True)
        try:
            hanger_x = PipingSystem.from_dict({"main_line": {"length": ss.length, "n_pipes": 1},
                                               "hangers": hangers_from_state(), "braces": {"count": 0}}).hanger_x()
        except (InputError, ValueError) as exc:
            hanger_x = np.array([])
            st.error(str(exc))
        if ss.b_mode == "Evenly spaced":
            ss.b_count = min(int(ss.b_count), len(hanger_x))
            st.number_input("Number of braces", min_value=0, max_value=max(len(hanger_x), 0), step=1, key="b_count")
            st.caption("Placed at length/n spacing starting at half a spacing, snapped to the nearest free hanger.")
        else:
            braced = {round(x, 6) for x in ss.brace_pos}
            df = pd.DataFrame({"hanger": np.arange(1, len(hanger_x) + 1), "x (mm)": hanger_x,
                               "braced": [round(x, 6) in braced for x in hanger_x]})
            h_key = hashlib.md5(hanger_x.tobytes()).hexdigest()[:8]
            edited = st.data_editor(df, key=f"braces_{v}_{h_key}", hide_index=True, height=220,
                                    disabled=["hanger", "x (mm)"], width="stretch")
            if len(hanger_x):   # keep the braces while the hanger list is invalid
                ss.brace_pos = [float(x) for x, b in zip(edited["x (mm)"], edited["braced"]) if b]

        st.subheader("Branches")
        st.caption("Orthogonal pipelines framing into the main line; x = junction position along the main line.")
        ss.branches_edit = st.data_editor(
            ss.branches_df, key=f"branches_{v}", num_rows="dynamic", width="stretch", hide_index=True,
            column_config={"x": st.column_config.NumberColumn("x (mm)", min_value=0.0),
                           "length": st.column_config.NumberColumn("length (mm)", min_value=0.0),
                           "n_pipes": st.column_config.NumberColumn("pipes", min_value=1, step=1),
                           "n_braces": st.column_config.NumberColumn("longitudinal braces", min_value=1, step=1)})



# ============================================================================ trapezes
def trapeze_figure(p: Pinching4, title: str) -> go.Figure:
    tri = trilinear_from_pinching4(p)
    d = [0.0, *p.pos_disp]
    f = [0.0, *p.pos_force]
    dn, fn = [0.0, *p.neg_disp], [0.0, *p.neg_force]
    u = np.linspace(0, p.pos_disp[-1], 200)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=d, y=np.array(f) / 1e3, mode="lines+markers", name="Pinching4 envelope",
                             line=dict(color=C_MAIN)))
    fig.add_trace(go.Scatter(x=dn, y=np.array(fn) / 1e3, mode="lines+markers", name="(negative)",
                             line=dict(color=C_MAIN, dash="dot"), showlegend=False))
    fig.add_trace(go.Scatter(x=u, y=[tri.force(x) / 1e3 for x in u], mode="lines",
                             name="Trilinear used in static procedure", line=dict(color=C_BRACE, dash="dash")))
    fig.update_layout(title=title, height=330, margin=dict(l=10, r=10, t=40, b=10),
                      xaxis_title="Deformation (mm)", yaxis_title="Force (kN)", legend=dict(orientation="h", y=-0.25))
    return fig


with tab_trap:
    st.caption("All braces of a type share one definition. Defaults: `inputs/trapezes/`. "
               "Upload a file in the same format or edit the values directly.")
    ss.trapezes = {}
    cols = st.columns(2)
    for col, (kind, label) in zip(cols, KINDS.items()):
        with col:
            st.subheader(label)
            st.caption(f"Source: {ss.trapeze_source[kind]}")
            up = st.file_uploader(f"Upload {kind} trapeze (CSV)", type=["csv"], key=f"up_{kind}_{v}")
            b1, b2 = st.columns(2)
            if b1.button("Use uploaded file", key=f"use_{kind}", disabled=up is None):
                try:
                    ss.trapeze_base[kind] = parse_trapeze_csv(up.getvalue().decode(), name=up.name)
                    ss.trapeze_source[kind] = up.name
                    ss.v += 1
                    st.rerun()
                except ValueError as exc:
                    st.error(str(exc))
            if b2.button("Reset to default", key=f"reset_{kind}"):
                ss.trapeze_base[kind] = load_trapeze("default", kind)
                ss.trapeze_source[kind] = "default file"
                ss.v += 1
                st.rerun()
            base = ss.trapeze_base[kind]
            params = base.parameters()
            df = pd.DataFrame({"parameter": PARAMETER_NAMES, "value": [str(params[k]) for k in PARAMETER_NAMES]})
            with st.expander("Parameters"):
                edited = st.data_editor(df, key=f"trap_{kind}_{v}", hide_index=True, disabled=["parameter"],
                                        width="stretch", height=400)
            try:
                p = Pinching4.from_parameters(dict(zip(edited["parameter"], edited["value"])), name=base.name)
                if p.parameters() != base.parameters():
                    ss.trapeze_source[kind] = "edited in app"
                ss.trapezes[kind] = p
                st.plotly_chart(trapeze_figure(p, label), width="stretch")
                st.download_button("Download CSV", p.to_csv(PREFIX[kind]), file_name=f"trapeze_{kind}.csv",
                                   key=f"dl_{kind}")
            except ValueError as exc:
                st.error(str(exc))

system, error = system_from_state()


# ============================================================================ settings
def settings_from_state() -> tuple[AnalysisSettings | None, str | None]:
    try:
        values = parse_list(ss.s_values) if ss.s_explicit else None
        data = {"pushover": {"delta_c_start": ss.s_start, "delta_c_stop": ss.s_stop, "n_steps": ss.s_n,
                             "delta_c_values": values, "warm_start": ss.s_warm},
                "shape_iteration": {"max_iterations": ss.s_maxit, "tolerance": ss.s_tol},
                "static_solver": {"test": ss.s_test, "tolerance": ss.s_stol, "max_iterations": ss.s_smaxit},
                "equivalent_static": {"branch_split": ss.s_split},
                "sdof": {"delta_c": ss.s_sdof_dc},
                "motions": {**ss.s_raw["motions"], "set": ss.m_set, "levels": list(ss.m_levels) or None,
                            "floor": int(ss.m_floor)},
                "sdof_time_history": {**ss.s_raw["sdof_time_history"], "damping_ratio": ss.th_xi,
                                      "test": ss.th_test, "tolerance": ss.th_tol, "max_iterations": ss.th_maxit},
                "verification_3d": {**ss.s_raw["verification_3d"], "damping_ratio": ss.v3_xi, "test": ss.v3_test,
                                    "tolerance": ss.v3_tol, "max_iterations": ss.v3_maxit,
                                    "fallback_test": ss.v3_fb_test, "fallback_tolerance": ss.v3_fb_tol}}
        return AnalysisSettings.from_dict(data), None
    except (InputError, ValueError) as exc:
        return None, str(exc)


with tab_set:
    c1, c2, c3 = st.columns(3)
    with c1:
        st.subheader("Pseudo-pushover")
        st.checkbox("Explicit list of target displacements", key="s_explicit")
        if ss.s_explicit:
            st.text_area("Delta_c values (mm)", key="s_values")
        else:
            st.number_input("Delta_c start (mm)", min_value=1e-6, format="%.3f", key="s_start")
            st.number_input("Delta_c stop (mm)", min_value=1e-6, format="%.3f", key="s_stop")
            st.number_input("Number of steps", min_value=1, step=1, key="s_n")
        st.checkbox("Warm start from previous step's shape", key="s_warm")
    with c2:
        st.subheader("Shape iteration")
        st.number_input("Maximum iterations", min_value=1, step=1, key="s_maxit")
        st.number_input("Tolerance (RMS shape change)", min_value=1e-12, format="%.1e", key="s_tol")
        st.subheader("Static solver")
        st.selectbox("Convergence test", ["NormDispIncr", "EnergyIncr", "NormUnbalance"], key="s_test")
        st.number_input("Solver tolerance", min_value=1e-16, format="%.1e", key="s_stol")
        st.number_input("Solver max iterations", min_value=1, step=1, key="s_smaxit")
        st.selectbox("Branch force split", ["consistent", "legacy"], key="s_split",
                     help="consistent: the branch force is fully applied (junction node mass in the main-line "
                          "share). legacy: as the paper's code, which reproduces its pushover results "
                          "(docs/legacy_issues.md, A2).")
    with c3:
        st.subheader("Equivalent SDOF")
        st.number_input("Delta_c defining the SDOF (mm)", min_value=1e-6, format="%.3f", key="s_sdof_dc")
    tests = ["EnergyIncr", "RelativeEnergyIncr", "NormDispIncr", "NormUnbalance"]
    c4, c5 = st.columns(2)
    with c4:
        st.subheader("SDOF time history")
        st.number_input("Damping ratio", min_value=0.0, max_value=1.0, format="%.3f", key="th_xi")
        st.selectbox("Convergence test", tests, key="th_test")
        st.number_input("Tolerance", min_value=1e-16, format="%.1e", key="th_tol")
        st.number_input("Max iterations", min_value=1, step=1, key="th_maxit")
        st.caption("Rayleigh damping on the current stiffness, from the SDOF period (as NLTHA_SDOF.py).")
    with c5:
        st.subheader("3D verification")
        st.number_input("Damping ratio ", min_value=0.0, max_value=1.0, format="%.3f", key="v3_xi")
        st.selectbox("Convergence test ", tests, key="v3_test")
        st.number_input("Tolerance ", min_value=1e-16, format="%.1e", key="v3_tol")
        st.number_input("Max iterations ", min_value=1, step=1, key="v3_maxit")
        st.selectbox("Fallback test", tests, key="v3_fb_test")
        st.number_input("Fallback tolerance", min_value=1e-16, format="%.1e", key="v3_fb_tol")
        st.caption("Rayleigh damping on mass and committed stiffness, modes 1-2 (as the paper's 3D models). "
                   "The paper's M01-M03 scripts use RelativeEnergyIncr, which fails to converge from rest; "
                   "M29-M63 use EnergyIncr (default).")
    settings, s_error = settings_from_state()
    if s_error:
        st.error(s_error)
    else:
        st.download_button("Download settings (YAML)", settings.to_yaml(), file_name="settings.yaml")


# ============================================================================ bundles
def custom_trapeze_files(system: PipingSystem) -> dict[str, str]:
    out = {}
    for kind, p in system.trapezes.items():
        if isinstance(p, Pinching4) and p.parameters() != load_trapeze("default", kind).parameters():
            out[f"custom_{kind}.csv"] = p.to_csv(PREFIX[kind])
    return out


def system_yaml(system: PipingSystem) -> str:
    d = system.to_dict()
    custom = custom_trapeze_files(system)
    d["trapezes"] = {k: (f"custom_{k}.csv" if f"custom_{k}.csv" in custom else "default") for k in KINDS}
    return dump_yaml(d)


def zip_bytes(files: dict[str, str]) -> bytes:
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
        for name, text in files.items():
            z.writestr(name, text)
    return buf.getvalue()


def input_files(system: PipingSystem, settings: AnalysisSettings) -> dict[str, str]:
    return {"system.yaml": system_yaml(system), "settings.yaml": settings.to_yaml(), **custom_trapeze_files(system)}


def signature(*parts: str) -> str:
    return hashlib.sha1("\n".join(parts).encode()).hexdigest()


with tab_geo:
    st.subheader("Plan view")
    if error:
        st.error(error)
    else:
        st.plotly_chart(plan_view(system), width="stretch")
    if system is not None and settings is not None:
        st.download_button("Download inputs (system + settings + custom trapezes, zip)",
                           zip_bytes(input_files(system, settings)), file_name=f"{system.name}_inputs.zip")

ready = system is not None and settings is not None
if ready:
    trap_sig = "".join(str(sorted(p.parameters().items())) for p in system.trapezes.values())
    po_sig = signature(system_yaml(system), trap_sig, dump_yaml({
        k: v for k, v in settings.to_dict().items()
        if k not in ("sdof", "motions", "sdof_time_history", "verification_3d")}))
    sd_sig = po_sig + signature(str(settings.sdof_delta_c))


# ============================================================================ SDOF backbone
def sdof_backbone(params) -> tuple[np.ndarray, np.ndarray]:
    """Monotonic backbone of the SDOF: sum of the springs' positive envelopes, up to the first envelope end."""
    u_max = min(s.spring.pos_disp[-1] for s in params.supports)
    u = np.linspace(0, u_max, 300)
    F = sum(np.interp(u, [0, *s.spring.pos_disp], [0, *s.spring.pos_force]) for s in params.supports)
    return u, F



# ============================================================================ pushover
def run_remote(fn, *args, label="Step"):
    """Run ``fn(*args, queue)`` in a worker process, showing its (k, n) progress messages."""
    q = manager().Queue()
    fut = executor().submit(fn, *args, q)
    bar = st.progress(0.0, text="Starting worker...")
    while not fut.done():
        try:
            k, n = q.get(timeout=0.2)
            text = f"{label} {k}/{n}" if isinstance(k, int) else f"{label} {100 * k / n:.0f}%"
            bar.progress(min(k / n, 1.0), text=text)
        except Exception:  # noqa: BLE001  (queue.Empty)
            pass
    bar.empty()
    return fut.result()


def run_pushover_remote(system: PipingSystem, settings: AnalysisSettings):
    return run_remote(pushover_job, system, settings)


with tab_po:
    if not ready:
        st.warning("Fix the inputs first: " + (error or s_error or ""))
    else:
        n_steps = len(settings.delta_c())
        st.write(f"**{system.name}**: {n_steps} target displacements from {settings.delta_c()[0]:g} "
                 f"to {settings.delta_c()[-1]:g} mm.")
        if st.button("Run pseudo-pushover", type="primary"):
            try:
                ss.po_result, ss.po_sig = run_pushover_remote(system, settings), po_sig
                ss.po_inputs = input_files(system, settings)
            except Exception as exc:  # noqa: BLE001
                st.error(f"Analysis failed: {exc}")
        res = ss.get("po_result")
        if res is not None:
            if ss.po_sig != po_sig:
                st.info("Inputs changed since this run; results below refer to the previous inputs.")
            if res.n_not_converged:
                st.warning(f"{res.n_not_converged} step(s) did not reach the shape tolerance.")
            curve = pd.DataFrame(res.curve_rows())
            c1, c2 = st.columns(2)
            with c1:
                xaxis = st.radio("Capacity curve abscissa", ["u_sdof", "delta_c"], horizontal=True,
                                 format_func={"u_sdof": "Equivalent SDOF displacement",
                                              "delta_c": "Target displacement Δc"}.get)
                fig = go.Figure(go.Scatter(x=curve[xaxis], y=curve.base_shear / 1e3, mode="lines+markers",
                                           line=dict(color=C_MAIN), name="2D pseudo-pushover"))
                sd = ss.get("sdof_result")
                if sd is not None and ss.get("sdof_sig", "").startswith(po_sig) and xaxis == "u_sdof":
                    u, F = sdof_backbone(sd)
                    fig.add_trace(go.Scatter(x=u, y=F / 1e3, mode="lines", line=dict(color=C_BRACE, dash="dash"),
                                             name=f"SDOF backbone (Δc = {sd.delta_c:g} mm)"))
                fig.update_layout(height=380, margin=dict(l=10, r=10, t=10, b=10), yaxis_title="Base shear (kN)",
                                  xaxis_title="u_SDOF (mm)" if xaxis == "u_sdof" else "Δc (mm)",
                                  legend=dict(orientation="h", y=1.1))
                st.plotly_chart(fig, width="stretch")
            with c2:
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=curve.delta_c, y=curve.gamma, name="Γ", line=dict(color=C_MAIN)))
                fig.add_trace(go.Scatter(x=curve.delta_c, y=curve.mass_ratio, name="Effective mass ratio",
                                         line=dict(color=C_BRANCH)))
                fig.update_layout(height=410, margin=dict(l=10, r=10, t=40, b=10), xaxis_title="Δc (mm)",
                                  legend=dict(orientation="h", y=1.1))
                st.plotly_chart(fig, width="stretch")

            k = st.select_slider("Displaced shape at Δc (mm)", options=list(range(len(res.steps))),
                                 format_func=lambda i: f"{res.steps[i].delta_c:.3g}", value=len(res.steps) - 1)
            step = res.steps[k]
            dofs = pd.DataFrame(res.dofs)
            scaled = st.toggle("Show displacements in mm (otherwise normalised to the reference branch DOF)")
            yv = step.d_scaled if scaled else step.d_norm
            h = dofs.kind == "hanger"
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=dofs.x[h] / 1e3, y=yv[h.values], mode="lines+markers", name="Main line",
                                     line=dict(color=C_MAIN), marker=dict(size=5)))
            hb = h & dofs.braced
            fig.add_trace(go.Scatter(x=dofs.x[hb] / 1e3, y=yv[hb.values], mode="markers", name="Transverse brace",
                                     marker=dict(symbol="triangle-up", size=11, color=C_BRACE)))
            b = dofs.kind == "branch"
            fig.add_trace(go.Scatter(x=dofs.x[b] / 1e3, y=yv[b.values], mode="markers", name="Branch DOF",
                                     marker=dict(symbol="diamond", size=11, color=C_BRANCH),
                                     hovertext=[f"branch {int(j) + 1}" for j in dofs.branch[b]]))
            fig.update_layout(height=360, margin=dict(l=10, r=10, t=10, b=10), xaxis_title="x along main line (m)",
                              yaxis_title="Displacement (mm)" if scaled else "Normalised displacement",
                              legend=dict(orientation="h", y=1.1))
            st.plotly_chart(fig, width="stretch")
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Base shear", f"{step.base_shear / 1e3:.2f} kN")
            m2.metric("Γ", f"{step.gamma:.4f}")
            m3.metric("Effective mass", f"{step.effective_mass:.3f} t")
            m4.metric("Shape iterations", f"{step.iterations}" + ("" if step.converged else " (not converged)"))

            with st.expander("Capacity curve table"):
                st.dataframe(curve, hide_index=True, width="stretch")
            files = {"pushover_curve.csv": rows_to_csv(res.curve_rows(), CURVE_COLUMNS),
                     "pushover_shapes.csv": rows_to_csv(res.shape_rows(), SHAPE_COLUMNS), **ss.po_inputs}
            d1, d2 = st.columns(2)
            d1.download_button("Download capacity curve (CSV)", files["pushover_curve.csv"],
                               file_name=f"{res.name}_pushover_curve.csv")
            d2.download_button("Download all results and inputs (zip)", zip_bytes(files),
                               file_name=f"{res.name}_pushover.zip")


# ============================================================================ SDOF
def current_sdof():
    """SDOF parameters derived in this session for the current inputs, or None."""
    sd = ss.get("sdof_result")
    return sd if ready and sd is not None and ss.get("sdof_sig") == sd_sig else None


def derive_sdof_button(key: str) -> None:
    if st.button("Derive SDOF parameters", type="primary", key=key):
        try:
            with st.spinner("Running the equivalent static procedure..."):
                ss.sdof_result = executor().submit(sdof_job, system, settings, settings.sdof_delta_c).result()
            ss.sdof_sig = sd_sig
            ss.sdof_inputs = input_files(system, settings)
        except Exception as exc:  # noqa: BLE001
            st.error(f"Derivation failed: {exc}")
        else:
            st.rerun()


with tab_sdof:
    if not ready:
        st.warning("Fix the inputs first: " + (error or s_error or ""))
    else:
        st.write(f"Equivalent SDOF of **{system.name}** at Δc = **{settings.sdof_delta_c:g} mm** "
                 "(change it in the Settings tab).")
        derive_sdof_button("derive_sdof")
        sd = ss.get("sdof_result")
        if sd is not None:
            if ss.sdof_sig != sd_sig:
                st.info("Inputs changed since these parameters were derived.")
            if not sd.converged:
                st.warning("The displaced shape did not reach the tolerance at this Δc.")
            m = st.columns(5)
            m[0].metric("Γ", f"{sd.gamma:.4f}")
            m[1].metric("Effective mass", f"{sd.effective_mass:.3f} t")
            m[2].metric("Mass ratio", f"{sd.mass_ratio:.3f}")
            m[3].metric("u_SDOF at Δc", f"{sd.u_sdof:.3f} mm")
            m[4].metric("Base shear at Δc", f"{sd.base_shear / 1e3:.2f} kN")
            rows = [{"kind": s.kind, "x (mm)": s.x, "branch": "" if s.branch is None else s.branch + 1,
                     "φ": s.phi, "trapezes": s.n_trapezes, "Γ·φ": sd.gamma * s.phi,
                     **{f"ePd{i + 1} (mm)": s.spring.pos_disp[i] for i in range(4)},
                     **{f"ePf{i + 1} (kN)": s.spring.pos_force[i] / 1e3 for i in range(4)}}
                    for s in sd.supports]
            st.dataframe(pd.DataFrame(rows), hide_index=True, width="stretch")
            u, F = sdof_backbone(sd)
            fig = go.Figure(go.Scatter(x=u, y=F / 1e3, mode="lines", line=dict(color=C_BRACE),
                                       name="SDOF backbone"))
            fig.update_layout(height=320, margin=dict(l=10, r=10, t=10, b=10), xaxis_title="u_SDOF (mm)",
                              yaxis_title="Force (kN)")
            st.plotly_chart(fig, width="stretch")
            st.caption("Backbone = sum of the scaled spring envelopes (positive branch), plotted up to the first "
                       "spring's last envelope point. Overlay it on the pushover curve in the Pseudo-pushover tab.")
            files = {"sdof_parameters.yaml": sd.to_yaml(), "sdof_springs.csv": sd.springs_csv(), **ss.sdof_inputs}
            d1, d2 = st.columns(2)
            d1.download_button("Download SDOF parameters (YAML)", files["sdof_parameters.yaml"],
                               file_name=f"{sd.name}_sdof_parameters.yaml")
            d2.download_button("Download all (zip)", zip_bytes(files), file_name=f"{sd.name}_sdof.zip")


# ============================================================================ SDOF time history
with tab_th:
    sets = load_motion_sets()
    if not ready:
        st.warning("Fix the inputs first: " + (error or s_error or ""))
    elif not sets:
        st.warning("No floor-motion sets: add them to motions/motion_sets.yaml.")
    else:
        sd = current_sdof()
        if sd is None:
            st.info(f"The SDOF time history uses the SDOF of the current inputs (Δc = {settings.sdof_delta_c:g} mm).")
            derive_sdof_button("derive_th")
        else:
            st.write(f"SDOF of **{sd.name}** at Δc = {sd.delta_c:g} mm: Γ = {sd.gamma:.4f}, "
                     f"M_eff = {sd.effective_mass:.3f} t, {len(sd.supports)} springs.")
            if ss.m_set not in sets:
                ss.m_set = next(iter(sets))
            c1, c2, c3 = st.columns([1, 1, 2])
            with c1:
                st.selectbox("Motion set", list(sets), key="m_set", help="Defined in motions/motion_sets.yaml")
                ms = sets[ss.m_set]
                st.caption(ms.description)
                floors = sorted(ms.floors)
                if ss.m_floor not in floors:
                    ss.m_floor = floors[-1]
                st.selectbox("Floor", floors, key="m_floor")
            with c2:
                if ms.levels is not None:
                    ss.m_levels = [lv for lv in ss.m_levels if lv in ms.levels] or [ms.levels[-1]]
                    st.multiselect("Intensity levels", ms.levels, key="m_levels")
            with c3:
                all_rec = st.toggle("All records", value=True, key="th_all")
                recs = None if all_rec else st.multiselect("Records", ms.records, default=ms.records[:2],
                                                           key="th_recs")
            try:
                runs = select_runs(ms, list(ss.m_levels) if ms.levels else None, recs)
            except InputError as exc:
                runs = []
                st.error(str(exc))
            st.caption(f"{len(runs)} analyses (about 0.3 s each).")
            th_sig = sd_sig + signature(ms.name, str(runs), str(ss.m_floor), dump_yaml(settings.sdof_time_history))
            if st.button("Run SDOF time histories", type="primary", disabled=not runs):
                try:
                    model = SDOFModel.from_parameters(sd)
                    ss.th_result = (model, run_remote(sdof_time_history_job, model, ms.name, runs, int(ss.m_floor),
                                                      settings, label="Analysis"))
                    ss.th_sig = th_sig
                except Exception as exc:  # noqa: BLE001
                    st.error(f"Analysis failed: {exc}")
            if ss.get("th_result"):
                model, resp = ss.th_result
                if ss.th_sig != th_sig:
                    st.info("Inputs or selection changed since this run; results refer to the previous run.")
                phi = max(model.support_phi)
                df = pd.DataFrame([{"level": r.level, "record": r.record, "peak u_SDOF (mm)": r.peak_u,
                                    "peak support displacement (mm)": model.gamma * phi * r.peak_u,
                                    "completed": r.completed} for r in resp])
                bad = int((~df.completed).sum())
                if bad:
                    st.warning(f"{bad} analysis/es stopped before the end of the record.")
                ycol = "peak support displacement (mm)"
                fig = go.Figure()
                if df.level.notna().any() and df.level.nunique() > 1:
                    fig.add_trace(go.Scatter(x=df.level, y=df[ycol], mode="markers", name="records",
                                             marker=dict(color=C_MAIN, opacity=0.45, size=7), text=df.record))
                    med = df.groupby("level")[ycol].median()
                    fig.add_trace(go.Scatter(x=med.index, y=med.values, mode="lines+markers", name="median",
                                             line=dict(color=C_BRACE, width=3)))
                    fig.update_layout(xaxis_title="Intensity level")
                else:
                    fig.add_trace(go.Bar(x=df.record.astype(str), y=df[ycol], marker_color=C_MAIN))
                    fig.update_layout(xaxis_title="Record", xaxis_type="category")
                fig.update_layout(height=360, margin=dict(l=10, r=10, t=10, b=10), yaxis_title=ycol,
                                  legend=dict(orientation="h", y=1.1))
                st.plotly_chart(fig, width="stretch")
                st.caption("Peak support displacement = Γ · max φ · peak u_SDOF (largest support demand).")
                with st.expander("Results table"):
                    st.dataframe(df, hide_index=True, width="stretch")
                st.download_button("Download peaks (CSV)", df.to_csv(index=False), file_name=f"{model.name}_sdof_peaks.csv")

                with_hist = [i for i, r in enumerate(resp) if len(r.u)]
                if with_hist:
                    i = st.selectbox("Response history", with_hist,
                                     format_func=lambda i: f"record {resp[i].record}"
                                     + ("" if resp[i].level is None else f", IM{resp[i].level}"))
                    r = resp[i]
                    h1, h2 = st.columns(2)
                    f1 = go.Figure(go.Scatter(x=r.time, y=r.u, line=dict(color=C_MAIN, width=1)))
                    f1.update_layout(height=300, margin=dict(l=10, r=10, t=30, b=10), title="SDOF displacement",
                                     xaxis_title="Time (s)", yaxis_title="u (mm)")
                    h1.plotly_chart(f1, width="stretch")
                    f2 = go.Figure(go.Scatter(x=r.u, y=r.force / 1e3, line=dict(color=C_BRACE, width=1)))
                    f2.update_layout(height=300, margin=dict(l=10, r=10, t=30, b=10), title="Hysteresis",
                                     xaxis_title="u (mm)", yaxis_title="Force (kN)")
                    h2.plotly_chart(f2, width="stretch")
                    st.dataframe(pd.DataFrame(support_demands(model, r.peak_u)), hide_index=True, width="stretch")
                    st.caption("Support demands: peak displacement Γ·φ·u and its ratio to the trapeze envelope "
                               "deformations ePd1-ePd4.")
                else:
                    st.caption("Response histories are kept for batches of up to 100 analyses.")


# ============================================================================ 3D verification
def node_plan(model3d, nodes, peaks, title):
    xy = model3d.node_coords()
    fig = go.Figure(go.Scatter(
        x=[xy[n][0] / 1e3 for n in nodes], y=[xy[n][1] / 1e3 for n in nodes], mode="markers",
        marker=dict(size=11, color=peaks, colorscale="Viridis", showscale=True,
                    colorbar=dict(title="mm", thickness=12)),
        text=[f"node {n}: {p:.2f} mm" for n, p in zip(nodes, peaks)], hoverinfo="text"))
    fig.update_layout(height=340, margin=dict(l=10, r=10, t=30, b=10), title=title, xaxis_title="x (m)",
                      yaxis_title="y (m)")
    fig.update_yaxes(scaleanchor="x", scaleratio=1)
    return fig


with tab_3d:
    models = list_models3d()
    paired = {n: m for n, m in load_motion_sets().items() if m.record_pairs}
    if not ready:
        st.warning("Fix the inputs first: " + (error or s_error or ""))
    elif not models or not paired:
        st.warning("Needs 3D models in inputs/models3d/ and a motion set with record pairs.")
    else:
        st.caption("Full 3D model of a paper archetype under a bidirectional floor motion, compared with the "
                   "reduced-order model of each direction (systems of inputs/archetypes/, SDOF at the Δc of "
                   "the Settings tab, default trapezes).")
        default = model3d_for_system(system.name) if system else None
        c1, c2, c3, c4 = st.columns(4)
        name3d = c1.selectbox("3D model", models, index=models.index(default) if default in models else 0)
        set3d = c2.selectbox("Motion set ", list(paired))
        ms3 = paired[set3d]
        level3d = c3.selectbox("Intensity level", ms3.levels, index=len(ms3.levels) - 1) if ms3.levels else None
        floor3d = c4.selectbox("Floor ", sorted(ms3.floors), index=len(ms3.floors) - 1)
        c5, c6 = st.columns(2)
        pairs = ms3.pairs()
        k = c5.selectbox("Ground motion", range(len(pairs)), format_func=lambda i: f"{i + 1}: {pairs[i][0]} / {pairs[i][1]}")
        flip = c6.radio("Orientation", ["x ← first component", "x ← second component"], horizontal=True) != \
            "x ← first component"
        rx, ry = pairs[k][::-1] if flip else pairs[k]
        st.caption(f"x ← {rx}, y ← {ry}. One run takes about 30 s for M01–M03 and several minutes for the "
                   "larger models.")
        if st.button("Run 3D verification", type="primary"):
            try:
                ss.v3_result = run_remote(verification_job, name3d, set3d, rx, ry, level3d, int(floor3d), settings,
                                          label="3D analysis")
            except Exception as exc:  # noqa: BLE001
                st.error(f"Analysis failed: {exc}")
        res3 = ss.get("v3_result")
        if res3 is not None:
            r = res3.response
            m3 = load_model3d(r.model)
            (st.success if r.completed else st.error)(
                f"{r.model}: x ← {r.record_x}, y ← {r.record_y}"
                + ("" if r.level is None else f", IM{r.level}")
                + (" — completed." if r.completed else f" — stopped at {r.end_time:.3f} of {r.duration:.3f} s."))
            rows = []
            at_braced = braced_peaks(m3, r)
            for d, peaks in (("x", r.peak_x), ("y", r.peak_y)):
                at_braces = at_braced[d]
                row = {"direction": d, "3D max peak, all nodes (mm)": peaks.max(),
                       "3D max peak at braced nodes (mm)": at_braces}
                p = res3.rom.get(d)
                if p is not None:
                    row.update({"ROM system": p.system, "Γ": p.gamma, "max φ": p.phi_max, "SDOF peak u (mm)": p.peak_u,
                                "ROM Γ·φ·u (mm)": p.peak_support_displacement,
                                "ROM / 3D (braced nodes)": p.peak_support_displacement / at_braces})
                rows.append(row)
            st.dataframe(pd.DataFrame(rows), hide_index=True, width="stretch")
            st.caption("'3D max peak at braced nodes' is the measure stored in the paper's Results/ "
                       "(DispX, DispY): the largest peak displacement over the braced nodes of the 3D model.")
            st.caption(f"3D periods: {', '.join(f'{T:.4f}' for T in r.periods)} s.")
            p1, p2 = st.columns(2)
            p1.plotly_chart(node_plan(m3, r.nodes_x, r.peak_x, "Peak displacement in x"), width="stretch")
            p2.plotly_chart(node_plan(m3, r.nodes_y, r.peak_y, "Peak displacement in y"), width="stretch")
            d = st.radio("History of node", ["x", "y"], horizontal=True, key="v3_dir")
            nodes, u = (r.nodes_x, r.ux) if d == "x" else (r.nodes_y, r.uy)
            peaks = r.peak_x if d == "x" else r.peak_y
            n = st.selectbox("Node", nodes, index=int(np.argmax(peaks)))
            f = go.Figure(go.Scatter(x=r.time, y=u[:, nodes.index(n)], line=dict(color=C_MAIN, width=1)))
            f.update_layout(height=300, margin=dict(l=10, r=10, t=10, b=10), xaxis_title="Time (s)",
                            yaxis_title=f"u_{d} (mm)")
            st.plotly_chart(f, width="stretch")
            csv = pd.DataFrame([{"direction": "x", "node": a, "peak": b} for a, b in zip(r.nodes_x, r.peak_x)]
                               + [{"direction": "y", "node": a, "peak": b} for a, b in zip(r.nodes_y, r.peak_y)])
            st.download_button("Download 3D peaks (CSV)", csv.to_csv(index=False), file_name=f"{r.model}_3d_peaks.csv")
