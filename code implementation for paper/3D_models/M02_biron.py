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

direc = './ResultsM02_biron'

if(os.path.exists(direc)==False):
    os.makedirs(direc)
    
 
im = 11

for gm in range(22):
    for rot in range(2):
     
        op.model('basic', '-ndm', 3, '-ndf', 6) 


        # 1st step: Node definition with Node Command

        #Main line, fixed points trapezes
        op.node(1,	 1000.0,   0.0,	    10.0) 	#fix point	
        op.node(2,	 4000.0,   0.0,	    10.0) 	#fix point	
        op.node(3,	 7000.0,   0.0,		10.0) 	#fix point	
        op.node(4,	 10000.0,  0.0,		10.0) 	#fix point	
        op.node(5,	 13000.0,  0.0,		10.0) 	#fix point	
        op.node(6,	 16000.0,  0.0,		10.0) 	#fix point	
        op.node(7,	 19000.0,  0.0,		10.0) 	#fix point	
        op.node(8,	 22000.0,  0.0,		10.0) 	#fix point	
        op.node(9,	 25000.0,  0.0,		10.0) 	#fix point	
        op.node(10,	 28000.0,  0.0,		10.0) 	#fix point	
        op.node(11,	 31000.0,  0.0,		10.0) 	#fix point	
        op.node(12,	 34000.0,  0.0,		10.0) 	#fix point	


        #Cross lines fixed points trapezes
        op.node(13,	 36000.0,  1000.0,	10.0) 	#fix point
        op.node(14,	 36000.0,  4000.0,	10.0) 	#fix point
        op.node(15,  36000.0,  7000.0,	10.0) 	#fix point
        op.node(16,  36000.0,  10000.0,	10.0) 	#fix point
        op.node(17,  36000.0,  13000.0,	10.0) 	#fix point
        op.node(18,  36000.0,  16000.0,	10.0) 	#fix point

        massML = [0.363, 0.363, 0.363, 0, 0, 0]
        massCL = [0.363, 0.363, 0.363, 0, 0, 0]

        #Pipe Connection, Main Line
        op.node(1001,	0.0,	 	0.0,		0.0) 	#pipe connection	
        op.node(101,	1000.0,		0.0,		0.0, '-mass', *massML) 	#pipe connection	
        op.node(102,	4000.0,		0.0,		0.0, '-mass', *massML) 	#pipe connection	
        op.node(103,	7000.0,		0.0,		0.0, '-mass', *massML) 	#pipe connection	
        op.node(104,	10000.0,	0.0,		0.0, '-mass', *massML) 	#pipe connection	
        op.node(105,	13000.0,	0.0,		0.0, '-mass', *massML) 	#pipe connection	
        op.node(106,	16000.0,	0.0,		0.0, '-mass', *massML) 	#pipe connection	
        op.node(107,	19000.0,	0.0,		0.0, '-mass', *massML) 	#pipe connection	
        op.node(108,	22000.0,	0.0,		0.0, '-mass', *massML) 	#pipe connection	
        op.node(109,	25000.0,	0.0,		0.0, '-mass', *massML) 	#pipe connection	
        op.node(110,	28000.0,	0.0,		0.0, '-mass', *massML) 	#pipe connection	
        op.node(111,	31000.0,	0.0,		0.0, '-mass', *massML) 	#pipe connection
        op.node(112,	34000.0,	0.0,		0.0, '-mass', *massML) 	#pipe connection
        op.node(1002,	36000.0,	0.0,		0.0) 	#pipe connection	

        #Cross line
        op.node(113, 	36000.0,	1000.0,		0.0, '-mass', *massML) 	#pipe connection
        op.node(114, 	36000.0,	4000.0,		0.0, '-mass', *massML) 	#pipe connection
        op.node(115, 	36000.0,	7000.0,		0.0, '-mass', *massML) 	#pipe connection
        op.node(116, 	36000.0,	10000.0,	0.0, '-mass', *massML) 	#pipe connection
        op.node(117, 	36000.0,	13000.0,	0.0, '-mass', *massML) 	#pipe connection
        op.node(118, 	36000.0,	16000.0,	0.0, '-mass', *massML) 	#pipe connection
        op.node(1003, 	36000.0,	18000.0,	0.0) 	#pipe connection

        #### Nodes for nonlinear & linear springs

        #Main Line (1)
        op.node(201,	1000.0,	    0.0,		5.0) 	#spring	
        op.node(202,    4000.0,		0.0,		5.0) 	#spring	
        op.node(203,	7000.0,		0.0,		5.0) 	#spring	
        op.node(204,	10000.0,	0.0,		5.0) 	#spring	
        op.node(205,	13000.0,	0.0,		5.0) 	#spring	
        op.node(206,	16000.0,	0.0,		5.0) 	#spring	
        op.node(207,	19000.0,	0.0,		5.0) 	#spring	
        op.node(208,	22000.0,	0.0,		5.0) 	#spring	
        op.node(209,	25000.0,	0.0,		5.0) 	#spring	
        op.node(210,	28000.0,	0.0,		5.0) 	#spring	
        op.node(211,	31000.0,	0.0,		5.0) 	#spring	
        op.node(212,	34000.0,	0.0,	    5.0) 	#spring	


        #Cross lines 
        #Second cross line (1)
        op.node(213,	 36000.0,	1000.0,		5.0) 	#spring
        op.node(214,	 36000.0,	4000.0,		5.0) 	#spring
        op.node(215,	 36000.0,	7000.0,		5.0) 	#spring
        op.node(216,	 36000.0,	10000.0,	5.0) 	#spring
        op.node(217,	 36000.0,	13000.0,	5.0) 	#spring
        op.node(218,	 36000.0,	16000.0,	5.0) 	#spring


        #Main Line (2)
        op.node(301,	1000.0,	    0.0,		5.0) 	#spring	
        op.node(302,    4000.0,		0.0,		5.0) 	#spring	
        op.node(303,	7000.0,		0.0,		5.0) 	#spring	
        op.node(304,	10000.0,	0.0,		5.0) 	#spring	
        op.node(305,	13000.0,	0.0,		5.0) 	#spring	
        op.node(306,	16000.0,	0.0,		5.0) 	#spring	
        op.node(307,	19000.0,	0.0,		5.0) 	#spring	
        op.node(308,	22000.0,	0.0,		5.0) 	#spring	
        op.node(309,	25000.0,	0.0,		5.0) 	#spring	
        op.node(310,	28000.0,	0.0,		5.0) 	#spring	
        op.node(311,	31000.0,	0.0,		5.0) 	#spring	
        op.node(312,	34000.0,	0.0,	    5.0) 	#spring	


        #Cross lines 
        #Second cross line (2)
        op.node(313,	 36000.0,	1000.0,		5.0) 	#spring
        op.node(314,	 36000.0,	4000.0,		5.0) 	#spring
        op.node(315,	 36000.0,	7000.0,		5.0) 	#spring
        op.node(316,	 36000.0,	10000.0,	5.0) 	#spring
        op.node(317,	 36000.0,	13000.0,	5.0) 	#spring
        op.node(318,	 36000.0,	16000.0,	5.0) 	#spring

        ## Pipe connection nodes
        #Main line (1)
        op.node(801, 	5940.0,		0.0,		0.0) 	#Pipe connection
        op.node(802, 	6060.0,		0.0,		0.0) 	#Pipe connection
        op.node(803, 	11940.0,	0.0,		0.0) 	#Pipe connection
        op.node(804, 	12060.0,	0.0,		0.0) 	#Pipe connection
        op.node(805, 	17940.0,	0.0,		0.0) 	#Pipe connection
        op.node(806, 	18060.0,	0.0,		0.0) 	#Pipe connection
        op.node(807, 	23940.0,	0.0,		0.0) 	#Pipe connection
        op.node(808, 	24060.0,	0.0,		0.0) 	#Pipe connection
        op.node(809, 	29940.0,	0.0,		0.0) 	#Pipe connection
        op.node(810, 	30060.0,	0.0,		0.0) 	#Pipe connection
        op.node(811, 	35900.0,	0.0,		0.0) 	#Pipe connection

        #Cross line (1)
        op.node(812, 	36000.0,	100.0,	    0.0) 	#Pipe connection
        op.node(813, 	36000.0,	5940.0,	    0.0) 	#Pipe connection
        op.node(814, 	36000.0,	6060.0,	    0.0) 	#Pipe connection
        op.node(815, 	36000.0,	11940.0,	0.0) 	#Pipe connection
        op.node(816, 	36000.0,	12060.0,	0.0) 	#Pipe connection

        #Main line (2)
        op.node(901, 	5940.0,		0.0,		0.0) 	#Pipe connection
        op.node(902, 	6060.0,		0.0,		0.0) 	#Pipe connection
        op.node(903, 	11940.0,	0.0,		0.0) 	#Pipe connection
        op.node(904, 	12060.0,	0.0,		0.0) 	#Pipe connection
        op.node(905, 	17940.0,	0.0,		0.0) 	#Pipe connection
        op.node(906, 	18060.0,	0.0,		0.0) 	#Pipe connection
        op.node(907, 	23940.0,	0.0,		0.0) 	#Pipe connection
        op.node(908, 	24060.0,	0.0,		0.0) 	#Pipe connection
        op.node(909, 	29940.0,	0.0,		0.0) 	#Pipe connection
        op.node(910, 	30060.0,	0.0,		0.0) 	#Pipe connection
        op.node(911, 	35900.0,	0.0,		0.0) 	#Pipe connection

        #Cross line (2)
        op.node(912, 	36000.0,	100.0,	    0.0) 	#Pipe connection
        op.node(913, 	36000.0,	5940.0,	    0.0) 	#Pipe connection
        op.node(914, 	36000.0,	6060.0,	    0.0) 	#Pipe connection
        op.node(915, 	36000.0,	11940.0,	0.0) 	#Pipe connection
        op.node(916, 	36000.0,	12060.0,	0.0) 	#Pipe connection

        # 2nd step: Boundary Condition

        op.fix(1,	1,	1,	1,	1,	1,	1) 
        op.fix(2,	1,	1,	1,	1,	1,	1) 
        op.fix(3,	1,	1,	1,	1,	1,	1)
        op.fix(4,	1,	1,	1,	1,	1,	1)
        op.fix(5,	1,	1,	1,	1,	1,	1)
        op.fix(6,	1,	1,	1,	1,	1,	1)
        op.fix(7,	1,	1,	1,	1,	1,	1)
        op.fix(8,	1,	1,	1,	1,	1,	1)
        op.fix(9,	1,	1,	1,	1,	1,	1)
        op.fix(10,	1,	1,	1,	1,	1,	1)
        op.fix(11,	1,	1,	1,	1,	1,	1)
        op.fix(12,	1,	1,	1,	1,	1,	1)
        op.fix(13,	1,	1,	1,	1,	1,	1)
        op.fix(14,	1,	1,	1,	1,	1,	1)
        op.fix(15,	1,	1,	1,	1,	1,	1)
        op.fix(16,	1,	1,	1,	1,	1,	1)
        op.fix(17,	1,	1,	1,	1,	1,	1)
        op.fix(18,	1,	1,	1,	1,	1,	1)

        # 3rd step: Geometric transformation

        vecxz = [0,0,1]
        op.geomTransf('Linear', 1, *vecxz)


        # 4th step: Definition MaterialTnd Histeretic Behavior: 1.C-TPS-L hysteretic bracing dir) 2.C-TPS-L Elastic perp dir) 3.C-TPL-T hysteretic bracing dir) 4.C-TPS-T Elastic perp dir

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



        ##Parameters for threaded pipe joints
        sp1 = 7300000
        sp2 = 17600000
        sp3 = 21000000
        ep1 = 0.00065
        ep2 = 0.0045
        ep3 = 0.01
        sn1 = -7300000
        sn2 = -17600000
        sn3 = -21000000
        en1 = -0.00065
        en2 = -0.0045
        en3 = -0.01
        pinchx = 0.8
        pinchy = 0.05
        damage1 = 0
        damage2 = 0
        beta = 0.1

        mincap = -125
        maxcap = 125


        op.uniaxialMaterial('Pinching4', 10, LePf1, LePd1, LePf2, LePd2, LePf3, LePd3, LePf4, LePd4, LeNf1, LeNd1, LeNf2, LeNd2, LeNf3, LeNd3, LeNf4, LeNd4, LrDispP, LrForceP, LuForceP, LrDispN, LrForceN, LuForceN, LgK1, LgK2, LgK3, LgK4, LgKLim, LgD1, LgD2, LgD3, LgD4, LgDLim, LgF1, LgF2, LgF3, LgF4, LgFLim, LgE, LdmgType)
        op.uniaxialMaterial('Pinching4', 20, TePf1, TePd1, TePf2, TePd2, TePf3, TePd3, TePf4, TePd4, TeNf1, TeNd1, TeNf2, TeNd2, TeNf3, TeNd3, TeNf4, TeNd4, TrDispP, TrForceP, TuForceP, TrDispN, TrForceN, TuForceN, TgK1, TgK2, TgK3, TgK4, TgKLim, TgD1, TgD2, TgD3, TgD4, TgDLim, TgF1, TgF2, TgF3, TgF4, TgFLim, TgE, TdmgType)
        op.uniaxialMaterial('MinMax', 1, 10,  '-min', -35, '-max',35)
        op.uniaxialMaterial('MinMax', 2, 20,  '-min', -60, '-max',60)
        op.uniaxialMaterial('Elastic', 	 3,	0.01)
        op.uniaxialMaterial('Elastic', 	 4,	10e12)
        op.uniaxialMaterial('ElasticBilin', 33, 141.5, 0.01, 12.8)
        op.uniaxialMaterial('MinMax', 88, 33,  '-min', mincap, '-max', maxcap)
        op.uniaxialMaterial('Hysteretic', 7, sp1, ep1, sp2, ep2, sp3, ep3, sn1, en1, sn2, en2, sn3, en3, pinchx, pinchy, damage1, damage2, beta)
        op.uniaxialMaterial('Parallel', 8, 7, 7, 7)


        # 5th step: Element definition

        # Steel
        A = 7761.3 		#area of the pipe section
        E = 210000.0 	#Young modulus of the pipe material
        G = 81000.0		#Shear modulus of the pipe material
        J = 35712656.3 	#torsional moment of the inertia of cross section of pipe
        Iy = 17856328.2 		#second moment of area of the pipe about local y-axix
        Iz = 17856328.2 		#second moment of area of the pipe about local z-axix
        #massu = 0.000121		#mass per unit length of steel pipes (N*s2/mm2)
        massu = 0

        #Main line
        op.element('elasticBeamColumn', 1,	 1001,	101,	A,	E,	G,	J,	Iy,	Iz,	1) #pipe element
        op.element('elasticBeamColumn', 2,	 101,	102,	A,	E,	G,	J,	Iy,	Iz,	1) #pipe element
        op.element('elasticBeamColumn', 3,	 102,	801,	A,	E,	G,	J,	Iy,	Iz,	1) #pipe element
        op.element('elasticBeamColumn', 4,	 901,	802,	A,	E,	G,	J,	Iy,	Iz,	1) #pipe element
        op.element('elasticBeamColumn', 5,	 902,	103,	A,	E,	G,	J,	Iy,	Iz,	1) #pipe element
        op.element('elasticBeamColumn', 6,	 103,	104,	A,	E,	G,	J,	Iy,	Iz,	1) #pipe element
        op.element('elasticBeamColumn', 7,	 104,	803,	A,	E,	G,	J,	Iy,	Iz,	1) #pipe element
        op.element('elasticBeamColumn', 8,	 903,	804,	A,	E,	G,	J,	Iy,	Iz,	1) #pipe element
        op.element('elasticBeamColumn', 9,	 904,	105,	A,	E,	G,	J,	Iy,	Iz,	1) #pipe element
        op.element('elasticBeamColumn', 10,	 105,	106,	A,	E,	G,	J,	Iy,	Iz,	1) #pipe element
        op.element('elasticBeamColumn', 11,	 106,	805,	A,	E,	G,	J,	Iy,	Iz,	1) #pipe element
        op.element('elasticBeamColumn', 12,	 905,	806,	A,	E,	G,	J,	Iy,	Iz,	1) #pipe element
        op.element('elasticBeamColumn', 13,	 906,	107,	A,	E,	G,	J,	Iy,	Iz,	1) #pipe element
        op.element('elasticBeamColumn', 14,	 107,	108,	A,	E,	G,	J,	Iy,	Iz,	1) #pipe element
        op.element('elasticBeamColumn', 15,	 108,	807,	A,	E,	G,	J,	Iy,	Iz,	1) #pipe element
        op.element('elasticBeamColumn', 16,	 907,	808,	A,	E,	G,	J,	Iy,	Iz,	1) #pipe element
        op.element('elasticBeamColumn', 17,	 908,	109,	A,	E,	G,	J,	Iy,	Iz,	1) #pipe element
        op.element('elasticBeamColumn', 18,	 109,	110,	A,	E,	G,	J,	Iy,	Iz,	1) #pipe element
        op.element('elasticBeamColumn', 19,	 110,	809,	A,	E,	G,	J,	Iy,	Iz,	1) #pipe element
        op.element('elasticBeamColumn', 20,	 909,	810,	A,	E,	G,	J,	Iy,	Iz,	1) #pipe element
        op.element('elasticBeamColumn', 21,	 910,	111,	A,	E,	G,	J,	Iy,	Iz,	1) #pipe element
        op.element('elasticBeamColumn', 22,	 111,	112, 	A,	E,	G,	J,	Iy,	Iz,	1) #pipe element
        op.element('elasticBeamColumn', 23,	 112,	811, 	A,	E,	G,	J,	Iy,	Iz,	1) #pipe element
        op.element('elasticBeamColumn', 24,	 911,	1002, 	A,	E,	G,	J,	Iy,	Iz,	1) #pipe element

        #Second cross line
        op.element('elasticBeamColumn', 25,	 1002,	812, 	A,	E,	G,	J,	Iy,	Iz,	1) #pipe element
        op.element('elasticBeamColumn', 26,	 912, 	113, 	A,	E,	G,	J,	Iy,	Iz,	1) #pipe element
        op.element('elasticBeamColumn', 27,	 113,	114, 	A,	E,	G,	J,	Iy,	Iz,	1) #pipe element
        op.element('elasticBeamColumn', 28,	 114,	813,	A,	E,	G,	J,	Iy,	Iz,	1) #pipe element
        op.element('elasticBeamColumn', 29,	 913,	814,	A,	E,	G,	J,	Iy,	Iz,	1) #pipe element
        op.element('elasticBeamColumn', 30,	 914,	115,	A,	E,	G,	J,	Iy,	Iz,	1) #pipe element
        op.element('elasticBeamColumn', 31,	 115,	116, 	A,	E,	G,	J,	Iy,	Iz,	1) #pipe element
        op.element('elasticBeamColumn', 32,	 116,	815,	A,	E,	G,	J,	Iy,	Iz,	1) #pipe element
        op.element('elasticBeamColumn', 33,	 915,	816,	A,	E,	G,	J,	Iy,	Iz,	1) #pipe element
        op.element('elasticBeamColumn', 34,	 916,	117,	A,	E,	G,	J,	Iy,	Iz,	1) #pipe element
        op.element('elasticBeamColumn', 35,	 117,	118,	A,	E,	G,	J,	Iy,	Iz,	1) #pipe element
        op.element('elasticBeamColumn', 36,	 118,	1003,	A,	E,	G,	J,	Iy,	Iz,	1) #pipe element

        op.rigidLink('beam',	1,	201)	#rigid link
        op.rigidLink('beam',	2,	202)	#rigid link
        op.rigidLink('beam',	3,	203)	#rigid link
        op.rigidLink('beam',	4,	204)	#rigid link
        op.rigidLink('beam',	5,	205)	#rigid link
        op.rigidLink('beam',	6,	206)	#rigid link
        op.rigidLink('beam',	7,	207)	#rigid link
        op.rigidLink('beam',	8,	208)	#rigid link
        op.rigidLink('beam',	9,	209)	#rigid link
        op.rigidLink('beam',	10,	210)	#rigid link
        op.rigidLink('beam',	11,	211)	#rigid link
        op.rigidLink('beam',	12,	212)	#rigid link
        op.rigidLink('beam',	13,	213)	#rigid link
        op.rigidLink('beam',	14,	214)	#rigid link
        op.rigidLink('beam',	15,	215)	#rigid link
        op.rigidLink('beam',	16,	216)	#rigid link
        op.rigidLink('beam',	17,	217)	#rigid link
        op.rigidLink('beam',	18,	218)	#rigid link

        op.rigidLink('beam',	301, 101)	#rigid link
        op.rigidLink('beam',	302, 102)	#rigid link
        op.rigidLink('beam',	303, 103)	#rigid link
        op.rigidLink('beam',	304, 104)	#rigid link
        op.rigidLink('beam',	305, 105)	#rigid link
        op.rigidLink('beam',	306, 106)	#rigid link
        op.rigidLink('beam',	307, 107)	#rigid link
        op.rigidLink('beam',	308, 108)	#rigid link
        op.rigidLink('beam',	309, 109)	#rigid link
        op.rigidLink('beam',	310, 110)	#rigid link
        op.rigidLink('beam',	311, 111)	#rigid link
        op.rigidLink('beam',	312, 112)	#rigid link
        op.rigidLink('beam',	313, 113)	#rigid link
        op.rigidLink('beam',	314, 114)	#rigid link
        op.rigidLink('beam',	315, 115)	#rigid link
        op.rigidLink('beam',	316, 116)	#rigid link
        op.rigidLink('beam',	317, 117)	#rigid link
        op.rigidLink('beam',	318, 118)	#rigid link

        #5.2: Braces behaviour

        #Main line
        op.element('zeroLength', 	501,		201,		301,  '-mat',	1,	2,	4, 4, 4, 4, '-dir', 	1,  2,  3,  4,  5,  6) #Typology of subassembly
        op.element('zeroLength', 	502,		202,		302,  '-mat',	3,	3,	4, 4, 4, 4, '-dir', 	1,  2,  3,  4,  5,  6) #Typology of subassembly 
        op.element('zeroLength', 	503,		203,		303,  '-mat',	3,	3,	4, 4, 4, 4, '-dir', 	1,  2,  3,  4,  5,  6) #Typology of subassembly
        op.element('zeroLength', 	504,		204,		304,  '-mat',	3,	3,	4, 4, 4, 4, '-dir', 	1,  2,  3,  4,  5,  6) #Typology of subassembly
        op.element('zeroLength', 	505,		205,		305,  '-mat',	3,	2,	4, 4, 4, 4, '-dir', 	1,  2,  3,  4,  5,  6) #Typology of subassembly 
        op.element('zeroLength', 	506,		206,		306,  '-mat',	1,	3,	4, 4, 4, 4, '-dir', 	1,  2,  3,  4,  5,  6) #Typology of subassembly
        op.element('zeroLength', 	507,		207,		307,  '-mat',	3,  3,	4, 4, 4, 4, '-dir', 	1,  2,  3,  4,  5,  6) #Typology of subassembly
        op.element('zeroLength', 	508,		208,		308,  '-mat',	3,  2,	4, 4, 4, 4, '-dir', 	1,  2,  3,  4,  5,  6) #Typology of subassembly
        op.element('zeroLength', 	509,		209,		309,  '-mat',	3,  3,	4, 4, 4, 4, '-dir', 	1,  2,  3,  4,  5,  6) #Typology of subassembly
        op.element('zeroLength', 	510,		210,		310,  '-mat',	3,  3,	4, 4, 4, 4, '-dir', 	1,  2,  3,  4,  5,  6) #Typology of subassembly
        op.element('zeroLength', 	511,		211,		311,  '-mat',	1,  3,	4, 4, 4, 4, '-dir', 	1,  2,  3,  4,  5,  6) #Typology of subassembly
        op.element('zeroLength', 	512,		212,		312,  '-mat',	3,	2,	4, 4, 4, 4, '-dir', 	1,  2,  3,  4,  5,  6) #Typology of subassembly

        op.element('zeroLength', 	513,		213,		313,  '-mat',	3,	3,	4, 4, 4, 4, '-dir', 	1,  2,  3,  4,  5,  6) #Typology of subassembly
        op.element('zeroLength', 	514,		214,		314,  '-mat',	2,  1,	4, 4, 4, 4, '-dir', 	1,  2,  3,  4,  5,  6) #Typology of subassembly
        op.element('zeroLength', 	515,		215,		315,  '-mat',	3,  3,	4, 4, 4, 4, '-dir', 	1,  2,  3,  4,  5,  6) #Typology of subassembly
        op.element('zeroLength', 	516,		216,		316,  '-mat',	3,  3,	4, 4, 4, 4, '-dir', 	1,  2,  3,  4,  5,  6) #Typology of subassembly
        op.element('zeroLength', 	517,		217,		317,  '-mat',	2,  1,	4, 4, 4, 4, '-dir', 	1,  2,  3,  4,  5,  6) #Typology of subassembly
        op.element('zeroLength', 	518,		218,		318,  '-mat',	3,	3,	4, 4, 4, 4, '-dir', 	1,  2,  3,  4,  5,  6) #Typology of subassembly

        nodesX = [1001, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 1002, 113, 114, 115, 116, 117, 118, 1003]
        nodesY = [1001, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 1002, 113, 114, 115, 116, 117, 118, 1003]
        
        nodesXt = [101,106,111,114,117]
        nodesXp = []

        for i in range(len(nodesX)):
            if nodesX[i] not in nodesXt:
                nodesXp.append(nodesX[i])
                
        nodesYt = [101,105,108,112,114,117]
        nodesYp = []

        for i in range(len(nodesY)):
            if nodesY[i] not in nodesYt:
                nodesYp.append(nodesY[i])
        

        ## Springs for pipe joints

        op.element('zeroLength',	701,		801,		901,   '-mat', 4, 4, 4, 4, 4, 8, '-dir', 1, 2, 3, 4, 5, 6) #Typology of subassembly
        op.element('zeroLength',	702,		802,		902,   '-mat', 4, 4, 4, 4, 4, 8, '-dir', 1, 2, 3, 4, 5, 6) #Typology of subassembly
        op.element('zeroLength',	703,		803,		903,   '-mat', 4, 4, 4, 4, 4, 8, '-dir', 1, 2, 3, 4, 5, 6) #Typology of subassembly
        op.element('zeroLength',	704,		804,		904,   '-mat', 4, 4, 4, 4, 4, 8, '-dir', 1, 2, 3, 4, 5, 6) #Typology of subassembly
        op.element('zeroLength',	705,		805,		905,   '-mat', 4, 4, 4, 4, 4, 8, '-dir', 1, 2, 3, 4, 5, 6) #Typology of subassembly 
        op.element('zeroLength',	706,		806,		906,   '-mat', 4, 4, 4, 4, 4, 8, '-dir', 1, 2, 3, 4, 5, 6) #Typology of subassembly
        op.element('zeroLength',	707,		807,		907,   '-mat', 4, 4, 4, 4, 4, 8, '-dir', 1, 2, 3, 4, 5, 6) #Typology of subassembly
        op.element('zeroLength',	708,		808,		908,   '-mat', 4, 4, 4, 4, 4, 8, '-dir', 1, 2, 3, 4, 5, 6) #Typology of subassembly
        op.element('zeroLength',	709,		809,		909,   '-mat', 4, 4, 4, 4, 4, 8, '-dir', 1, 2, 3, 4, 5, 6) #Typology of subassembly
        op.element('zeroLength',	710,		810,		910,   '-mat', 4, 4, 4, 4, 4, 8, '-dir', 1, 2, 3, 4, 5, 6) #Typology of subassembly
        op.element('zeroLength',	711,		811,		911,   '-mat', 4, 4, 4, 4, 4, 8, '-dir', 1, 2, 3, 4, 5, 6) #Typology of subassembly

        op.element('zeroLength',	712,		812,		912,   '-mat', 4, 4, 4, 4, 4, 8, '-dir', 1, 2, 3, 4, 5, 6) #Typology of subassembly
        op.element('zeroLength',	713,		813,		913,   '-mat', 4, 4, 4, 4, 4, 8, '-dir', 1, 2, 3, 4, 5, 6) #Typology of subassembly
        op.element('zeroLength',	714,		814,		914,   '-mat', 4, 4, 4, 4, 4, 8, '-dir', 1, 2, 3, 4, 5, 6) #Typology of subassembly
        op.element('zeroLength',	715,		815,		915,   '-mat', 4, 4, 4, 4, 4, 8, '-dir', 1, 2, 3, 4, 5, 6) #Typology of subassembly
        op.element('zeroLength',	716,		816,		916,   '-mat', 4, 4, 4, 4, 4, 8, '-dir', 1, 2, 3, 4, 5, 6) #Typology of subassembly

        # 6th step: Definition restrain displamente and rotation

        '''
        op.equalDOF(201, 301,  3, 4, 5, 6)
        op.equalDOF(202, 302,  3, 4, 5, 6)
        op.equalDOF(203, 303,  3, 4, 5,	6)
        op.equalDOF(204, 304,  3, 4, 5, 6)
        op.equalDOF(205, 305,  3, 4, 5, 6)
        op.equalDOF(206, 306,  3, 4, 5, 6)
        op.equalDOF(207, 307,  3, 4, 5, 6)
        op.equalDOF(208, 308,  3, 4, 5, 6)
        op.equalDOF(209, 309,  3, 4, 5, 6)
        op.equalDOF(210, 310,  3, 4, 5, 6)
        op.equalDOF(211, 311,  3, 4, 5, 6)

        op.equalDOF(212, 312,  3, 4, 5, 6)
        op.equalDOF(213, 313,  3, 4, 5, 6)
        op.equalDOF(214, 314,  3, 4, 5, 6)
        op.equalDOF(215, 315,  3, 4, 5, 6)
        op.equalDOF(216, 316,  3, 4, 5, 6)
        op.equalDOF(217, 317,  3, 4, 5, 6)
        op.equalDOF(218, 318,  3, 4, 5, 6)
        '''
        ## For piping joints

        op.equalDOF(801, 901, 1, 2, 3, 4, 5)
        op.equalDOF(802, 902, 1, 2, 3, 4, 5)
        op.equalDOF(803, 903, 1, 2, 3, 4, 5)
        op.equalDOF(804, 904, 1, 2, 3, 4, 5)
        op.equalDOF(805, 905, 1, 2, 3, 4, 5)
        op.equalDOF(806, 906, 1, 2, 3, 4, 5)
        op.equalDOF(807, 907, 1, 2, 3, 4, 5)
        op.equalDOF(808, 908, 1, 2, 3, 4, 5)
        op.equalDOF(809, 909, 1, 2, 3, 4, 5)
        op.equalDOF(810, 910, 1, 2, 3, 4, 5)
        op.equalDOF(811, 911, 1, 2, 3, 4, 5)

        op.equalDOF(812, 912, 1, 2, 3, 4, 5)
        op.equalDOF(813, 913, 1, 2, 3, 4, 5)
        op.equalDOF(814, 914, 1, 2, 3, 4, 5)
        op.equalDOF(815, 915, 1, 2, 3, 4, 5)
        op.equalDOF(816, 916, 1, 2, 3, 4, 5)


        # 9th step: Apply of load and gravity with static analysis

        # set l -0.2315; #load per unit length of cpvc piping (N/mm)
        l = -1.183; #load per unit length of steel piping (N/mm)

        op.timeSeries('Constant', 1)
        op.pattern('Plain', 1, 1)

        op.eleLoad('-ele', 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, '-type', '-beamUniform',0.0, l, 0.0)

        # Analysis command for static analysis

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
            
        # 10th Step: Eigenvalue Analysis

        omega = []
        freq =  []
        T = []

        lamb = op.eigen(4)


        for lam in lamb:
            omega.append((lam)**0.5)
            freq.append((lam)**0.5/(2*np.pi))
            T.append((2*np.pi)/(lam)**0.5)

        for t in range(len(T)):
            print('T'+str(t+1)+' = '+str(T[t])+' s')
            
            
        #11th step: Define Rayleigh Damping
        xDamp = 0.02					# damping ratio
        MpropSwitch = 1.0
        KcurrSwitch = 0.0
        KcommSwitch = 1.0
        KinitSwitch = 0.0
        nEigenI = 1		# mode 1
        nEigenJ = 2		# mode 2
        lambdaN = op.eigen(nEigenJ)			# eigenvalue analysis for nEigenJ modes
        lambdaI = lambdaN[nEigenI-1] 		# eigenvalue mode i
        lambdaJ = lambdaN[nEigenJ-1] 	# eigenvalue mode j
        omegaI = lambdaI**0.5
        omegaJ = lambdaJ**0.5
        alphaM = MpropSwitch*xDamp*(2*omegaI*omegaJ)/(omegaI+omegaJ) # M-prop. damping; D = alphaM*M
        betaKcurr = KcurrSwitch*2*xDamp/(omegaI+omegaJ)        	# current-K;      +beatKcurr*KCurrent
        betaKcomm = KcommSwitch*2*xDamp/(omegaI+omegaJ)   		# last-committed K;   +betaKcomm*KlastCommitt
        betaKinit = KinitSwitch*2*xDamp/(omegaI+omegaJ)         # initial-K;     +beatKinit*Kini

        op.rayleigh(alphaM, betaKcurr, betaKinit, betaKcomm)   

        #12th step: Run Dynamic Nonlinear time history analysis 


        print('Running NLTH Analysis, GM '+str(gm+1)+'...')

        Name1 = np.loadtxt('C:/Users/rmeri/Documents/UCL/SuspendedNSEs/Ground_Motion_Set/Names.txt')[2*gm]
        Name2 = np.loadtxt('C:/Users/rmeri/Documents/UCL/SuspendedNSEs/Ground_Motion_Set/Names.txt')[2*gm+1]
        
        dts = np.loadtxt('C:/Users/rmeri/Documents/UCL/SuspendedNSEs/Ground_Motion_Set/Timesteps.txt')[2*gm]/10


        GMfact = 1 


        acc1 = 1000*np.loadtxt('C:/Users/rmeri/Documents/UCL/SuspendedNSEs/BuildingsOS/NLTH/ResultsS4/FloorAcc_IM'+str(im+1)+'_'+str(int(Name1))+'.txt')[:,4]
        acc2 = 1000*np.loadtxt('C:/Users/rmeri/Documents/UCL/SuspendedNSEs/BuildingsOS/NLTH/ResultsS4/FloorAcc_IM'+str(im+1)+'_'+str(int(Name2))+'.txt')[:,4]


        Npts1 = len(acc1)
        Npts2 = len(acc2)

        if(Npts1<=Npts2):
            Npts = Npts1
        else:
            Npts = Npts2


        dta = dts
        TmaxAnalysis = dts*Npts

        GMfatt =  GMfact

        IDLoadTag1 = 100
        IDLoadTag2 = 200
        
        IDTimeSeries1 = 1000
        IDTimeSeries2 = 2000


        #Define time series
        op.timeSeries('Path',IDTimeSeries1,'-dt',dts,'-values',*acc1,'-factor',GMfatt, '-prependZero')
        op.timeSeries('Path',IDTimeSeries2,'-dt',dts,'-values',*acc2,'-factor',GMfatt, '-prependZero')


        #Define load pattern
        if(rot == 0):
            op.pattern('UniformExcitation',IDLoadTag1,1,'-accel',IDTimeSeries1)
            op.pattern('UniformExcitation',IDLoadTag2,2,'-accel',IDTimeSeries2)

            op.recorder('Node', '-file', direc+'/PipeDispX_IM'+str(im+1)+'_'+str(int(Name1))+'.out', '-time', '-dt', 0.001, '-node', *nodesX, '-dof', 1, 'disp')
            op.recorder('Node', '-file', direc+'/PipeDispY_IM'+str(im+1)+'_'+str(int(Name2))+'.out', '-time', '-dt', 0.001, '-node', *nodesY, '-dof', 2, 'disp')
            
            op.recorder('Node', '-file', direc+'/PipeDispXt_IM'+str(im+1)+'_'+str(int(Name1))+'.out', '-time', '-dt', 0.001, '-node', *nodesXt, '-dof', 1, 'disp')
            op.recorder('Node', '-file', direc+'/PipeDispYt_IM'+str(im+1)+'_'+str(int(Name2))+'.out', '-time', '-dt', 0.001, '-node', *nodesYt, '-dof', 2, 'disp')
            
            op.recorder('Node', '-file', direc+'/PipeDispXp_IM'+str(im+1)+'_'+str(int(Name1))+'.out', '-time', '-dt', 0.001, '-node', *nodesXp, '-dof', 1, 'disp')
            op.recorder('Node', '-file', direc+'/PipeDispYp_IM'+str(im+1)+'_'+str(int(Name2))+'.out', '-time', '-dt', 0.001, '-node', *nodesYp, '-dof', 2, 'disp')
            
        elif(rot == 1):
            op.pattern('UniformExcitation',IDLoadTag1,2,'-accel',IDTimeSeries1)
            op.pattern('UniformExcitation',IDLoadTag2,1,'-accel',IDTimeSeries2)

            op.recorder('Node', '-file', direc+'/PipeDispX_IM'+str(im+1)+'_'+str(int(Name2))+'.out', '-time', '-dt', 0.001, '-node', *nodesX, '-dof', 1, 'disp')
            op.recorder('Node', '-file', direc+'/PipeDispY_IM'+str(im+1)+'_'+str(int(Name1))+'.out', '-time', '-dt', 0.001, '-node', *nodesY, '-dof', 2, 'disp')
            
            op.recorder('Node', '-file', direc+'/PipeDispXt_IM'+str(im+1)+'_'+str(int(Name2))+'.out', '-time', '-dt', 0.001, '-node', *nodesXt, '-dof', 1, 'disp')
            op.recorder('Node', '-file', direc+'/PipeDispYt_IM'+str(im+1)+'_'+str(int(Name1))+'.out', '-time', '-dt', 0.001, '-node', *nodesYt, '-dof', 2, 'disp')
            
            op.recorder('Node', '-file', direc+'/PipeDispXp_IM'+str(im+1)+'_'+str(int(Name2))+'.out', '-time', '-dt', 0.001, '-node', *nodesXp, '-dof', 1, 'disp')
            op.recorder('Node', '-file', direc+'/PipeDispYp_IM'+str(im+1)+'_'+str(int(Name1))+'.out', '-time', '-dt', 0.001, '-node', *nodesYp, '-dof', 2, 'disp')


        testParams = [1.e-4, 500]                        # convergence tolerance for test
        op.wipeAnalysis()
        op.integrator('Newmark', 0.5, 0.25) # determine the next time step for an analysis
        op.numberer('RCM')                  # renumber dof's to minimize band-width (optimization), if you want to
        op.system('FullGeneral')          # how to store and solve the system of equations in the analysis
        op.constraints('Transformation')             # how it handles boundary conditions
        op.test('RelativeEnergyIncr',*testParams)      # determine if convergence has been achieved at the end of an iteration step
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
                    testParams2 = [1.e-3, 3000]
                    op.test('RelativeEnergyIncr',*testParams2)
                    op.algorithm('Newton','-initial')
                    print("Trying Newton with Initial Tangent ..")
                    ok = op.analyze(1,dta/2)
                    op.test('RelativeEnergyIncr',*testParams) 
                    op.algorithm('Newton') 
                if(ok != 0):
                    op.algorithm('Broyden',50)
                    op.test('RelativeEnergyIncr',*testParams2)
                    print("Trying Broyden ..")
                    ok = op.analyze(1,dta/2) 
                    op.test('RelativeEnergyIncr',*testParams) 
                    op.algorithm('Newton') 
                if(ok != 0):
                    op.algorithm('NewtonLineSearch')
                    op.test('RelativeEnergyIncr',*testParams2)
                    print("Trying NewtonWithLineSearch ..")
                    ok = op.analyze(1,dta/10)
                    op.test('RelativeEnergyIncr',*testParams) 
                    op.algorithm('Newton') # use Newton's solution algorithm: updates tangent stiffness at every iteration
                if(ok != 0):
                    print("Trying KrylovNewton ..")
                    op.algorithm('KrylovNewton') 
                    op.test('RelativeEnergyIncr',*testParams2)
                    ok = op.analyze(1,dta/20)
                    op.test('RelativeEnergyIncr',*testParams) 
                    op.algorithm('Newton')  

        if(op.getTime()<TmaxAnalysis):
            print('Problem with analysis at: '+str(op.getTime()))
        else:
            print("Ground Motion Done. End Time:"+str(op.getTime()))
        op.wipe()
