import openseespy.opensees as op
import numpy as np

def build_model(
        n_elem=10,
        Lpipe=6000,
        Dext=127,
        Dint=113,
        npipes=1,
        E=210000.0,
        G=81000.0,
        rho=7.85e-9,

        x0_soft=1000.0,          # first soft hanger location
        soft_spacing=3000.0,     # spacing between soft hangers
        stiff_mask=None,         # 0/1 vector selecting stiff hangers

        Delta=1.0,
        d=None,

        # general orthogonals along the main line
        x_ortho_user=None,
        L_ortho_user=None,
        n_ortho_pipes_user=None,
        n_ortho_springs_user=None,

        alpha=1.0,
        use_initial_k=False
):
    # --------------------------------------------------------
    # Trilinear stiffness envelopes (unchanged numerically)
    # --------------------------------------------------------

    # Transverse (T)
    d1_T, d2_T = 10.0, 17.0
    F1_T, F2_T = 6000.0, 9000.0
    k1_T = F1_T / d1_T
    k2_T = (F2_T - F1_T) / (d2_T - d1_T)
    k3_T = 0.01 * k1_T

    # Longitudinal (L)
    d1_L, d2_L = 12.0, 24.0
    F1_L, F2_L = 7500.0, 11500.0
    k1_L = F1_L / d1_L
    k2_L = (F2_L - F1_L) / (d2_L - d1_L)
    k3_L = 0.01 * k1_L


    def trilinear_keff(disp, k1, k2, k3, d1, d2):
        """
        Returns the secant stiffness F/disp for a trilinear spring.
        Fully consistent with your original implementation.
        """
        d_abs = abs(disp)

        # Avoid division by zero
        if d_abs <= 1e-12:
            return k1

        # Force at first and second breakpoints
        F1 = k1 * d1
        F2 = F1 + k2 * (d2 - d1)

        # Piecewise force
        if d_abs <= d1:
            F = k1 * d_abs
        elif d_abs <= d2:
            F = F1 + k2 * (d_abs - d1)
        else:
            F = F2 + k3 * (d_abs - d2)

        return F / d_abs
    # --------------------------------------------------------
    # BASIC CHECKS AND INPUT PARSING
    # --------------------------------------------------------
    op.wipe()
    op.model('basic', '-ndm', 3, '-ndf', 6)

    # d must always be provided
    if d is None:
        raise ValueError("Shape vector d must be provided.")

    # Orthogonal inputs → ensure arrays
    x_ortho_user         = np.array([] if x_ortho_user is None else x_ortho_user, dtype=float)
    L_ortho_user         = np.array([] if L_ortho_user is None else L_ortho_user, dtype=float)
    n_ortho_pipes_user   = np.array([] if n_ortho_pipes_user is None else n_ortho_pipes_user, dtype=int)
    n_ortho_springs_user = np.array([] if n_ortho_springs_user is None else n_ortho_springs_user, dtype=int)

    n_orth = len(x_ortho_user)

    # Validate orthogonal input lengths
    if not (len(L_ortho_user) == len(n_ortho_pipes_user) == len(n_ortho_springs_user) == n_orth):
        raise ValueError("All orthogonal input vectors must have the same length.")

    # Convert shape vector
    d = np.array(d, dtype=float)

    # --------------------------------------------------------
    # Build hanger grid (ALL hangers: soft + stiff)
    # --------------------------------------------------------
    if x0_soft > Lpipe - 1000.0:
        raise ValueError(
            f"First hanger at {x0_soft} must be at least 1 m from the right end."
        )

    # Maximum number of intervals that keep last hanger ≥ 1 m from right end
    Nmax = int((Lpipe - 1000.0 - x0_soft) // soft_spacing)

    x_soft = []
    for i in range(Nmax + 1):
        xi = x0_soft + i * soft_spacing
        if xi <= Lpipe - 1000.0 + 1e-6:
            x_soft.append(xi)

    x_soft = np.array(x_soft, dtype=float)
    n_soft = len(x_soft)
    x_soft_all = x_soft.copy()   # preserve ALL hangers

    # --------------------------------------------------------
    # Validate stiff_mask and compute stiff/soft subsets
    # --------------------------------------------------------
    if stiff_mask is None:
        raise ValueError("stiff_mask must be provided under Option A.")

    stiff_mask = np.array(stiff_mask, dtype=int)
    
    print(">>> stiff_mask INSIDE build_model =", stiff_mask)
    print(">>> sum(stiff_mask) =", stiff_mask.sum())
    print(">>> stiff_indices =", np.where(stiff_mask == 1)[0])
    print(">>> n_soft =", n_soft)

    if len(stiff_mask) != n_soft:
        raise ValueError(
            f"stiff_mask length {len(stiff_mask)} does not match number of hangers {n_soft}."
        )

    if not np.all((stiff_mask == 0) | (stiff_mask == 1)):
        raise ValueError("stiff_mask must contain only 0s and 1s.")

    # Compute stiff and soft hanger coordinates
    x_stiff_user = x_soft[stiff_mask == 1]
    x_soft_user  = x_soft[stiff_mask == 0]

    n_stiff = int(stiff_mask.sum())
    line_stiff_nodes = [None] * n_stiff

    # --------------------------------------------------------
    # Collision check — orthogonals vs stiff hangers
    # --------------------------------------------------------
    tol = 1e-2
    for xo in x_ortho_user:
        if np.any(np.abs(x_stiff_user - xo) < tol):
            raise ValueError(
                f"Orthogonal location x={xo} coincides with a stiff hanger. "
                "This configuration is not allowed."
            )

    n_hangers = n_soft
    n_dof = n_hangers + n_orth

    # Shape vector length check (updated)
    if len(d) < n_dof:
        raise ValueError(
            f"Shape vector d must have length at least {n_dof} "
            f"(= {n_hangers} hangers + {n_orth} orthogonals)."
        )
        
    # --------------------------------------------------------
    # Section and mass properties
    # --------------------------------------------------------
    A  = npipes * np.pi * ((Dext/2)**2 - (Dint/2)**2)
    Aw = npipes * np.pi * ((Dint/2)**2)

    J  = npipes*np.pi/2*((Dext/2)**4 - (Dint/2)**4)
    Iy = npipes*np.pi/4*((Dext/2)**4 - (Dint/2)**4)
    Iz = Iy

    mass_per_length  = rho * A
    mass_per_lengthw = (rho/7.8) * Aw
    mL_total = 1.35*(mass_per_length + mass_per_lengthw)

    # --------------------------------------------------------
    # Materials
    # --------------------------------------------------------
    op.uniaxialMaterial('Elastic', 4,   1e12)   # rigid
    op.uniaxialMaterial('Elastic', 99,  1e-6)   # very soft


    # --------------------------------------------------------
    # MESH CREATION FOR MAIN LINE (NO rotational hinges)
    # --------------------------------------------------------
    
    # Keep the full hanger list for the main-line mesh and spring creation
    x_soft = x_soft_all.copy()       # ALL hangers (soft + stiff)
    x_stiff = x_stiff_user.copy()    # stiff hangers only
    x_soft_user = x_soft_user.copy() # soft hangers only

    n_springs = len(x_soft_user)     # number of soft hangers (if needed elsewhere)

    tol_snap = 1e-3   # snapping tolerance (m)

    # 1. Start with pipe start only
    x_coords_list = [0.0]

    # 2. Add ALL hanger locations (soft + stiff)
    #    Under Option A, x_soft contains ALL hangers.
    x_coords_list.extend(list(x_soft))

    # 3. Add pipe end
    x_coords_list.append(Lpipe)

    # 4. Process orthogonals: snap to existing main-line nodes if close; otherwise add as new
    for j in range(n_orth):
        x_ortho = float(x_ortho_user[j])

        candidates = np.array(x_coords_list, float)
        diffs = np.abs(candidates - x_ortho)
        idx_min = np.argmin(diffs)

        if diffs[idx_min] < tol_snap:
            # snap to existing node
            x_snap = candidates[idx_min]
            x_ortho_user[j] = x_snap
        else:
            # add new node
            x_coords_list.append(x_ortho)

    # 5. Finalize main-line x-coordinates
    x_coords = np.unique(np.round(np.array(x_coords_list, float), 6))
    x_coords = np.sort(x_coords)

    # --------------------------------------------------------
    # Geometric transformation
    # --------------------------------------------------------
    op.geomTransf('Linear', 1, 0.0, 0.0, 1.0)

    # --------------------------------------------------------
    # MAIN LINE: nodes, masses, beam chain (NO rotational hinges)
    # --------------------------------------------------------

    base  = 0
    tol_x = 1e-6   # geometric tolerance for matching x-positions

    # --------------------------------------------------------
    # Create main-line nodes at x_coords
    # --------------------------------------------------------
    line_node_tags = []
    for i, x in enumerate(x_coords):
        tag = base + 100 + i
        op.node(tag, x, 0.0, 0.0)
        line_node_tags.append(tag)

    line_node_coords = np.array([op.nodeCoord(nd)[0] for nd in line_node_tags], float)

    # Enforce monotonic main line
    idx_sort         = np.argsort(line_node_coords)
    line_node_coords = line_node_coords[idx_sort]
    line_node_tags   = [line_node_tags[i] for i in idx_sort]
    x_coords         = line_node_coords.copy()

    # Main-line end node (x = Lpipe)
    nd_main_end = line_node_tags[-1]

    # Main-line nodes at each orthogonal attach point (for FE connectivity only)
    nd_main_ortho = []
    for j in range(n_orth):
        x_ortho = x_ortho_user[j]
        diffs   = np.abs(line_node_coords - x_ortho)
        idx_closest = np.argmin(diffs)
        nd_main_ortho.append(line_node_tags[idx_closest])

   # --------------------------------------------------------
    # Determine which x-positions should carry FE mass
    # --------------------------------------------------------
    mass_positions = set()

    # All hangers (soft + stiff)
    for xs in x_soft:
        mass_positions.add(xs)

    # Orthogonal joints
    for j in range(n_orth):
        mass_positions.add(x_ortho_user[j])

    # Pipe start and end
    mass_positions.add(0.0)
    mass_positions.add(Lpipe)

    # --------------------------------------------------------
    # Compute tributary lengths for each FE node
    # --------------------------------------------------------
    elem_lengths = np.diff(x_coords)
    L_trib       = np.zeros_like(x_coords)

    for i in range(len(x_coords)):
        if i == 0:
            L_trib[i] = 0.5 * elem_lengths[0]
        elif i == len(x_coords) - 1:
            L_trib[i] = 0.5 * elem_lengths[-1]
        else:
            L_trib[i] = 0.5 * (elem_lengths[i-1] + elem_lengths[i])

    # --------------------------------------------------------
    # Assign FE nodal masses
    # --------------------------------------------------------
    nodal_masses = np.zeros_like(x_coords)

    for i, x in enumerate(x_coords):
        tag = line_node_tags[i]

        is_mass_node = any(abs(x - xm) < tol_x for xm in mass_positions)
        if not is_mass_node:
            continue

        nodal_masses[i] = L_trib[i] * mL_total
        op.mass(tag, nodal_masses[i], nodal_masses[i], 0, 0, 0, 0)

    # --------------------------------------------------------
    # Create beam-column elements (continuous chain, no hinge skips)
    # --------------------------------------------------------
    beam_base = 1000

    for i in range(len(line_node_tags) - 1):
        op.element('elasticBeamColumn',
                   base + beam_base + i,
                   line_node_tags[i], line_node_tags[i+1],
                   A, E, G, J, Iy, Iz, 1)



    # --------------------------------------------------------
    # Stiff spring tangent stiffnesses (now based on hanger DOFs)
    # --------------------------------------------------------

    # DOF layout (new):
    #   d[0 : n_hangers]      → all hangers (soft + stiff), in hanger order
    #   d[n_hangers : ...]    → orthogonals
    n_hangers = n_soft
    d_hanger  = d[:n_hangers]          # displacement at each hanger DOF

    stiff_indices = np.where(stiff_mask == 1)[0]   # hanger indices that are stiff
    n_stiff       = len(stiff_indices)

    stiff_kT = np.zeros(n_stiff)
    for j, i_hanger in enumerate(stiff_indices):
        # i_hanger = global hanger index (0..n_hangers-1)
        # j        = local stiff-hanger index (0..n_stiff-1)
        Di = Delta * d_hanger[i_hanger]
        stiff_kT[j] = trilinear_keff(Di, k1_T, k2_T, k3_T, d1_T, d2_T)

    # --------------------------------------------------------
    # Hangers: top node, bottom node, zeroLength spring
    # --------------------------------------------------------
    x_springs         = []
    line_stiff_nodes  = [None] * n_stiff        # FE nodes for stiff hangers
    line_hanger_nodes = np.zeros(n_hangers, int)  # FE nodes for ALL hangers
    nd_bottom_support = []

    tol_x = 1e-6

    # --------------------------------------------------------
    # Mapping: hanger index i → stiff index j (or -1 if soft)
    # --------------------------------------------------------
    hanger_to_stiff = -np.ones(n_hangers, dtype=int)   # default: soft hanger
    hanger_to_stiff[stiff_indices] = np.arange(n_stiff)

    for i, xs in enumerate(x_soft):

        # 1. Find the main-line node at xs
        idx_candidates = np.where(np.abs(x_coords - xs) < tol_x)[0]
        if len(idx_candidates) == 0:
            raise RuntimeError(
                f"No main-line node found at hanger location x={xs}. "
                "This should never happen because x_soft is inserted into the mesh."
            )

        idx_node  = int(idx_candidates[0])
        beam_node = line_node_tags[idx_node]

        # 2. Top support node (fixed)
        top = base + 400 + i
        op.node(top, xs, 0.0, 10.0)
        op.fix(top, 1,1,1,1,1,1)

        # 3. Bottom hanger node (rigid-linked to beam)
        bot = base + 500 + i
        op.node(bot, xs, 0.0, 5.0)
        op.rigidLink('beam', beam_node, bot)

        x_springs.append(xs)
        nd_bottom_support.append(top)

        # 4. Store FE node for ALL hangers (soft + stiff)
        line_hanger_nodes[i] = bot

        # 5. Assign stiff or soft material
        j = hanger_to_stiff[i]   # -1 if soft, 0..n_stiff-1 if stiff

        if j >= 0:
            # This hanger is stiff → use tangent stiffness stiff_kT[j]
            line_stiff_nodes[j] = bot

            mat_id = base + 600 + i
            op.uniaxialMaterial('Elastic', mat_id, stiff_kT[j])
            mat_x = mat_id
            mat_y = mat_id
        else:
            # Soft hanger → dummy material
            mat_x = 99
            mat_y = 99

        # 6. Create hanger zeroLength spring
        op.element(
            'zeroLength', base + 700 + i,
            top, bot,
            '-mat', mat_x, mat_y, 4,4,4,4,
            '-dir', 1,2,3,4,5,6
        )
        
    
    # --------------------------------------------------------
    # Orthogonals (generalized: any number, anywhere along main line)
    # --------------------------------------------------------

    # Lumped masses and stiffnesses per orthogonal
    m_ortho_lump = np.zeros(n_orth, dtype=float)
    k_ortho_lump = np.zeros(n_orth, dtype=float)

    # DOF nodes and support nodes per orthogonal
    nd_ortho_start   = [None] * n_orth   # orthogonal branch nodes (at y=Loff, z=0)
    nd_ortho_support = [None] * n_orth   # vertical support nodes (at y=Loff, z=z_top)

    Loff  = 1000.0
    z_bot = 5.0
    z_top = 10.0

    eid_global     = 600000   # base element tag for orthogonals
    MAT_ORTHO_BASE = 2100     # base material tag for orthogonal springs

    for j in range(n_orth):

        L_j  = float(L_ortho_user[j])
        np_j = int(n_ortho_pipes_user[j])
        ns_j = int(n_ortho_springs_user[j])
        x_j  = float(x_ortho_user[j])

        # Skip if this orthogonal is effectively absent
        if L_j <= 0.0 or np_j <= 0 or ns_j <= 0 or alpha <= 0.0:
            continue

        # (1) main-line node at x = x_j (already identified earlier)
        nd_main_j = nd_main_ortho[j]   # at (x_j, 0, 0)

        # ------------------------------------------------------------
        # (2) orthogonal branch start node at (x_j, Loff, 0)
        # ------------------------------------------------------------
        nd_start_j = 920100 + j
        op.node(nd_start_j, x_j, Loff, 0.0)

        # rigid tee offset: short beam from main line to branch start
        op.element('elasticBeamColumn', eid_global,
                   nd_main_j, nd_start_j,
                   A, E, G, J, Iy, Iz, 1)
        eid_global += 1

        # ------------------------------------------------------------
        # (3) compute lumped mass and stiffness of orthogonal j
        # ------------------------------------------------------------
        A_ortho_j  = np_j * np.pi * ((Dext/2)**2 - (Dint/2)**2)
        Aw_ortho_j = np_j * np.pi * ((Dint/2)**2)

        mL_steel_j = rho * A_ortho_j
        mL_water_j = (rho/7.8) * Aw_ortho_j
        mL_total_j = 1.35*(mL_steel_j + mL_water_j)

        # lumped mass
        m_ortho_lump[j] = alpha * mL_total_j * L_j

        # ------------------------------------------------------------
        # OLD-CODE-COMPATIBLE stiffness evaluation
        # Use the orthogonal DOF displacement, not the main-line DOF
        # ------------------------------------------------------------

        #   d[0 : n_hangers]           → all hangers
        #   d[n_hangers : ...]         → orthogonals
        i_ortho   = n_hangers + j
        d_elbow_j = d[i_ortho]


        # evaluate tangent stiffness at orthogonal DOF displacement
        u_elbow_j = Delta * d_elbow_j
        kL_unit_j = trilinear_keff(u_elbow_j, k1_L, k2_L, k3_L, d1_L, d2_L)

        # lumped stiffness
        k_ortho_lump[j] = alpha * ns_j * kL_unit_j

        mat_tag_j = MAT_ORTHO_BASE + j
        op.uniaxialMaterial('Elastic', mat_tag_j, k_ortho_lump[j])

        # ------------------------------------------------------------
        # (4) vertical support node and spring chain
        # ------------------------------------------------------------
        nd_support_j = 930100 + j
        op.node(nd_support_j, x_j, Loff, z_top)
        op.fix(nd_support_j, 1,1,1,1,1,1)

        nd_bottom_j = 940100 + j
        op.node(nd_bottom_j, x_j, Loff, z_bot)

        # rigid link: branch start → bottom spring node
        op.rigidLink('beam', nd_start_j, nd_bottom_j)

        # zero-length spring: bottom → top
        op.element('zeroLength', eid_global,
                   nd_bottom_j, nd_support_j,
                   '-mat', mat_tag_j,
                   '-dir', 2)
        eid_global += 1

        # ------------------------------------------------------------
        # (5) lumped mass at orthogonal branch node
        # ------------------------------------------------------------
        op.mass(nd_start_j, 0, m_ortho_lump[j], 0, 0, 0, 0)

        # bookkeeping
        nd_ortho_start[j]   = nd_start_j
        nd_ortho_support[j] = nd_support_j
    
    
    
    # --------------------------------------------------------
    # Eigen (diagnostic)
    # --------------------------------------------------------

    # DOF layout (new):
    #   1) all hanger DOFs (soft + stiff), in hanger order
    #   2) all orthogonal DOFs, in orthogonal order

    # 1. Hanger DOF nodes (bottom nodes)
    dof_hanger_nodes = [base + 500 + i for i in range(n_hangers)]

    # 2. Orthogonal DOF nodes (branch start nodes)
    dof_ortho_nodes = list(nd_ortho_start)

    # Combined DOF node list
    dof_node_tags = dof_hanger_nodes + dof_ortho_nodes
    dof_node_tags = [int(nd) for nd in dof_node_tags]

    # Compute eigenvectors
    op.eigen(2)
    mode1 = np.array([op.nodeEigenvector(nd, 1, 2) for nd in dof_node_tags])
    
    # ------------------------------------------------------------
    # DOF location and mass vector (correct tributary logic)
    # ------------------------------------------------------------

    n_hangers = n_soft
    n_dof     = n_hangers + n_orth

    m_d = np.zeros(n_dof)

    # ------------------------------------------------------------
    # 1. HANGER DOF MASSES (take FE mass at hanger node)
    # ------------------------------------------------------------

    m_hanger = np.zeros(n_hangers)

    for i, xs in enumerate(x_soft):
        idx = np.where(np.abs(x_coords - xs) < 1e-9)[0]
        if len(idx) == 0:
            raise RuntimeError(f"No FE node found at hanger x = {xs}")
        m_hanger[i] = nodal_masses[idx[0]]

    # ------------------------------------------------------------
    # 2. ORTHOGONAL DOF MASSES (take FE mass at the actual FE node)
    # ------------------------------------------------------------

    m_ortho = np.zeros(n_orth)

    for j, xo in enumerate(x_ortho_user):
        idx = np.where(np.abs(x_coords - xo) < 1e-9)[0]
        if len(idx) == 0:
            raise RuntimeError(f"No FE node found at orthogonal x = {xo}")
        m_ortho[j] = nodal_masses[idx[0]]

    # ------------------------------------------------------------
    # 3. Assemble DOF mass vector
    # ------------------------------------------------------------

    m_d[:n_hangers] = m_hanger
    m_d[n_hangers:] = m_ortho
    
    
    # --------------------------------------------------------
    # 1) Main-line base shear from stiff springs
    # --------------------------------------------------------

    V_main_springs = 0.0

    # stiff_indices[i] = hanger index of stiff hanger i
    for i in range(n_stiff):
        i_hanger = stiff_indices[i]      # hanger index in 0..n_hangers-1
        d_i = d[i_hanger]                # DOF displacement of this stiff hanger
        u_i = Delta * d_i
        V_main_springs += stiff_kT[i] * u_i


    # --------------------------------------------------------
    # 2) Orthogonal base shear and redistribution (PASS SHEAR)
    # --------------------------------------------------------

    V_ortho_tot  = np.zeros(n_orth)
    V_stay_ortho = np.zeros(n_orth)
    V_pass_ortho = np.zeros(n_orth)

    # Neighbour set for tributary logic:
    #   - pipe ends
    #   - stiff hangers
    #   - orthogonals
    x_support = np.sort(
        np.concatenate([
            np.array([0.0, Lpipe], dtype=float),
            x_stiff.copy(),
            x_ortho_user.copy()
        ])
    )

    tol_x = 1e-9

    for j in range(n_orth):

        # ----------------------------------------------------
        # 1) Total orthogonal base shear
        # ----------------------------------------------------
        i_ortho = n_hangers + j
        d_j     = d[i_ortho]
        u_j     = Delta * d_j
        V_ortho_tot[j] = k_ortho_lump[j] * u_j

        xj = float(x_ortho_user[j])

        # ----------------------------------------------------
        # 2) Find nearest neighbours (left/right)
        # ----------------------------------------------------
        left_supports  = x_support[x_support <= xj + tol_x]
        right_supports = x_support[x_support >= xj - tol_x]

        xL_sup = left_supports[-1]  if len(left_supports)  > 0 else x_support[0]
        xR_sup = right_supports[0] if len(right_supports) > 0 else x_support[-1]

        # If orthogonal coincides with a support, use previous/next
        if abs(xL_sup - xR_sup) < tol_x:
            idx_sup = np.where(np.abs(x_support - xj) < tol_x)[0][0]
            if idx_sup == 0:
                xL_sup = x_support[0]
                xR_sup = x_support[1]
            elif idx_sup == len(x_support) - 1:
                xL_sup = x_support[-2]
                xR_sup = x_support[-1]
            else:
                xL_sup = x_support[idx_sup - 1]
                xR_sup = x_support[idx_sup + 1]

        # ----------------------------------------------------
        # 3) Midpoint tributary window (MATCHES BLOCK 6)
        # ----------------------------------------------------
        x_mid_L = 0.5 * (xL_sup + xj)
        x_mid_R = 0.5 * (xj + xR_sup)

        # ----------------------------------------------------
        # 4) Main-line tributary mass (soft hangers + node)
        # ----------------------------------------------------
        m_main_pass_j = 0.0

        # soft hangers inside midpoint window
        for xs in x_soft:
            if x_mid_L <= xs <= x_mid_R:
                idx = np.where(np.abs(x_coords - xs) < tol_x)[0][0]
                m_main_pass_j += nodal_masses[idx]

        # orthogonal node mass (main-line node)
        idx_ortho = np.where(np.abs(x_coords - xj) < tol_x)[0][0]
        m_main_pass_j += nodal_masses[idx_ortho]

        # ----------------------------------------------------
        # 5) PASS/STAY split (consistent with Block 6)
        # ----------------------------------------------------
        m_eff_j = m_ortho_lump[j] + m_main_pass_j

        if m_eff_j > 0.0:
            V_pass_ortho[j] = V_ortho_tot[j] * (m_main_pass_j   / m_eff_j)
            V_stay_ortho[j] = V_ortho_tot[j] * (m_ortho_lump[j] / m_eff_j)
        else:
            V_pass_ortho[j] = 0.0
            V_stay_ortho[j] = 0.0
                
        # ------------------------------------------------------------
        # 6) SEGMENT-WISE REDISTRIBUTION OF BASE SHEAR (GENERALIZED)
        # ------------------------------------------------------------

        # Segment boundaries: 0, all orthogonal x-locations, Lpipe
        seg_bounds = sorted(set([0.0] + list(x_ortho_user) + [Lpipe]))

        # DOF coordinates and arrays (NEW convention)
        #   d = [all hangers (soft+stiff) ..., all orthogonals ...]
        x_d = np.zeros(n_dof)
        x_d[:n_hangers] = x_soft
        for j in range(n_orth):
            x_d[n_hangers + j] = x_ortho_user[j]

        d_d = np.array(d, float)
        m_d = m_d

        Fy_full = np.zeros_like(x_d)

        # FE coordinates and masses
        x_fe = x_coords
        m_fe = nodal_masses

        # Neighbour set for tributary logic: ends + stiff + orthogonals
        x_support = np.sort(
            np.concatenate([
                np.array([0.0, Lpipe], dtype=float),
                x_stiff.copy(),
                x_ortho_user.copy()
            ])
        )

        tol_x = 1e-9

    # ------------------------------------------------------------
    # Precompute pass shear (stay/pass + left/right) for each orthogonal
    # ------------------------------------------------------------

    V_pass_left  = np.zeros(n_orth)
    V_pass_right = np.zeros(n_orth)

    for j in range(n_orth):

        xj = float(x_ortho_user[j])

        # 1) Total orthogonal base shear (from orthogonal DOF)
        i_ortho   = n_hangers + j
        d_ortho_j = d_d[i_ortho]
        u_ortho_j = Delta * d_ortho_j
        V_ortho_j = k_ortho_lump[j] * u_ortho_j

        # 2) Find nearest neighbours in x_support (left/right)
        left_supports  = x_support[x_support <= xj + tol_x]
        right_supports = x_support[x_support >= xj - tol_x]

        if len(left_supports) == 0:
            xL_sup = x_support[0]
        else:
            xL_sup = left_supports[-1]

        if len(right_supports) == 0:
            xR_sup = x_support[-1]
        else:
            xR_sup = right_supports[0]

        # If orthogonal coincides with a support, use previous/next
        if abs(xL_sup - xR_sup) < tol_x:
            idx_sup = np.where(np.abs(x_support - xj) < tol_x)[0][0]
            if idx_sup == 0:
                xL_sup = x_support[0]
                xR_sup = x_support[1]
            elif idx_sup == len(x_support) - 1:
                xL_sup = x_support[-2]
                xR_sup = x_support[-1]
            else:
                xL_sup = x_support[idx_sup - 1]
                xR_sup = x_support[idx_sup + 1]

        # Midpoints define tributary window
        x_mid_L = 0.5 * (xL_sup + xj)
        x_mid_R = 0.5 * (xj + xR_sup)

        # 3) Main-line tributary mass for PASS/STAY: soft + node
        m_main_trib_j = 0.0
        for xs in x_soft:
            if x_mid_L <= xs <= x_mid_R:
                idx_fe = np.where(np.abs(x_fe - xs) < tol_x)[0][0]
                m_main_trib_j += m_fe[idx_fe]

        idx_ortho_node    = np.where(np.abs(x_fe - xj) < tol_x)[0][0]
        m_node_ortho_main = m_fe[idx_ortho_node]
        #m_main_trib_j    += m_node_ortho_main

        m_ortho_j = m_ortho_lump[j]
        m_eff_j   = m_ortho_j + m_main_trib_j

        if m_eff_j > 0.0:
            V_pass_j = V_ortho_j * (m_main_trib_j / m_eff_j)
        else:
            V_pass_j = 0.0

        # 4) LEFT/RIGHT split of PASS shear

        # Ends: no left/right split
        if abs(xj - 0.0) < 1e-6:
            V_pass_left[j]  = 0.0
            V_pass_right[j] = V_pass_j
            continue

        if abs(xj - Lpipe) < 1e-6:
            V_pass_left[j]  = V_pass_j
            V_pass_right[j] = 0.0
            continue

        M_L = 0.0
        M_R = 0.0

        for xs in x_soft:
            idx_fe = np.where(np.abs(x_fe - xs) < tol_x)[0][0]
            if x_mid_L <= xs <= xj + tol_x:
                M_L += m_fe[idx_fe]
            if xj - tol_x <= xs <= x_mid_R:
                M_R += m_fe[idx_fe]

        # Split orthogonal-node main-line mass half/half
        M_L += 0.5 * m_node_ortho_main
        M_R += 0.5 * m_node_ortho_main

        if M_L + M_R > 0.0:
            V_pass_left[j]  = V_pass_j * (M_L / (M_L + M_R))
            V_pass_right[j] = V_pass_j * (M_R / (M_L + M_R))
        else:
            V_pass_left[j]  = 0.0
            V_pass_right[j] = 0.0

    # ------------------------------------------------------------
    # Segment-wise redistribution (NEW DOF logic for inertia forces)
    # ------------------------------------------------------------

    for s in range(len(seg_bounds) - 1):

        xL = seg_bounds[s]
        xR = seg_bounds[s + 1]

        mask_dof = (x_d >= xL - 1e-6) & (x_d <= xR + 1e-6)
        idx_seg  = np.where(mask_dof)[0]
        if len(idx_seg) == 0:
            continue

        V_seg = 0.0

        # (a) local stiff-spring shear
        for i in range(n_stiff):
            x_stiff_i = x_stiff_user[i]
            if xL <= x_stiff_i <= xR:
                i_hanger = stiff_indices[i]
                d_i = d_d[i_hanger]
                V_seg += stiff_kT[i] * (Delta * d_i)

        # (b) pass shear from orthogonals at segment boundaries
        
        for j in range(n_orth):
            xj = x_ortho_user[j]
            if abs(xj - xL) < 1e-6:
                V_seg += V_pass_right[j]
            if abs(xj - xR) < 1e-6:
                V_seg += V_pass_left[j]

        # (c) redistribute within segment
        md_seg = m_d[idx_seg] * d_d[idx_seg]
        denom  = np.sum(md_seg)
        if denom < 1e-12:
            continue

        dF_seg = V_seg * md_seg / denom
        Fy_full[idx_seg] += dF_seg
    
    print("\n================ DOF DIAGNOSTICS ================")

    print("\nDOF coordinates (x_d):")
    for i, x in enumerate(x_d):
        print(f"  DOF {i:2d}: x = {x:10.3f}")

    print("\nShape vector d:")
    for i, val in enumerate(d_d):
        print(f"  d[{i:2d}] = {val:12.6f}")

    print("\nMass vector m_d:")
    for i, val in enumerate(m_d):
        print(f"  m[{i:2d}] = {val:12.6f}")

    print("\nRedistributed shear Fy:")
    for i, val in enumerate(Fy_full):
        print(f"  Fy[{i:2d}] = {val:12.6f}")

    print("=================================================\n")

       
    # ------------------------------------------------------------
    # 6) Extract loads at orthogonals and stay components
    # ------------------------------------------------------------

    # DOF layout:
    #   0 .. n_hangers-1          → all hangers (soft + stiff)
    #   n_hangers .. n_hangers+n_orth-1 → orthogonals

    ortho_dof_positions = np.arange(n_hangers, n_hangers + n_orth, dtype=int)
    Fy_ortho_main       = Fy_full[ortho_dof_positions]   # pass-through on main line
    Fy_ortho_stay       = V_stay_ortho.copy()            # stay part on branch

    # ------------------------------------------------------------
    # 7) Apply loads
    # ------------------------------------------------------------
    op.timeSeries('Constant', 100)
    op.pattern('Plain', 100, 100)

   
    # (A) ALL hangers (soft + stiff): DOF i → FE node line_hanger_nodes[i]
    for i in range(n_hangers):
        nd = int(line_hanger_nodes[i])        # bottom hanger node (rigid-linked to beam)
        Fy = float(Fy_full[i])           # redistributed shear at hanger DOF i
        if abs(Fy) > 0.0:
            op.load(nd, 0, Fy, 0, 0, 0, 0)

    # (B) Orthogonals — pass-through on main line and stay on branch
    for j in range(n_orth):

        # main-line pass-through load at orthogonal DOF location
        nd_main_j = nd_main_ortho[j]     # FE node on main line for orthogonal j
        Fy_main_j = float(Fy_ortho_main[j])

        if nd_main_j is not None and abs(Fy_main_j) > 0.0:
            op.load(nd_main_j, 0, Fy_main_j, 0, 0, 0, 0)

        # stay part on orthogonal branch node
        nd_ortho_j = nd_ortho_start[j]   # FE node at start of orthogonal branch j
        Fy_stay_j  = float(Fy_ortho_stay[j])

        if nd_ortho_j is not None and abs(Fy_stay_j) > 0.0:
            op.load(nd_ortho_j, 0, Fy_stay_j, 0, 0, 0, 0)

    # --------------------------------------------------------
    # Static analysis
    # --------------------------------------------------------
    op.constraints('Transformation')
    op.numberer('RCM')
    op.system('BandGeneral')
    op.test('NormDispIncr', 1e-8, 50)
    op.algorithm('Newton')
    op.integrator('LoadControl', 1.0)
    op.analysis('Static')
    op.analyze(1)

    # ------------------------------------------------------------
    # 7) Participation factor, effective mass, global base shear
    # ------------------------------------------------------------

    # DOF shape and mass vectors in the new order
    d_all = d_d.copy()     # [d_stiff..., d_ortho...]
    m_all = m_d.copy()     # tributary main-line masses
    d_all = d_all/d_all[-1]
    # Add orthogonal lumped masses to the orthogonal DOFs
    for j in range(n_orth):
        k = n_hangers + j     # DOF index of orthogonal j
        m_all[k] += m_ortho_lump[j]
    
    f_push = np.zeros(len(d_all))
    
    # Participation factor
    num = np.sum(m_all * d_all)
    den = np.sum(m_all * d_all * d_all)
    Gamma = num / den if den > 0 else 0.0
    
    for i in range(len(f_push)):
        f_push[i] = (m_all[i]*d_all[i])/num
    
    # Effective modal mass
    M_eff = Gamma * num

    # Global base shear = redistributed main-line forces + stay forces
    Vb = np.sum(Fy_full) + np.sum(V_stay_ortho)

    # ------------------------------------------------------------
    # Modal mass ratio (generalized)
    # ------------------------------------------------------------

    # Total modal mass = main-line modal masses + orthogonal lumped masses
    M_total = np.sum(m_d) + np.sum(m_ortho_lump)

    mass_ratio = M_eff / M_total if M_total > 0 else 0.0

    
    # ------------------------------------------------------------
    # 6) Extract results (new DOF architecture)
    # ------------------------------------------------------------

    # DOF ordering (NEW):
    #   0 .. n_hangers-1              → all hangers (soft + stiff)
    #   n_hangers .. n_hangers+n_orth-1 → orthogonals

    # Build DOF → FE node mapping in the NEW order
    #   First all hangers (soft + stiff), then orthogonals
    dof_node_tags = list(dof_hanger_nodes) + list(nd_main_ortho)

    # FE displacements at DOF nodes (new DOF order)
    uy_array = np.array([op.nodeDisp(nd, 2) for nd in dof_node_tags])

    # FE x-coordinates at DOF nodes
    x_nodes = np.array([op.nodeCoord(nd)[0] for nd in dof_node_tags])

    # Sorted x for plotting only
    order = np.argsort(x_nodes)
    x_nodes_sorted = x_nodes[order]

    # Output stiff hanger and spring coordinates
    x_springs   = np.array(x_springs, dtype=float)
    x_stiff_out = x_stiff_user.copy()
    

    return (
        uy_array,          # FE displacements in DOF order (new)
        mode1,             # modal shape in DOF order (new)
        x_nodes_sorted,    # sorted FE x for plotting
        x_springs,         # spring locations
        x_stiff_out,       # stiff hanger locations
        x_d,               # DOF coordinates (new architecture)
        Gamma,             # participation factor
        M_eff,             # effective modal mass
        Vb,                # global base shear
        mass_ratio,        # modal mass ratio
        order,             # sorting index for plotting
        f_push,
    )
    
def normalize_shape(phi):
    max_abs = np.max(np.abs(phi))
    if max_abs == 0:
        return phi
    return phi / max_abs


def iterate_shape_from_static(
    d_init,
    Delta=1.0,
    max_iter=100,
    tol=1e-3,
    x0_soft=1000.0,
    soft_spacing=3000.0,
    stiff_mask=None,
    **model_kwargs
):

    # ------------------------------------------------------------
    # Normalize initial shape BEFORE first build_model()
    # ------------------------------------------------------------
    d_curr = normalize_shape(np.array(d_init, float))

    # ------------------------------------------------------------
    # First call: get DOF ordering and initial FE response
    # ------------------------------------------------------------
    (
        uy,
        mode1,
        x_nodes_sorted,
        x_springs,
        x_stiff_out,
        x_d,
        Gamma,
        M_eff,
        Vb,
        mass_ratio,
        order,
        f_push,
    ) = build_model(
        Delta=Delta,
        d=d_curr,
        x0_soft=x0_soft,
        soft_spacing=soft_spacing,
        stiff_mask=stiff_mask,
        **model_kwargs
    )

    # ------------------------------------------------------------
    # DOF count from returned DOF ordering
    # ------------------------------------------------------------
    ndof = len(uy)     # uy is FE displacement at DOF nodes (new DOF order)

    # ------------------------------------------------------------
    # Iteration loop
    # ------------------------------------------------------------
    for it in range(max_iter):

        (
            uy,
            mode1,
            x_nodes_sorted,
            x_springs,
            x_stiff_out,
            x_d,
            Gamma,
            M_eff,
            Vb,
            mass_ratio,
            order,
            f_push,
        ) = build_model(
            Delta=Delta,
            d=d_curr,
            x0_soft=x0_soft,
            soft_spacing=soft_spacing,
            stiff_mask=stiff_mask,
            **model_kwargs
        )

        # FE displacement at DOF nodes (already in DOF order)
        u_samples = uy.copy()

        # Normalize → new shape
        d_new = normalize_shape(u_samples)

        # Convergence check
        diff = np.linalg.norm(d_new - d_curr) / np.sqrt(ndof)
        print(f"Iteration {it}: diff = {diff:.4e}")

        if diff < tol:
            print("Converged (static shape).")
            d_curr = d_new
            break

        d_curr = d_new

    else:
        print("WARNING: did not converge within max_iter.")

    return (
        d_curr,            # final DOF-order shape
        uy,                # FE displacements at DOF nodes
        mode1,             # modal shape (DOF order)
        x_nodes_sorted,    # sorted FE x for plotting
        x_springs,
        x_stiff_out,
        x_d,               # DOF coordinates
        Gamma,
        M_eff,
        Vb,
        mass_ratio,
        order,             # plotting index
        f_push,
    )
 