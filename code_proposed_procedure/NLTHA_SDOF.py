#Piping system layout without branches
# N, mm, s
import openseespy.opensees as op
import os
import numpy as np
import sys



def extract_support_displacements(d_dof, stiff_mask, n_orth):
    """
    Extract displaced-shape values at:
    - stiff hangers (from stiff_mask)
    - orthogonals (last n_orth DOFs)

    Parameters
    ----------
    d_dof : array-like
        Displaced shape in DOF order.
    stiff_mask : array-like of 0/1
        Mask for hanger DOFs only (length = n_hangers).
    n_orth : int
        Number of orthogonal DOFs at the end of d_dof.

    Returns
    -------
    d_supports : np.ndarray
        Displacements at stiff hangers + orthogonals.
    """

    d_dof = np.asarray(d_dof)
    stiff_mask = np.asarray(stiff_mask, dtype=bool)

    n_hangers = len(stiff_mask)

    # 1. Stiff hanger displacements
    d_stiff = d_dof[:n_hangers][stiff_mask]

    # 2. Orthogonal displacements (last n_orth DOFs)
    if n_orth > 0:
        d_orth = d_dof[-n_orth:]
        return np.concatenate([d_stiff, d_orth])
    else:
        return d_stiff

def build_pinching_material(mat_id, pf, pd, nf, nd, rDispP, rForceP, uForceP,
                            rDispN, rForceN, uForceN,
                            gK, gKLim, gD, gDLim, gF, gFLim, gE, dmgType):
    op.uniaxialMaterial(
        'Pinching4', mat_id,
        pf[0], pd[0], pf[1], pd[1], pf[2], pd[2], pf[3], pd[3],
        nf[0], nd[0], nf[1], nd[1], nf[2], nd[2], nf[3], nd[3],
        rDispP, rForceP, uForceP,
        rDispN, rForceN, uForceN,
        gK[0], gK[1], gK[2], gK[3], gKLim,
        gD[0], gD[1], gD[2], gD[3], gDLim,
        gF[0], gF[1], gF[2], gF[3], gFLim,
        gE, dmgType
    )
    return mat_id



op.wipe()

print('Model generation started...')

nt = 4
floor = 4


data = np.load(f"./Results/EquivStatic/equiv_static_nT{nT}_nL{nL}.npz")

nT        = int(data["nT"])
nL        = int(data["nL"])
dc        = float(data["dc"])
Gamma     = float(data["Gamma"])
Meff     = float(data["M_eff"])
u_sdof    = float(data["u_sdof"])
nDOF      = int(data["nDOF"])
n_ortho     = int(data["nOrth"])
d_norm    = data["d_norm"]
stiff_mask = data["stiff_mask"]

DispShape = extract_support_displacements(d_norm, stiff_mask, n_ortho)

direc = './Results/NLTHA/SDOF_nT'+str(int(nT))+'_nL'+str(int(nL))

if(os.path.isdir(direc)==False):
    os.makedirs(direc)


for gm in range(150):
    
    op.model('basic', '-ndm', 2, '-ndf', 3) 

    nodefix = 1
    nodefree = 2
    
    mass = [Meff, Meff, 0] 
    
    op.node(nodefix, 0.0, 0.0)
    op.node(nodefree, 0.0, 0.0, '-mass', *mass)

    op.fix(nodefix, 1, 1, 1)

    #SteelTnd Stiff PR
    #parameters for C-TPS-L
    LePf1 = 600 #floating point values defining force points on the positive response envelope
    LePf2  = 7500.0 #floating point values defining force points on the positive response envelope
    LePf3 = 10000.0 #floating point values defining force points on the positive response envelope
    LePf4 = 11500.0 #floating point values defining force points on the positive response envelope
    LePd1 = 0.1 #floating point values defining deformation points on the positive response envelope
    LePd2 = 12.0 #floating point values defining deformation points on the positive response envelope
    LePd3 = 24.0 #floating point values defining deformation points on the positive response envelope
    LePd4 = 61.0 #floating point values defining deformation points on the positive response envelope
    LeNf1 = -600.0 #floating point values defining force points on the negative response envelope
    LeNf2 = -7500.0 #floating point values defining force points on the negative response envelope
    LeNf3 = -10000.0 #floating point values defining force points on the negative response envelope
    LeNf4 = -11500.0 #floating point values defining force points on the negative response envelope
    LeNd1 = -0.1 #floating point values defining deformation points on the negative response envelope
    LeNd2 = -12 #floating point values defining deformation points on the negative response envelope
    LeNd3 = -24 #floating point values defining deformation points on the negative response envelope
    LeNd4 = -61.0 #floating point values defining deformation points on the negative response envelope
    LrDispP = 0.1 #floating point value defining the ratio of the deformationTt which reloading occurs to the maximum historic deformation demand
    LrForceP = 0.45 #floating point value defining the ratio of the forceTt which reloading begins to force corresponding to the maximum historic deformation demand
    LuForceP = -0.4 #floating point value defining the ratio of strength developed upon unloading from negative load to the maximum strength developed under monotonic loading
    LrDispN = 0.1 #floating point value defining the ratio of the deformationTt which reloading occurs to the minimum historic deformation demand
    LrForceN = 0.45 #floating point value defining the ratio of the forceTt which reloading begins to force corresponding to the minimum historic deformation demand
    LuForceN = -0.4 #floating point value defining the ratio of strength developed upon unloading from negative load to the minimum strength developed under monotonic loading
    LgK1 = 0.0 #floating point values controlling cyclic degradation model for unloading stiffness degradation
    LgK2 = 0.0 #floating point values controlling cyclic degradation model for unloading stiffness degradation
    LgK3 = 0.0 #floating point values controlling cyclic degradation model for unloading stiffness degradation
    LgK4 = 0.0 #floating point values controlling cyclic degradation model for unloading stiffness degradation
    LgKLim = 0.0 #floating point values controlling cyclic degradation model for unloading stiffness degradation
    LgD1 = 0.0 #floating point values controlling cyclic degradation model for reloading stiffness degradation
    LgD2 = 0.0 #floating point values controlling cyclic degradation model for reloading stiffness degradation
    LgD3 = 0.0 #floating point values controlling cyclic degradation model for reloading stiffness degradation
    LgD4 = 0.0 #floating point values controlling cyclic degradation model for reloading stiffness degradation
    LgDLim = 0.0 #floating point values controlling cyclic degradation model for reloading stiffness degradation
    LgF1 = 0.0 #floating point values controlling cyclic degradation model for strength degradation
    LgF2 = 0.0 #floating point values controlling cyclic degradation model for strength degradation
    LgF3 = 0.0 #floating point values controlling cyclic degradation model for strength degradation
    LgF4 = 0.0 #floating point values controlling cyclic degradation model for strength degradation
    LgFLim = 0.0 #floating point values controlling cyclic degradation model for strength degradation
    LgE = 10.0 #floating point value used to define maximum energy dissipation under cyclic loading. Total energy dissipation capacity is definedTs this factor multiplied by the energy dissipated under monotonic loading.
    LdmgType = "cycle" #string to indicate type of damage (option: "cycle", "energy"		

    #parameters for C-TPS-T
    TePf1 = 600 #floating point values defining force points on the positive response envelope
    TePf2 = 6000 #floating point values defining force points on the positive response envelope
    TePf3 = 9000 #floating point values defining force points on the positive response envelope
    TePf4 = 9100 #floating point values defining force points on the positive response envelope
    TePd1 = 0.1 #floating point values defining deformation points on the positive response envelope
    TePd2 = 10.0 #floating point values defining deformation points on the positive response envelope
    TePd3 = 17.0 #floating point values defining deformation points on the positive response envelope
    TePd4 = 36.0 #floating point values defining deformation points on the positive response envelope
    TeNf1 = -600 #floating point values defining force points on the negative response envelope
    TeNf2 = -6000 #floating point values defining force points on the negative response envelope
    TeNf3 = -9000 #floating point values defining force points on the negative response envelope
    TeNf4 = -9100 #floating point values defining force points on the negative response envelope
    TeNd1 = -0.1 #floating point values defining deformation points on the negative response envelope
    TeNd2 = -10.0 #floating point values defining deformation points on the negative response envelope
    TeNd3 = -17.0 #floating point values defining deformation points on the negative response envelope
    TeNd4 = -36.0 #floating point values defining deformation points on the negative response envelope
    TrDispP = 0.1 #floating point value defining the ratio of the deformationTt which reloading occurs to the maximum historic deformation demand
    TrForceP = 0.4 #floating point value defining the ratio of the forceTt which reloading begins to force corresponding to the maximum historic deformation demand
    TuForceP = -0.3 #floating point value defining the ratio of strength developed upon unloading from negative load to the maximum strength developed under monotonic loading
    TrDispN = 0.1 #floating point value defining the ratio of the deformationTt which reloading occurs to the minimum historic deformation demand
    TrForceN = 0.4 #floating point value defining the ratio of the forceTt which reloading begins to force corresponding to the minimum historic deformation demand
    TuForceN = -0.3 #floating point value defining the ratio of strength developed upon unloading from negative load to the minimum strength developed under monotonic loading
    TgK1 = 0.0 #floating point values controlling cyclic degradation model for unloading stiffness degradation
    TgK2 = 0.0 #floating point values controlling cyclic degradation model for unloading stiffness degradation
    TgK3 = 0.0 #floating point values controlling cyclic degradation model for unloading stiffness degradation
    TgK4 = 0.0 #floating point values controlling cyclic degradation model for unloading stiffness degradation
    TgKLim = 0.0 #floating point values controlling cyclic degradation model for unloading stiffness degradation
    TgD1 = 0.0 #floating point values controlling cyclic degradation model for reloading stiffness degradation
    TgD2 = 0.0 #floating point values controlling cyclic degradation model for reloading stiffness degradation
    TgD3 = 0.0 #floating point values controlling cyclic degradation model for reloading stiffness degradation
    TgD4 = 0.0 #floating point values controlling cyclic degradation model for reloading stiffness degradation
    TgDLim = 0.0 #floating point values controlling cyclic degradation model for reloading stiffness degradation
    TgF1 = 0.0 #floating point values controlling cyclic degradation model for strength degradation
    TgF2 = 0.0 #floating point values controlling cyclic degradation model for strength degradation
    TgF3 = 0.0 #floating point values controlling cyclic degradation model for strength degradation
    TgF4 = 0.0 #floating point values controlling cyclic degradation model for strength degradation
    TgFLim = 0.0 #floating point values controlling cyclic degradation model for strength degradation
    TgE = 10.0 #floating point value used to define maximum energy dissipation under cyclic loading. Total energy dissipation capacity is definedTs this factor multiplied by the energy dissipated under monotonic loading.
    TdmgType = "cycle" #string to indicate type of damage (option: "cycle", "energy"


    matLong = []

    nL_per_ortho = nL / n_ortho   # distribute longitudinal strength

    for j in range(n_ortho):

        disp_j = DispShape[-n_ortho + j]   # DOF displacement at orthogonal j

        pf_long = [nL_per_ortho * LePf1,
                   nL_per_ortho * LePf2,
                   nL_per_ortho * LePf3,
                   nL_per_ortho * LePf4]

        pd_long = [LePd1/(Gamma*disp_j),
                   LePd2/(Gamma*disp_j),
                   LePd3/(Gamma*disp_j),
                   LePd4/(Gamma*disp_j)]

        nf_long = [nL_per_ortho * LeNf1,
                   nL_per_ortho * LeNf2,
                   nL_per_ortho * LeNf3,
                   nL_per_ortho * LeNf4]

        nd_long = [LeNd1/(Gamma*disp_j),
                   LeNd2/(Gamma*disp_j),
                   LeNd3/(Gamma*disp_j),
                   LeNd4/(Gamma*disp_j)]

        mat_id = 10 + j   # longitudinal IDs: 10, 11, 12, ...

        matLong.append(
            build_pinching_material(
                mat_id,
                pf_long, pd_long,
                nf_long, nd_long,
                LrDispP, LrForceP, LuForceP,
                LrDispN, LrForceN, LuForceN,
                [LgK1, LgK2, LgK3, LgK4], LgKLim,
                [LgD1, LgD2, LgD3, LgD4], LgDLim,
                [LgF1, LgF2, LgF3, LgF4], LgFLim,
                LgE, LdmgType
            )
        )



    matTran = []

    for i in range(nT):

        disp_i = DispShape[i]   # DOF displacement at transverse support i

        pf_tran = [TePf1, TePf2, TePf3, TePf4]
        pd_tran = [TePd1/(Gamma*disp_i),
                   TePd2/(Gamma*disp_i),
                   TePd3/(Gamma*disp_i),
                   TePd4/(Gamma*disp_i)]

        nf_tran = [TeNf1, TeNf2, TeNf3, TeNf4]
        nd_tran = [TeNd1/(Gamma*disp_i),
                   TeNd2/(Gamma*disp_i),
                   TeNd3/(Gamma*disp_i),
                   TeNd4/(Gamma*disp_i)]

        mat_id = 20 + i   # transverse IDs: 20, 21, 22, ...

        matTran.append(
            build_pinching_material(
                mat_id,
                pf_tran, pd_tran,
                nf_tran, nd_tran,
                TrDispP, TrForceP, TuForceP,
                TrDispN, TrForceN, TuForceN,
                [TgK1, TgK2, TgK3, TgK4], TgKLim,
                [TgD1, TgD2, TgD3, TgD4], TgDLim,
                [TgF1, TgF2, TgF3, TgF4], TgFLim,
                TgE, TdmgType
            )
        )

    matTot = 1000
    op.uniaxialMaterial('Parallel', matTot, *matLong, *matTran)
    
    matRig = 4
    op.uniaxialMaterial('Elastic', matRig, 10e12)
    
    op.element(
    'zeroLength', 1,
    nodefix, nodefree,
    '-mat', matTot, matRig, matRig,
    '-dir', 1, 2, 3
    )

    
    W = Meff*9805

    op.timeSeries('Constant', 1)
    op.pattern('Plain', 1, 1)

    op.load(nodefree, 0, W, 0)

    #Analysis command for static analysis

    op.constraints('Transformation')			
    op.numberer('RCM')				
    op.system('BandGeneral')			
    op.test('NormDispIncr', 1.0e-8, 200)
    op.algorithm('Newton')				
    NstepGravity = 10 # number of steps
    DGravity =  1.0/NstepGravity # load increment
    op.integrator('LoadControl', DGravity)		
    op.analysis('Static')					
    ok = op.analyze(NstepGravity)

    op.loadConst('-time', 0.0) # maintain constant gravity loads and reset time to zero

    if(ok == 0):
        print("Gravity Loads were successfully applied to the Model!")
    else:
        print("Gravity Loads could not be applied to the Model!")
    

    omega = []
    freq =  []
    T = []

    lamb = op.eigen(1)


    for lam in lamb:
        omega.append((lam)**0.5)
        freq.append((lam)**0.5/(2*np.pi))
        T.append((2*np.pi)/(lam)**0.5)

    for t in range(len(T)):
        print('T'+str(t+1)+' = '+str(T[t])+' s')
        
    
    xDamp = 0.02					# damping ratio
    MpropSwitch = 0.0
    KcurrSwitch = 1.0
    KcommSwitch = 0.0
    KinitSwitch = 0.0

    alphaM = MpropSwitch*xDamp*(2*omega[0]) # M-prop. damping; D = alphaM*M
    betaKcurr = KcurrSwitch*2*xDamp/(omega[0])        	# current-K;      +beatKcurr*KCurrent
    betaKcomm = KcommSwitch*2*xDamp/(omega[0])   		# last-committed K;   +betaKcomm*KlastCommitt
    betaKinit = KinitSwitch*2*xDamp/(omega[0])         # initial-K;     +beatKinit*Kini

    op.rayleigh(alphaM, betaKcurr, betaKinit, betaKcomm)   

    #Run Dynamic Nonlinear time history analysis 
    print('Running NLTH Analysis, GM '+str(gm+1)+'...')


    facc = np.loadtxt('C:/Users/rmeri/Documents/UCL/Surrogate_Modelling/RCFrames/ResultsS'+str(nt)+'/FloorAcc_'+str(gm+1)+'.txt')


    print('Running Floor '+str(floor)+'...')
    acc = 1000*facc[:,floor]
    dts = facc[0,0]

    Npts = len(acc)

    dta = dts
    TmaxAnalysis = dts*Npts
    GMfatt =  1

    IDLoadTag = 100
    IDTimeSeries = 1000


    #Define time series
    op.timeSeries('Path',IDTimeSeries,'-dt',dts,'-values',*acc,'-factor',GMfatt,'-prependZero')


    op.recorder('EnvelopeNode', '-file', direc+'/Disp_GM'+str(gm+1)+'_Floor'+str(floor)+'.txt', '-time', '-node', nodefree, '-dof', 1, 'disp')

    #Define load pattern
    op.pattern('UniformExcitation',IDLoadTag,1,'-accel',IDTimeSeries)



    Tol = 1e-8                          # convergence tolerance for test
    op.wipeAnalysis()
    op.integrator('Newmark', 0.5, 0.25) # determine the next time step for an analysis
    op.numberer('RCM')                  # renumber dof's to minimize band-width (optimization), if you want to
    op.system('BandGeneral')            # how to store and solve the system of equations in the analysis
    op.constraints('Plain')             # how it handles boundary conditions
    op.test('EnergyIncr', Tol, 50)      # determine if convergence has been achieved at the end of an iteration step
    op.algorithm('Newton')              # use Newton
    op.analysis('Transient') # define type of analysis static or transient

    ok =  op.analyze(Npts, dta)         # actually perform analysis; returns ok=0 if analysis was successful

    if(ok != 0):                    # analysis was not successful.
        # --------------------------------------------------------------------------------------------------
        # change some analysis parameters to achieve convergence
        # performance is slower inside this loop
        #    Time-controlled analysis
        ok = 0
        controlTime = op.getTime()
        while(controlTime < TmaxAnalysis and ok == 0):
            controlTime = op.getTime()
            ok = op.analyze(1, dta)
            if(ok != 0):
                print("Trying Newton with Initial Tangent ..")
                op.test('EnergyIncr', 1.0e-6, 100000, 0)
                op.algorithm('Newton', '-initial')
                ok = op.analyze(1, dta)
                op.test('EnergyIncr', Tol, 50)
                op.algorithm('Newton')
            if(ok != 0):
                print("Trying Broyden ..")
                op.test('EnergyIncr', 1.0e-6, 100000,  0)
                op.algorithm('Broyden', 8)
                ok = op.analyze(1, dta)
                op.algorithm('Newton')
            if(ok != 0):
                print("Trying NewtonWithLineSearch ..")
                op.algorithm('NewtonLineSearch', 0.8)
                ok = op.analyze(1, dta)
                op.algorithm('Newton')
            if(ok != 0):
                print("Trying KrylovNewton ..")
                op.algorithm('KrylovNewton') 
                ok = op.analyze(1, dta)
                op.algorithm('Newton')      

    print("Floor Motion Done. End Time:"+str(op.getTime()))
    op.wipe()
