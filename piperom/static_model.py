"""Equivalent static analysis of the reduced model (Section 3 of the paper).

For an assumed normalised shape ``d`` and a target displacement ``delta`` this module:

1. builds the OpenSees model of the main line (elastic beam on hangers), with braced hangers given
   the trapeze secant stiffness at ``delta * d`` and each branch lumped into one mass/spring DOF;
2. turns the brace and branch forces implied by the shape into an inertial load pattern;
3. solves the linear static problem and returns the displacements at the DOFs, together with the
   modal participation factor, effective mass and base shear.

``iterate_shape`` repeats this until the displaced shape is consistent with the assumed one.

This is a restructured port of ``build_model``/``iterate_shape_from_static`` in
``code implementation for paper/Pushover2D/Functions.py``: modelling, OpenSees tags, command order and arithmetic are unchanged.

DOF order: all hangers by position, then branches in input order. The last branch is the
reference DOF used to normalise the shape when computing Gamma.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field

import numpy as np
import openseespy.opensees as op

from .inputs import ResolvedSystem

# OpenSees tags (as in the original code)
MAIN_NODE, HANGER_TOP, HANGER_BOTTOM = 100, 400, 500
HANGER_MAT, HANGER_ELE, BEAM_ELE = 600, 700, 1000
BRANCH_START, BRANCH_SUPPORT, BRANCH_BOTTOM = 920100, 930100, 940100
BRANCH_ELE, BRANCH_MAT = 600000, 2100
MAT_RIGID, MAT_SOFT, TRANSF = 4, 99, 1

RIGID_STIFFNESS = 1e12
SOFT_STIFFNESS = 1e-6       # lateral stiffness of unbraced (gravity-only) hangers
BRANCH_OFFSET = 1000.0      # y-offset of the lumped branch node
Z_BOTTOM, Z_TOP = 5.0, 10.0
SNAP_TOL = 1e-3             # branch snaps onto an existing main-line node closer than this
X_TOL = 1e-6
MASS_TOL = 1e-9


@dataclass
class SolverSettings:
    """Convergence test of each static solve (values from the analysis settings)."""

    test: str
    tolerance: float
    max_iterations: int


@dataclass
class StaticStep:
    """Result of one linear static solve for an assumed shape."""

    u: np.ndarray               # displacement at each DOF (DOF order)
    dof_x: np.ndarray           # DOF x-coordinate (branches after snapping)
    dof_mass: np.ndarray        # main-line mass at each DOF
    branch_mass: np.ndarray     # lumped branch masses
    loads: np.ndarray           # redistributed main-line load at each DOF
    branch_stay_load: np.ndarray
    brace_stiffness: np.ndarray       # secant stiffness of each braced hanger
    branch_stiffness: np.ndarray      # lumped branch stiffness
    gamma: float
    effective_mass: float
    total_mass: float
    mass_ratio: float
    base_shear: float
    f_push: np.ndarray


@dataclass
class ShapeResult:
    d_star: np.ndarray          # converged shape, normalised to max |d| = 1
    step: StaticStep            # last static solve
    iterations: int
    converged: bool
    history: list[float] = field(default_factory=list)


def normalize_shape(phi: np.ndarray) -> np.ndarray:
    max_abs = np.max(np.abs(phi))
    if max_abs == 0:
        return phi
    return phi / max_abs


def _section(n_pipes, d_ext, d_int):
    A = n_pipes * np.pi * ((d_ext / 2) ** 2 - (d_int / 2) ** 2)
    Aw = n_pipes * np.pi * ((d_int / 2) ** 2)
    J = n_pipes * np.pi / 2 * ((d_ext / 2) ** 4 - (d_int / 2) ** 4)
    I = n_pipes * np.pi / 4 * ((d_ext / 2) ** 4 - (d_int / 2) ** 4)
    return A, Aw, J, I


def _neighbours(x_support: np.ndarray, xj: float, tol: float) -> tuple[float, float]:
    """Nearest supports left/right of xj; if xj is itself a support, the previous/next one."""
    left = x_support[x_support <= xj + tol]
    right = x_support[x_support >= xj - tol]
    xL = left[-1] if len(left) > 0 else x_support[0]
    xR = right[0] if len(right) > 0 else x_support[-1]
    if abs(xL - xR) < tol:
        i = np.where(np.abs(x_support - xj) < tol)[0][0]
        if i == 0:
            xL, xR = x_support[0], x_support[1]
        elif i == len(x_support) - 1:
            xL, xR = x_support[-2], x_support[-1]
        else:
            xL, xR = x_support[i - 1], x_support[i + 1]
    return xL, xR


def solve_static_step(rs: ResolvedSystem, d, delta: float, solver: SolverSettings) -> StaticStep:
    d = np.array(d, dtype=float)
    nh, nb = rs.n_hangers, rs.n_branches
    n_dof = nh + nb
    if len(d) < n_dof:
        raise ValueError(f"Shape vector has {len(d)} entries, expected {n_dof}")

    p = rs.pipe
    E, G, rho, rho_f = p.elastic_modulus, p.shear_modulus, p.density, p.effective_fluid_density
    L = rs.length
    alpha = rs.branch_participation
    tri_T, tri_L = rs.transverse_trilinear, rs.longitudinal_trilinear

    x_h = rs.hanger_x
    mask = rs.brace_mask
    brace_idx = np.where(mask == 1)[0]
    n_brace = len(brace_idx)
    x_brace = x_h[mask == 1]
    x_branch = np.array(rs.branch_x, dtype=float)

    op.wipe()
    op.logFile(os.devnull, "-noEcho")   # silence OpenSees (zeroLength length warnings at every solve)
    op.model("basic", "-ndm", 3, "-ndf", 6)

    A, Aw, J, Iy = _section(rs.n_pipes, p.outer_diameter, p.inner_diameter)
    Iz = Iy
    m_per_length = p.mass_factor * (rho * A + rho_f * Aw)

    op.uniaxialMaterial("Elastic", MAT_RIGID, RIGID_STIFFNESS)
    op.uniaxialMaterial("Elastic", MAT_SOFT, SOFT_STIFFNESS)

    # ---------------------------------------------------------------- main-line mesh
    coords = [0.0] + list(x_h) + [L]
    for j in range(nb):
        xo = float(x_branch[j])
        cand = np.array(coords, float)
        diffs = np.abs(cand - xo)
        i_min = np.argmin(diffs)
        if diffs[i_min] < SNAP_TOL:
            x_branch[j] = cand[i_min]
        else:
            coords.append(xo)
    x_coords = np.sort(np.unique(np.round(np.array(coords, float), 6)))

    op.geomTransf("Linear", TRANSF, 0.0, 0.0, 1.0)

    main_nodes = []
    for i, x in enumerate(x_coords):
        op.node(MAIN_NODE + i, x, 0.0, 0.0)
        main_nodes.append(MAIN_NODE + i)

    main_node_at_branch = [main_nodes[int(np.argmin(np.abs(x_coords - x_branch[j])))] for j in range(nb)]

    # lumped masses from tributary lengths (every main-line node is a hanger, branch junction or end)
    elem_len = np.diff(x_coords)
    trib = 0.5 * (np.r_[0.0, elem_len] + np.r_[elem_len, 0.0])
    nodal_mass = trib * m_per_length
    for node, m in zip(main_nodes, nodal_mass):
        op.mass(node, m, m, 0, 0, 0, 0)

    for i in range(len(main_nodes) - 1):
        op.element("elasticBeamColumn", BEAM_ELE + i, main_nodes[i], main_nodes[i + 1],
                   A, E, G, J, Iy, Iz, TRANSF)

    # ---------------------------------------------------------------- hangers
    brace_k = np.zeros(n_brace)
    for j, i_h in enumerate(brace_idx):
        brace_k[j] = tri_T.secant_stiffness(delta * d[i_h])

    hanger_to_brace = -np.ones(nh, dtype=int)
    hanger_to_brace[brace_idx] = np.arange(n_brace)
    hanger_bottom = np.zeros(nh, int)

    for i, xs in enumerate(x_h):
        hit = np.where(np.abs(x_coords - xs) < X_TOL)[0]
        beam_node = main_nodes[int(hit[0])]
        top, bot = HANGER_TOP + i, HANGER_BOTTOM + i
        op.node(top, xs, 0.0, Z_TOP)
        op.fix(top, 1, 1, 1, 1, 1, 1)
        op.node(bot, xs, 0.0, Z_BOTTOM)
        op.rigidLink("beam", beam_node, bot)
        hanger_bottom[i] = bot
        j = hanger_to_brace[i]
        if j >= 0:
            mat = HANGER_MAT + i
            op.uniaxialMaterial("Elastic", mat, brace_k[j])
        else:
            mat = MAT_SOFT
        op.element("zeroLength", HANGER_ELE + i, top, bot,
                   "-mat", mat, mat, MAT_RIGID, MAT_RIGID, MAT_RIGID, MAT_RIGID,
                   "-dir", 1, 2, 3, 4, 5, 6)

    # ---------------------------------------------------------------- branches
    branch_mass = np.zeros(nb)
    branch_k = np.zeros(nb)
    branch_start = [0] * nb
    eid = BRANCH_ELE
    for j in range(nb):
        L_j = float(rs.branch_length[j])
        np_j = int(rs.branch_n_pipes[j])
        ns_j = int(rs.branch_n_braces[j])
        x_j = float(x_branch[j])

        start = BRANCH_START + j
        op.node(start, x_j, BRANCH_OFFSET, 0.0)
        op.element("elasticBeamColumn", eid, main_node_at_branch[j], start, A, E, G, J, Iy, Iz, TRANSF)
        eid += 1

        A_j, Aw_j, _, _ = _section(np_j, p.outer_diameter, p.inner_diameter)
        m_per_length_j = p.mass_factor * (rho * A_j + rho_f * Aw_j)
        branch_mass[j] = alpha * m_per_length_j * L_j
        k_unit = tri_L.secant_stiffness(delta * d[nh + j])
        branch_k[j] = alpha * ns_j * k_unit
        op.uniaxialMaterial("Elastic", BRANCH_MAT + j, branch_k[j])

        support, bottom = BRANCH_SUPPORT + j, BRANCH_BOTTOM + j
        op.node(support, x_j, BRANCH_OFFSET, Z_TOP)
        op.fix(support, 1, 1, 1, 1, 1, 1)
        op.node(bottom, x_j, BRANCH_OFFSET, Z_BOTTOM)
        op.rigidLink("beam", start, bottom)
        op.element("zeroLength", eid, bottom, support, "-mat", BRANCH_MAT + j, "-dir", 2)
        eid += 1

        op.mass(start, 0, branch_mass[j], 0, 0, 0, 0)
        branch_start[j] = start

    # ---------------------------------------------------------------- DOF masses
    def mass_at(x):
        hit = np.where(np.abs(x_coords - x) < MASS_TOL)[0]
        if len(hit) == 0:
            raise RuntimeError(f"No main-line node at x={x}")
        return nodal_mass[hit[0]]

    m_d = np.array([mass_at(x) for x in x_h] + [mass_at(x) for x in x_branch])
    x_d = np.concatenate([x_h, x_branch])

    # ---------------------------------------------------------------- load pattern
    x_support = np.sort(np.concatenate([np.array([0.0, L]), x_brace.copy(), x_branch.copy()]))

    # (i)-(ii) each branch force is split by tributary mass into a part staying on the branch and a
    # part passed to the main line. As in the original code, the junction node mass counts in the
    # "stay" share but not in the "pass" share, so the two don't add up to the branch force.
    stay = np.zeros(nb)
    pass_left = np.zeros(nb)
    pass_right = np.zeros(nb)
    for j in range(nb):
        xj = float(x_branch[j])
        V_j = branch_k[j] * (delta * d[nh + j])
        xL, xR = _neighbours(x_support, xj, MASS_TOL)
        mid_L, mid_R = 0.5 * (xL + xj), 0.5 * (xj + xR)
        m_main = 0.0
        for xs in x_h:
            if mid_L <= xs <= mid_R:
                m_main += mass_at(xs)
        m_node = mass_at(xj)
        m_stay = branch_mass[j] + (m_main + m_node)
        stay[j] = V_j * (branch_mass[j] / m_stay) if m_stay > 0.0 else 0.0
        m_eff = branch_mass[j] + m_main
        V_pass = V_j * (m_main / m_eff) if m_eff > 0.0 else 0.0

        if abs(xj - 0.0) < X_TOL:
            pass_right[j] = V_pass
            continue
        if abs(xj - L) < X_TOL:
            pass_left[j] = V_pass
            continue
        M_L = M_R = 0.0
        for xs in x_h:
            m_s = mass_at(xs)
            if mid_L <= xs <= xj + MASS_TOL:
                M_L += m_s
            if xj - MASS_TOL <= xs <= mid_R:
                M_R += m_s
        M_L += 0.5 * m_node
        M_R += 0.5 * m_node
        if M_L + M_R > 0.0:
            pass_left[j] = V_pass * (M_L / (M_L + M_R))
            pass_right[j] = V_pass * (M_R / (M_L + M_R))

    # (iii) segment-wise redistribution between branch junctions, proportional to m * d
    loads = np.zeros(n_dof)
    seg_bounds = sorted(set([0.0] + list(x_branch) + [L]))
    for s in range(len(seg_bounds) - 1):
        xL, xR = seg_bounds[s], seg_bounds[s + 1]
        idx_seg = np.where((x_d >= xL - X_TOL) & (x_d <= xR + X_TOL))[0]
        if len(idx_seg) == 0:
            continue
        V_seg = 0.0
        for i in range(n_brace):
            if xL <= x_brace[i] <= xR:
                V_seg += brace_k[i] * (delta * d[brace_idx[i]])
        for j in range(nb):
            xj = x_branch[j]
            if abs(xj - xL) < X_TOL:
                V_seg += pass_right[j]
            if abs(xj - xR) < X_TOL:
                V_seg += pass_left[j]
        md_seg = m_d[idx_seg] * d[idx_seg]
        denom = np.sum(md_seg)
        if denom < 1e-12:
            continue
        loads[idx_seg] += V_seg * md_seg / denom

    # ---------------------------------------------------------------- apply loads and solve
    op.timeSeries("Constant", 100)
    op.pattern("Plain", 100, 100)
    for i in range(nh):
        if abs(float(loads[i])) > 0.0:
            op.load(int(hanger_bottom[i]), 0, float(loads[i]), 0, 0, 0, 0)
    for j in range(nb):
        f_main = float(loads[nh + j])
        if abs(f_main) > 0.0:
            op.load(main_node_at_branch[j], 0, f_main, 0, 0, 0, 0)
        if abs(float(stay[j])) > 0.0:
            op.load(branch_start[j], 0, float(stay[j]), 0, 0, 0, 0)

    op.constraints("Transformation")
    op.numberer("RCM")
    op.system("BandGeneral")
    op.test(solver.test, solver.tolerance, solver.max_iterations)
    op.algorithm("Newton")
    op.integrator("LoadControl", 1.0)
    op.analysis("Static")
    if op.analyze(1) != 0:
        raise RuntimeError(f"Static solve failed at delta={delta}")

    # ---------------------------------------------------------------- modal quantities
    d_ref = d / d[-1]
    m_all = m_d.copy()
    m_all[nh:] += branch_mass
    num = np.sum(m_all * d_ref)
    den = np.sum(m_all * d_ref * d_ref)
    gamma = num / den if den > 0 else 0.0
    f_push = (m_all * d_ref) / num
    m_eff = gamma * num
    total_mass = np.sum(m_d) + np.sum(branch_mass)

    dof_nodes = [int(n) for n in hanger_bottom] + main_node_at_branch
    u = np.array([op.nodeDisp(nd, 2) for nd in dof_nodes])

    return StaticStep(
        u=u, dof_x=x_d, dof_mass=m_d, branch_mass=branch_mass, loads=loads,
        branch_stay_load=stay, brace_stiffness=brace_k, branch_stiffness=branch_k,
        gamma=gamma, effective_mass=m_eff, total_mass=total_mass,
        mass_ratio=m_eff / total_mass if total_mass > 0 else 0.0,
        base_shear=np.sum(loads) + np.sum(stay), f_push=f_push,
    )


def iterate_shape(rs: ResolvedSystem, d_init, delta: float, max_iterations: int, tolerance: float,
                  solver: SolverSettings) -> ShapeResult:
    """Fixed-point iteration: assumed shape -> static solve -> normalised displacements -> new shape."""
    d_curr = normalize_shape(np.array(d_init, float))
    n = rs.n_dof
    history: list[float] = []
    converged = False
    step = None
    it = 0
    for it in range(max_iterations):
        step = solve_static_step(rs, d_curr, delta, solver)
        d_new = normalize_shape(step.u.copy())
        diff = np.linalg.norm(d_new - d_curr) / np.sqrt(n)
        history.append(float(diff))
        d_curr = d_new
        if diff < tolerance:
            converged = True
            break
    return ShapeResult(d_star=d_curr, step=step, iterations=it + 1, converged=converged, history=history)
