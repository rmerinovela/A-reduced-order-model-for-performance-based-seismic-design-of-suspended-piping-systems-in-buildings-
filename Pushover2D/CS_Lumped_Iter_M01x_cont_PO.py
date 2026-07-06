import openseespy.opensees as op
import numpy as np
from matplotlib import pyplot as plt
from Functions import*

#Lumped orthogonal line


# ------------------------------------------------------------
# Parameters
# ------------------------------------------------------------

Lpipe  = 18000
npipes = 3
Dext = 127
Dint = 113
E = 210000
G = 81000.0
rho = 7.85e-9

# Stiff spring coordinates (user input)
#x_stiff_user = np.array([4000.0, 13000.0])
x0_soft =1000
soft_spacing = 3000

# NEW: stiff hangers defined by mask (0/1)
# Example mask — must be defined by you
stiff_mask = np.array([
    0,1,0,1,0,1
], dtype=int)
# ------------------------------------------------------------
# Orthogonal branches (generalized)
# ------------------------------------------------------------
x_ortho_user         = np.array([18000])
L_ortho_user         = np.array([36000])
n_ortho_pipes_user   = np.array([3])
n_ortho_springs_user = np.array([4])

n_orth = len(x_ortho_user)


# ------------------------------------------------------------
# Initial assumed shape
# ------------------------------------------------------------
# Number of soft hangers
x_soft = x0_soft + soft_spacing * np.arange(len(stiff_mask))
n_hangers = len(x_soft)

# Initial assumed shape (all DOFs = 1)
d0 = np.ones(n_hangers + n_orth)


# ------------------------------------------------------------
# Define pushover displacement steps
# ------------------------------------------------------------
dc_vec = np.linspace(0.1, 50.0, 50)   # example: 20 steps

# Storage list for all results
results = []

# ------------------------------------------------------------
# Initial shape for the FIRST step
# ------------------------------------------------------------
d_init_current = d0.copy()

# ------------------------------------------------------------
# Loop over displacement steps
# ------------------------------------------------------------
for dc in dc_vec:

    print(f"\n--- Running pushover step: Δc = {dc:.3f} ---")
    (
        d_star,
        uy,
        mode1,
        x_nodes_sorted,   # FE x-coordinates sorted
        x_springs,
        x_stiff_out,
        x_d,              # DOF coordinates (unsorted)
        Gamma,
        M_eff,
        Vb,
        mass_ratio,
        order,            # FE sorting index
        f_push,
    ) = iterate_shape_from_static(
        d_init=d0,
        Delta=dc,
        max_iter=50,
        tol=1e-3,

        x0_soft=x0_soft,
        soft_spacing=soft_spacing,
        stiff_mask=stiff_mask,

        # main-line parameters
        Lpipe=Lpipe,
        Dext=Dext,
        Dint=Dint,
        npipes=npipes,
        E=E,
        G=G,
        rho=rho,

        # generalized orthogonal inputs
        x_ortho_user=x_ortho_user,
        L_ortho_user=L_ortho_user,
        n_ortho_pipes_user=n_ortho_pipes_user,
        n_ortho_springs_user=n_ortho_springs_user,
    )
    

    # --------------------------------------------------------
    # Update initial guess for next step
    # --------------------------------------------------------
    d_init_current = d_star.copy()

    # --------------------------------------------------------
    # Scaled displaced shape
    # --------------------------------------------------------
    d_scaled = dc * d_star

    # Value at the maximum-x DOF (last DOF)
    ref = d_scaled[-1]

    # --------------------------------------------------------
    # Normalized displaced shape
    # --------------------------------------------------------
    d_norm = d_scaled / ref

    # --------------------------------------------------------
    # Equivalent SDOF displacement
    # --------------------------------------------------------
    u_sdof = dc / (Gamma*np.max(d_norm))

    # --------------------------------------------------------
    # Build one row of results:
    # [dc, Gamma, M_eff, Vb, mass_ratio, u_sdof, d_norm..., d_scaled...]
    # --------------------------------------------------------
    row = (
        [dc, Gamma, M_eff, Vb, mass_ratio, u_sdof]
        + list(d_norm)
        + list(d_scaled)
        + list(f_push)
    )

    results.append(row)


# ------------------------------------------------------------
# Convert to array and write to txt file (no headers)
# ------------------------------------------------------------
results_arr = np.array(results, float)

np.savetxt(
    "pushover_results_M01x.txt",
    results_arr,
    fmt="%.3f",
)