# Methodology: what the engine computes

This file describes the analyses `piperom` can run, the assumptions they keep from the paper, and their
limits. Units are N, mm, s; masses are in tonnes.

The engine implements the reduced-order model of Merino, Gentile and Galasso, "A reduced-order model
for performance-based seismic design of suspended piping systems in buildings". It changes no modelling
assumption of the paper's code (`code implementation for paper/`); only inputs and outputs differ.

```
system file ──► 1. equivalent static procedure ──► 2. adaptive pseudo-pushover
(one direction)        (at one Δc)                        (Δc = Δc1 … Δcn)
                           │
                           ▼
                  3. equivalent SDOF at a chosen Δc ──► 4. SDOF time history under floor motions
                                                                       │
            5. 3D verification (paper archetypes only) ◄── compared ───┘
```

## The idealised system

A system file describes **one loading direction**:

- **Main line.** A straight pipe bundle (`n_pipes` identical pipes) along x, loaded transversely (y). It's
  modelled as an elastic beam with lumped masses at its nodes:
  - mass per unit length = `mass_factor` × (pipe + contained fluid);
  - defaults: factor 1.35, water = steel density / 7.8.
- **Gravity hangers.** At given positions along the main line:
  - no lateral stiffness;
  - rigid vertically and in rotation.
- **Transverse braces (trapezes).** A subset of the hangers. Each one is a spring in the transverse
  direction (and along the pipe axis, as in the paper's code).
- **Branches.** Straight pipelines orthogonal to the main line, framing into it at a junction and loaded
  along their axis. Each branch is lumped into **one DOF**:
  - its whole mass;
  - `n_braces` longitudinal trapezes in parallel.

  A branch can't coincide with a braced hanger. At least one branch is required: the procedure is
  defined for a main line plus branches.
- **Trapeze behaviour.** One Pinching4 definition per type (transverse, longitudinal), shared by all
  braces of that type. The static procedure uses a trilinear secant idealisation of its positive envelope:
  - origin → envelope point 2 → envelope point 3;
  - then a slope of 1% of the first branch.

**DOFs:** all hangers (by position), then all branches (in input order). The **last branch** is the
reference DOF used to normalise the shape. Γ depends on this choice; the SDOF definition (Γ·φ and the
effective mass) does not.

## 1. Equivalent static procedure (at a target displacement Δc)

For an assumed normalised shape `d` (max |d| = 1):

1. **Stiffness.** Every brace and branch spring gets the secant stiffness of its trilinear backbone at
   displacement Δc·dᵢ.
2. **Loads.** The spring forces implied by the shape become an inertial load pattern:
   - Each branch force splits into a part that stays on the branch and a part passed to the main line,
     by tributary mass: the branch mass against the main-line mass around the junction, junction node
     included. The two parts add up to the branch force. The paper's code left the node mass out of the
     passed part, so the parts didn't add up; `branch_split: legacy` reproduces that
     ([legacy_issues.md](legacy_issues.md), A2).
   - The passed part divides left/right of the junction.
   - Along the main line, between consecutive branch junctions, the total shear is redistributed in
     proportion to mᵢ·dᵢ.
3. **Solve.** A linear static analysis (OpenSees) gives the displaced shape; normalising it gives a new `d`.
4. **Iterate.** Repeat until the RMS change of `d` is below the tolerance (fixed-point iteration).

**Outputs:**
- the converged shape;
- the participation factor Γ = Σmd / Σmd² and the effective mass M_eff = Γ·Σmd (shape normalised to
  the reference DOF);
- the effective-mass ratio and the base shear V_b;
- the equivalent SDOF displacement u_SDOF = Δc / (Γ · max d).

## 2. Adaptive pseudo-pushover

The procedure is repeated for a list of target displacements, Δc = 0.1 … 50 mm by default. Each step
gives one point (u_SDOF, V_b) of the capacity curve, with its own shape: the shape adapts as the braces
soften. By default each step starts from a uniform shape, as in the paper's code (`warm_start: false`).

## 3. Equivalent SDOF

At a user-chosen Δc, from the converged shape:

| Quantity | Value |
|---|---|
| Mass | M_eff |
| Springs (in parallel) | one per support: each braced hanger (1 trapeze) and each branch (`n_braces` trapezes) |
| Spring definition | the support's Pinching4, envelope **deformations divided by Γ·φᵢ**, **forces multiplied by the number of trapezes** |

φᵢ is the shape at the support, normalised to the reference DOF. The SDOF base shear equals the sum of
the support forces, so the SDOF backbone reproduces the system's capacity curve.

## 4. SDOF time history

The SDOF is excited by a floor acceleration history (`motions/`), as in the paper's `NLTHA_SDOF.py`:

- a single zeroLength element with the parallel springs;
- a gravity step (no effect: that DOF is rigid);
- Rayleigh damping, 2% on the current stiffness, from the SDOF period;
- Newmark average-acceleration integration;
- the paper's fallback sequence of solution algorithms.

Outputs:
- the SDOF displacement history (relative to the floor) and the spring force;
- the peak |u|;
- the demand at each support: peak displacement Γ·φᵢ·u_peak, and its ratio to the trapeze envelope
  deformations.

The largest support demand, Γ·max φ·u_peak, is the quantity the paper compares with the 3D model.

## 5. 3D verification (paper archetypes)

The paper's full 3D models are stored unchanged in `inputs/models3d/` and include:
- threaded-joint hysteresis;
- Pinching4 trapezes with failure caps;
- both loading directions at once.

They're analysed under a bidirectional floor motion (the two horizontal components of one ground
motion) with the procedure of the paper's `3D_models` scripts:
- gravity, then Rayleigh damping on modes 1–2 (mass + last-committed stiffness);
- Newmark integration and the same fallbacks.

The reduced-order prediction of each direction (archetype system file, SDOF at the chosen Δc, default
trapezes) is computed under the same component and compared with the paper's measure: **the largest
peak displacement over the braced nodes** of the 3D model.

Only the convergence test differs from some paper scripts. M01–M03 use `RelativeEnergyIncr`, which can't
converge from rest; the default is `EnergyIncr`, as in M29–M63. See
[legacy_issues.md](legacy_issues.md), A6.

## Scope and limits

- **Geometry.** One straight main line plus orthogonal branches, one direction per file. No bends,
  elevation changes, loops, or branches off branches. Branches are lumped (no flexibility, no transverse
  braces of their own) and use the main line's pipe section.
- **Trapezes.** All braces of one type are identical.
- **3D verification.** Available only for the 9 archetypes with a model in `inputs/models3d/`; new 3D
  models can't be generated from a system file.
- **Motions.** Only sets described in `motions/motion_sets.yaml`.
- **Run times** (this machine):

  | Analysis | Time |
  |---|---|
  | Pseudo-pushover (50 steps) | 0.1–4 s |
  | One SDOF time history | about 0.3 s |
  | One 3D run, M01–M03 | about 30 s |
  | One 3D run, M29–M31 | about 4 min |

## Validation against the paper

Full details: [validation.md](validation.md).

| Analysis | Compared with | Result | Report |
|---|---|---|---|
| Pseudo-pushover, 18 archetypes | `Pushover2D/pushover_results_*.txt` | all values identical (3 decimals) | [validation/report.md](../validation/report.md) |
| SDOF parameters | `equivalent_static.py` → `NLTHA_SDOF.py` | identical | [validation/report.md](../validation/report.md) |
| SDOF time history | `Results/*_peak_displacements.npy` | 14 of 18 SDOFs match; M61/M62 not traceable | [validation/timehistory_report.md](../validation/timehistory_report.md) |
| 3D verification | `Results/*_biron_DispX/Y.txt` | reproduced to the stored precision | [validation/timehistory_report.md](../validation/timehistory_report.md) |

The pushover match uses the paper code's inputs: the longitudinal backbone its static code actually
used (11500 N at 24 mm) and its branch-force split. The engine's defaults correct both:
- the trapeze file as published, 10000 N ([legacy_issues.md](legacy_issues.md), A1);
- the consistent split (A2).

Together they change base shears by up to 42% along the curves; per-archetype values are in
`validation/report.md` §4.
