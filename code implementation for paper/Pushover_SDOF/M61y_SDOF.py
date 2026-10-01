#Piping system layout without branches
# N, mm, s
import openseespy.opensees as op
import vfo.vfo as vfo
import os
import numpy as np
import matplotlib.pyplot as plt
import time
import scipy as scp




op.wipe()

print('Model generation started...')

direc = './ResultsM61y_SDOF'

if(os.path.isdir(direc)==False):
    os.mkdir(direc)
    
Analysis_Type = 'CPO'
       
op.model('basic', '-ndm', 2, '-ndf', 3) 

nodefix = 1
nodefree = 2

mass = [21.9, 21.9, 0] 
Gamma = 0.95
DispShape = [0.69,0.79,0.95,0.87,0.87,0.86,1.0,1.39,1.35,1.3,0.87,1]
nT = 10
nL = 12

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

matLong1 = 10
matLong2 = 5
matTran = [20,30,40,50,60,70,80,90,100,110]

op.uniaxialMaterial('Pinching4', matLong1, 0.5*nL*LePf1, LePd1/(Gamma*DispShape[-1]), 0.5*nL*LePf2, LePd2/(Gamma*DispShape[-1]), 0.5*nL*LePf3, LePd3/(Gamma*DispShape[-1]), 0.5*nL*LePf4, LePd4/(Gamma*DispShape[-1]), 
                        0.5*nL*LeNf1, LeNd1/(Gamma*DispShape[-1]), 0.5*nL*LeNf2, LeNd2/(Gamma*DispShape[-1]), 0.5*nL*LeNf3, LeNd3/(Gamma*DispShape[-1]), 0.5*nL*LeNf4, LeNd4/(Gamma*DispShape[-1]), 
                        LrDispP, LrForceP, LuForceP, LrDispN, LrForceN, LuForceN, LgK1, LgK2, LgK3, LgK4, LgKLim, LgD1, LgD2, LgD3, LgD4, LgDLim, LgF1, LgF2, LgF3, LgF4, LgFLim, LgE, LdmgType)

op.uniaxialMaterial('Pinching4', matLong2, 0.5*nL*LePf1, LePd1/(Gamma*DispShape[-2]), 0.5*nL*LePf2, LePd2/(Gamma*DispShape[-2]), 0.5*nL*LePf3, LePd3/(Gamma*DispShape[-2]), 0.5*nL*LePf4, LePd4/(Gamma*DispShape[-2]), 
                        0.5*nL*LeNf1, LeNd1/(Gamma*DispShape[-2]), 0.5*nL*LeNf2, LeNd2/(Gamma*DispShape[-2]), 0.5*nL*LeNf3, LeNd3/(Gamma*DispShape[-2]), 0.5*nL*LeNf4, LeNd4/(Gamma*DispShape[-2]), 
                        LrDispP, LrForceP, LuForceP, LrDispN, LrForceN, LuForceN, LgK1, LgK2, LgK3, LgK4, LgKLim, LgD1, LgD2, LgD3, LgD4, LgDLim, LgF1, LgF2, LgF3, LgF4, LgFLim, LgE, LdmgType)
    
for i in range(nT):
    op.uniaxialMaterial('Pinching4', matTran[i], TePf1, TePd1/(Gamma*DispShape[i]), TePf2, TePd2/(Gamma*DispShape[i]), TePf3, TePd3/(Gamma*DispShape[i]), TePf4, TePd4/(Gamma*DispShape[i]), 
                         TeNf1, TeNd1/(Gamma*DispShape[i]), TeNf2, TeNd2/(Gamma*DispShape[i]), TeNf3, TeNd3/(Gamma*DispShape[i]), TeNf4, TeNd4/(Gamma*DispShape[i]), 
                         TrDispP, TrForceP, TuForceP, TrDispN, TrForceN, TuForceN, TgK1, TgK2, TgK3, TgK4, TgKLim, TgD1, TgD2, TgD3, TgD4, TgDLim, TgF1, TgF2, TgF3, TgF4, TgFLim, TgE, TdmgType)

matTot = 1000
op.uniaxialMaterial('Parallel', matTot, matLong1, matLong2, matTran[0], matTran[1],matTran[2],matTran[3],matTran[4],matTran[5],matTran[6],matTran[7],matTran[8],matTran[9])


matRig = 4
op.uniaxialMaterial('Elastic', 	 matRig,	10e12)
    
#matTot = 30
#op.uniaxialMaterial('Parallel', matTot, matLong, matTran)

eleID1 = 1
op.element('zeroLength', eleID1, nodefix, nodefree, '-mat', matTot, matRig, matRig, '-dir', 1, 2, 3)
#eleID2 = 2
#op.element('zeroLength', eleID2, nodefix, nodefree, '-mat', matTran, matRig, matRig, '-dir', 1, 2, 3)

#op.equalDOF(nodefix, nodefree, 2 ,3)


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
    
    
if(Analysis_Type == 'PO'):   
    op.recorder('Node', '-file', direc+'/VbaseC.out', '-node', nodefix, '-dof', 1, 'reaction')
    op.recorder('Node', '-file', direc+'/DispC.out', '-node', nodefree, '-dof', 1, 'disp')
elif(Analysis_Type == 'CPO'):
    op.recorder('Node', '-file', direc+'/VbaseC_CPO.out', '-node', nodefix, '-dof', 1, 'reaction')
    op.recorder('Node', '-file', direc+'/DispC_CPO.out', '-node', nodefree, '-dof', 1, 'disp')
    
    
    
#Run Pushover Analysis
print('Running Pushover...')
if(Analysis_Type == 'PO'):
        displist = [50]
    
elif(Analysis_Type == 'CPO'):
    displist = [1, 0, -1, 0, 2, 0, -2, 0, 5, 0, -5, 0, 8, 0, -8, 0, 10, 0, -10, 0, 15, 0, -15, 0, 20, 0, -20, 0, 25, 0, -25, 0, 30, 0, -30, 0,  35, 0, -35, 0]
          
dstep = 0.05
IDctrlNode = nodefree          # node where disp is read for disp control
IDctrlDOF  = 1                  # degree of freedom read for disp control (1 = x displacement)

testParams = [1.e-4, 1000]

op.numberer('RCM') # renumber dof's to minimize band-width (optimization), if you want to
op.system('FullGeneral') # how to store and solve the system of equations in the analysis
op.constraints('Transformation') # how it handles boundary conditions
op.test('EnergyIncr',*testParams) # determine if convergence has been achieved at the end of an iteration step
op.algorithm('Newton') # use Newton's solution algorithm: updates tangent stiffness at every iteration
op.analysis('Static') # define type of analysis static or transient

POtag = 100;
linTS = 2
op.timeSeries('Linear',linTS)

op.pattern('Plain', POtag, linTS) 


op.load(nodefree, 1, 0, 0)

op.reactions()

ok = 0
for j in range(0, len(displist)):
    if ok != 0:
        break
    dispnew = displist[j]
    if j > 0:
        dispold = displist[j-1]
    else:
        dispold = 0
    disp = dispnew - dispold
    if disp > 0:
        dsteps = dstep
    else:
        dsteps = -dstep
    nstep = int(disp/dsteps)
    op.integrator('DisplacementControl', IDctrlNode, IDctrlDOF, dsteps) # determine the next time step for an analysis
    for i in range(nstep):
        ok = op.analyze(1)
        
        if ok != 0:
            testParams2 = [1.e-3, 5000]
            op.test('EnergyIncr',*testParams2)
            op.algorithm('Newton','-initial')
            print("Trying Newton with Initial Tangent ..")
            ok = op.analyze(1,dsteps/2)
            op.test('RelativeEnergyIncr',*testParams) 
            op.algorithm('Newton') 
        
        if ok != 0:
            op.algorithm('Broyden',50)
            op.test('EnergyIncr',*testParams2)
            print("Trying Broyden ..")
            ok = op.analyze(1,dsteps/2) 
            op.test('RelativeEnergyIncr',*testParams) 
            op.algorithm('Newton') 
            
        if ok != 0:
            op.algorithm('NewtonLineSearch')
            op.test('EnergyIncr',*testParams2)
            print("Trying NewtonWithLineSearch ..")
            ok = op.analyze(1,dsteps/10)
            op.test('RelativeEnergyIncr',*testParams) 
            op.algorithm('Newton') # use Newton's solution algorithm: updates tangent stiffness at every iteration
        
        if ok == 0:
            dsp = round(op.nodeDisp(IDctrlNode,IDctrlDOF),3)
            #print(f'Displacement {dsp} reached of {dispnew}')
            
        else:
            break

if(ok != 0):
    print('Problem with Pushover')
else:
    print('Done')
#print(force)        
#ani = vfo.animate_deformedshape(model="Tank", loadcase="Pushover")
#vfo.plot_model(show_nodes = "yes",show_nodetags="yes")