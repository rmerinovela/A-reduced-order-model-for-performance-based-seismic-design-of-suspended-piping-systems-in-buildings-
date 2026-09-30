#Piping system layout with branches
# N, mm, s
import openseespy.opensees as op
import os
import numpy as np
import matplotlib.pyplot as plt
import time
import scipy as scp



op.wipe()


print('Model generation started...')

direc = './ResultsM31_biron'

if(os.path.isdir(direc)==False):
    os.makedirs(direc)
    
 
im = 9
    
for gm in range(22):
    for rot in range(2):
        
        op.model('basic', '-ndm', 3, '-ndf', 6) 

        # 1st step: Node definition with Node Command

        #Main line, fixed points trapezes
        op.node(1,  0.0,     0.0, 10.0) 
        op.node(2,  2000.0,  0.0, 10.0) 
        op.node(3,  5000.0,  0.0, 10.0) 
        op.node(4,  8000.0,  0.0, 10.0) 
        op.node(5,  11000.0, 0.0, 10.0) 
        op.node(6,  14000.0, 0.0, 10.0) 
        op.node(7,  17000.0, 0.0, 10.0) 
        op.node(8,  20000.0, 0.0, 10.0) 
        op.node(9,  23125.0, 0.0, 10.0) 
        op.node(10, 26000.0, 0.0, 10.0) 
        op.node(11,	29000.0, 0.0, 10.0)


        #Branches, fixed points trapezes
        #Branch 1
        op.node(12, 1050.0,	1500.0,	10.0)
        op.node(13,	1050.0,	4500.0,	10.0)

        #Branch 2
        op.node(14,	4250.0,	1500.0,	10.0)
        op.node(15,	4250.0,	4500.0,	10.0)

        #Branch 3
        op.node(16,	7050.0,	1500.0,	10.0)
        op.node(17,	7050.0,	4500.0,	10.0)

        #Branch 4
        op.node(18,	11550.0, 1500.0, 10.0)
        op.node(19, 11550.0, 4500.0, 10.0)

        #Branch 5
        op.node(20, 14250.0, 1500.0, 10.0)
        op.node(21, 14250.0, 4500.0, 10.0)

        #Branch 6
        op.node(22,	18350.0, 1500.0, 10.0)
        op.node(23,	18350.0, 4500.0, 10.0)

        #Branch 7
        op.node(24, 20950.0, 1500.0, 10.0)
        op.node(25,	20950.0, 4500.0, 10.0)

        #Branch 8
        op.node(26, 25550.0, 1500.0, 10.0)
        op.node(27,	25550.0, 4500.0, 10.0)

        #Branch 9
        op.node(28, 30450.0, 1500.0, 10.0)
        op.node(29, 30450.0, 4500.0, 10.0)

        #Branch 10
        op.node(30, 2350.0, -4500.0, 10.0)
        op.node(31, 2350.0, -1500.0, 10.0)

        #Branch 11
        op.node(32,	7050.0,	-4500.0, 10.0)
        op.node(33,	7050.0,	-1500.0, 10.0)

        #Branch 12
        op.node(34, 11550.0, -4500.0, 10.0)
        op.node(35,	11550.0, -1500.0, 10.0)

        #Branch 13
        op.node(36,	19150.0, -4500.0, 10.0)
        op.node(37,	19150.0, -1500.0, 10.0)

        #Branch 14
        op.node(38, 22950.0, -4500.0, 10.0)
        op.node(39, 22950.0, -1500.0, 10.0)

        #Branch 15
        op.node(40,	30950.0, -4500.0, 10.0)
        op.node(41,	30950.0, -1500.0, 10.0)

        massML = [0.352, 0.352, 0, 0, 0, 0]

        #Pipe Connection, Main Line
        op.node(1001, -1050.0,  0.0, 0.0) 	
        op.node(101,   0.0,     0.0, 0.0, '-mass', *massML) 	
        op.node(1002,  1050.0,  0.0, 0.0) 	
        op.node(102,   2000.0,  0.0, 0.0, '-mass', *massML) 	
        op.node(1003,  2350.0,  0.0, 0.0) 	
        op.node(1004,  4250.0,  0.0, 0.0) 	
        op.node(103,   5000.0,  0.0, 0.0, '-mass', *massML) 	
        op.node(1005,  7050.0,  0.0, 0.0) 	
        op.node(104,   8000.0,  0.0, 0.0, '-mass', *massML) 	
        op.node(105,   11000.0, 0.0, 0.0, '-mass', *massML) 	
        op.node(1006,  11550.0, 0.0, 0.0) 	
        op.node(106,   14000.0, 0.0, 0.0, '-mass', *massML) 	
        op.node(1007,  14250.0, 0.0, 0.0) 	
        op.node(107,   17000.0, 0.0, 0.0, '-mass', *massML) 	
        op.node(1008,  18350.0, 0.0, 0.0) 	
        op.node(1009,  19150.0, 0.0, 0.0) 	
        op.node(108,   20000.0, 0.0, 0.0, '-mass', *massML) 	
        op.node(1010,  20950.0, 0.0, 0.0) 	
        op.node(1011,  22950.0, 0.0, 0.0) 	
        op.node(109,   23125.0, 0.0, 0.0, '-mass', *massML) 	
        op.node(1012,  25550.0, 0.0, 0.0) 	
        op.node(110,   26000.0, 0.0, 0.0, '-mass', *massML) 	
        op.node(111,   29000.0, 0.0, 0.0, '-mass', *massML) 	
        op.node(1013,  30450.0, 0.0, 0.0) 	
        op.node(1014,  30950.0, 0.0, 0.0) 
        

        massBL = [0.3025, 0.3025, 0, 0, 0, 0]

        #Pipe Connection, Branches 
        #Branch 1
        op.node(112,  1050.0, 1500.0, 0.0, '-mass', *massBL) 	#Pipe Connection
        op.node(113,  1050.0, 4500.0, 0.0, '-mass', *massBL) 	#Pipe Connection
        op.node(1015, 1050.0, 5000.0, 0.0) 	#Pipe Connection

        #Branch 2
        op.node(114,  4250.0, 1500.0, 0.0, '-mass', *massBL) 	#Pipe Connection
        op.node(115,  4250.0, 4500.0, 0.0, '-mass', *massBL) 	#Pipe Connection
        op.node(1016, 4250.0, 5000.0, 0.0) 	#Pipe Connection

        #Branch 3
        op.node(116,  7050.0,  1500.0, 0.0, '-mass', *massBL) 	#Pipe Connection
        op.node(117,  7050.0,  4500.0, 0.0, '-mass', *massBL) 	#Pipe Connection
        op.node(1017, 7050.0,  5000.0, 0.0) 	#Pipe Connection

        #Branch 4
        op.node(118,  11550.0, 1500.0, 0.0, '-mass', *massBL) 	#Pipe Connection
        op.node(119,  11550.0, 4500.0, 0.0, '-mass', *massBL) 	#Pipe Connection
        op.node(1018, 11550.0, 5000.0, 0.0) 	#Pipe Connection

        #Branch 5
        op.node(120,  14250.0, 1500.0, 0.0, '-mass', *massBL) 	#Pipe Connection
        op.node(121,  14250.0, 4500.0, 0.0, '-mass', *massBL) 	#Pipe Connection
        op.node(1019, 14250.0, 5000.0, 0.0) 	#Pipe Connection

        #Branch 6
        op.node(122,  18350.0, 1500.0, 0.0, '-mass', *massBL) 	#Pipe Connection
        op.node(123,  18350.0, 4500.0, 0.0, '-mass', *massBL) 	#Pipe Connection
        op.node(1020, 18350.0, 5000.0, 0.0) 	#Pipe Connection

        #Branch 7
        op.node(124,  20950.0, 1500.0, 0.0, '-mass', *massBL) 	#Pipe Connection
        op.node(125,  20950.0, 4500.0, 0.0, '-mass', *massBL) 	#Pipe Connection
        op.node(1021, 20950.0, 5000.0, 0.0) 	#Pipe Connection

        #Branch 8
        op.node(126,  25550.0, 1500.0, 0.0, '-mass', *massBL) 	#Pipe Connection
        op.node(127,  25550.0, 4500.0, 0.0, '-mass', *massBL) 	#Pipe Connection
        op.node(1022, 25550.0, 5000.0, 0.0) 	#Pipe Connection

        #Branch 9
        op.node(128,  30450.0, 1500.0, 0.0, '-mass', *massBL) 	#Pipe Connection
        op.node(129,  30450.0, 4500.0, 0.0, '-mass', *massBL) 	#Pipe Connection
        op.node(1023, 30450.0, 5000.0, 0.0) 	#Pipe Connection

        #Branch 10
        op.node(1024, 2350.0, -5000.0, 0.0, '-mass', *massBL) 	#Pipe Connection
        op.node(130,  2350.0, -4500.0, 0.0, '-mass', *massBL) 	#Pipe Connection
        op.node(131,  2350.0, -1500.0, 0.0) 	#Pipe Connection

        #Branch 11
        op.node(1025, 7050.0, -5000.0, 0.0, '-mass', *massBL) 	#Pipe Connection
        op.node(132,  7050.0, -4500.0, 0.0, '-mass', *massBL) 	#Pipe Connection
        op.node(133,  7050.0, -1500.0, 0.0) 	#Pipe Connection

        #Branch 12
        op.node(1026, 11550.0, -5000.0, 0.0, '-mass', *massBL) 	#Pipe Connection
        op.node(134,  11550.0, -4500.0,	0.0, '-mass', *massBL) 	#Pipe Connection
        op.node(135,  11550.0, -1500.0,	0.0) 	#Pipe Connection

        #Branch 13
        op.node(1027, 19150.0, -5000.0,	0.0, '-mass', *massBL) 	#Pipe Connection
        op.node(136,  19150.0, -4500.0,	0.0, '-mass', *massBL) 	#Pipe Connection
        op.node(137,  19150.0, -1500.0, 0.0) 	#Pipe Connection

        #Branch 14 
        op.node(1028, 22950.0, -5000.0,	0.0, '-mass', *massBL) 	#Pipe Connection
        op.node(138,  22950.0, -4500.0, 0.0, '-mass', *massBL) 	#Pipe Connection
        op.node(139,  22950.0, -1500.0, 0.0) 	#Pipe Connection

        #Branch 15
        op.node(1029, 30950.0, -5000.0, 0.0, '-mass', *massBL) 	#Pipe Connection
        op.node(140,  30950.0, -4500.0, 0.0, '-mass', *massBL) 	#Pipe Connection
        op.node(141,  30950.0, -1500.0, 0.0) 	#Pipe Connection



        #### Nodes for nonlinear & linear springs

        #Main Line (1)
        op.node(201,  0.0,	   0.0,	5.0) 	#Spring location	
        op.node(202,  2000.0,  0.0,	5.0) 	#Spring location	
        op.node(203,  5000.0,  0.0,	5.0) 	#Spring location	
        op.node(204,  8000.0,  0.0,	5.0) 	#Spring location	
        op.node(205,  11000.0, 0.0,	5.0) 	#Spring location	
        op.node(206,  14000.0, 0.0,	5.0) 	#Spring location	
        op.node(207,  17000.0, 0.0,	5.0) 	#Spring location	
        op.node(208,  20000.0, 0.0,	5.0) 	#Spring location	
        op.node(209,  23125.0, 0.0,	5.0) 	#Spring location	
        op.node(210,  26000.0, 0.0,	5.0) 	#Spring location	
        op.node(211,  29000.0, 0.0,	5.0) 	#Spring location

        #Branches (1)
        #Branch 1
        op.node(212,  1050.0, 1500.0, 5.0) 	#Spring location
        op.node(213,  1050.0, 4500.0, 5.0) 	#Spring location

        #Branch 2
        op.node(214,  4250.0, 1500.0, 5.0) 	#Spring location
        op.node(215,  4250.0, 4500.0, 5.0) 	#Spring location

        #Branch 3
        op.node(216,  7050.0, 1500.0, 5.0) 	#Spring location
        op.node(217,  7050.0, 4500.0, 5.0) 	#Spring location

        #Branch 4
        op.node(218,  11550.0, 1500.0, 5.0) 	#Spring location
        op.node(219,  11550.0, 4500.0, 5.0) 	#Spring location

        #Branch 5
        op.node(220,  14250.0, 1500.0, 5.0) 	#Spring location
        op.node(221,  14250.0, 4500.0, 5.0) 	#Spring location

        #Branch 6
        op.node(222,  18350.0, 1500.0, 5.0) 	#Spring location
        op.node(223,  18350.0, 4500.0, 5.0) 	#Spring location

        #Branch 7
        op.node(224,  20950.0,  1500.0, 5.0) 	#Spring location
        op.node(225,  20950.0,  4500.0,	5.0) 	#Spring location

        #Branch 8
        op.node(226,  25550.0,  1500.0, 5.0) 	#Spring location
        op.node(227,  25550.0,  4500.0,	5.0) 	#Spring location

        #Branch 9
        op.node(228,  30450.0,  1500.0, 5.0) 	#Spring location
        op.node(229,  30450.0,  4500.0, 5.0) 	#Spring location

        #Branch 10
        op.node(230,  2350.0,  -4500.0,	 5.0) 	#Spring location
        op.node(231,  2350.0,  -1500.0,  5.0) 	#Spring location

        #Branch 11
        op.node(232,  7050.0,  -4500.0,  5.0) 	#Spring location
        op.node(233,  7050.0,  -1500.0,  5.0) 	#Spring location

        #Branch 12
        op.node(234,   11550.0, -4500.0, 5.0) 	#Spring location
        op.node(235,   11550.0,	-1500.0, 5.0) 	#Spring location

        #Branch 13
        op.node(236,   19150.0,  -4500.0, 5.0) 	#Spring location
        op.node(237,   19150.0,  -1500.0, 5.0) 	#Spring location

        #Branch 14
        op.node(238,   22950.0,  -4500.0,  5.0) 	#Spring location
        op.node(239,   22950.0,  -1500.0,  5.0) 	#Spring location

        #Branch 15
        op.node(240,   30950.0,	  -4500.0, 5.0) 	#Spring location
        op.node(241,   30950.0,	  -1500.0, 5.0) 	#Spring location

        #Main Line (2)
        op.node(301,  0.0,	   0.0,  5.0) 	#Spring location	
        op.node(302,  2000.0,  0.0,	 5.0) 	#Spring location	
        op.node(303,  5000.0,  0.0,	 5.0) 	#Spring location	
        op.node(304,  8000.0,  0.0,	 5.0) 	#Spring location	
        op.node(305,  11000.0, 0.0,	 5.0) 	#Spring location	
        op.node(306,  14000.0, 0.0,	 5.0) 	#Spring location	
        op.node(307,  17000.0, 0.0,	 5.0) 	#Spring location	
        op.node(308,  20000.0, 0.0,	 5.0) 	#Spring location	
        op.node(309,  23125.0, 0.0,	 5.0) 	#Spring location	
        op.node(310,  26000.0, 0.0,	 5.0) 	#Spring location	
        op.node(311,  29000.0, 0.0,	 5.0) 	#Spring location

        #Branches (2)
        #Branch 1
        op.node(312,  1050.0,   1500.0,	5.0) 	#Spring location
        op.node(313,  1050.0,   4500.0,	5.0) 	#Spring location

        #Branch 2
        op.node(314,  4250.0,   1500.0,	5.0) 	#Spring location
        op.node(315,  4250.0,   4500.0,	5.0) 	#Spring location

        #Branch 3
        op.node(316,  7050.0,   1500.0, 5.0) 	#Spring location
        op.node(317,  7050.0,   4500.0,	5.0) 	#Spring location

        #Branch 4
        op.node(318,  11550.0,  1500.0, 5.0) 	#Spring location
        op.node(319,  11550.0,	4500.0,	5.0) 	#Spring location

        #Branch 5
        op.node(320,  14250.0,	1500.0,	5.0) 	#Spring location
        op.node(321,  14250.0,	4500.0, 5.0) 	#Spring location

        #Branch 6
        op.node(322,  18350.0,  1500.0,	5.0) 	#Spring location
        op.node(323,  18350.0,  4500.0,	5.0) 	#Spring location

        #Branch 7
        op.node(324,  20950.0,  1500.0, 5.0) 	#Spring location
        op.node(325,  20950.0,  4500.0,	5.0) 	#Spring location

        #Branch 8
        op.node(326,  25550.0,  1500.0,	5.0) 	#Spring location
        op.node(327,  25550.0,  4500.0, 5.0) 	#Spring location

        #Branch 9
        op.node(328,  30450.0,  1500.0,	5.0) 	#Spring location
        op.node(329,  30450.0,  4500.0,	5.0) 	#Spring location

        #Branch 10
        op.node(330,  2350.0,  -4500.0,	5.0) 	#Spring location
        op.node(331,  2350.0,  -1500.0,	5.0) 	#Spring location

        #Branch 11
        op.node(332,  7050.0,  -4500.0,	5.0) 	#Spring location
        op.node(333,  7050.0,  -1500.0,	5.0) 	#Spring location

        #Branch 12
        op.node(334,  11550.0,	-4500.0, 5.0) 	#Spring location
        op.node(335,  11550.0,	-1500.0, 5.0) 	#Spring location

        #Branch 13
        op.node(336,  19150.0,  -4500.0, 5.0) 	#Spring location
        op.node(337,  19150.0,  -1500.0, 5.0) 	#Spring location

        #Branch 14
        op.node(338,  22950.0,  -4500.0, 5.0) 	#Spring location
        op.node(339,  22950.0,  -1500.0, 5.0) 	#Spring location

        #Branch 15
        op.node(340,  30950.0,  -4500.0, 5.0) 	#Spring location
        op.node(341,  30950.0,  -1500.0, 5.0) 	#Spring location


        ## Pipe connection nodes
        #Main Line (1)
        op.node(801,  950,	 0.0,  0.0) 	#Pipe Connection
        op.node(802,  1150,	 0.0,  0.0) 	#Pipe Connection
        op.node(803,  2250,	 0.0,  0.0) 	#Pipe Connection
        op.node(804,  2450,	 0.0,  0.0) 	#Pipe Connection
        op.node(805,  4150,	 0.0,  0.0) 	#Pipe Connection
        op.node(806,  4350,	 0.0,  0.0) 	#Pipe Connection
        op.node(807,  6950,	 0.0,  0.0) 	#Pipe Connection
        op.node(808,  7150,	 0.0,  0.0) 	#Pipe Connection
        op.node(809,  11450, 0.0,  0.0) 	#Pipe Connection
        op.node(810,  11650, 0.0,  0.0) 	#Pipe Connection
        op.node(811,  14150, 0.0,  0.0) 	#Pipe Connection
        op.node(812,  14350, 0.0,  0.0) 	#Pipe Connection
        op.node(813,  18250, 0.0,  0.0) 	#Pipe Connection
        op.node(814,  18450, 0.0,  0.0) 	#Pipe Connection
        op.node(815,  19050, 0.0,  0.0) 	#Pipe Connection
        op.node(816,  19250, 0.0,  0.0) 	#Pipe Connection
        op.node(817,  20850, 0.0,  0.0) 	#Pipe Connection
        op.node(818,  21050, 0.0,  0.0) 	#Pipe Connection
        op.node(819,  22850, 0.0,  0.0) 	#Pipe Connection
        op.node(820,  23050, 0.0,  0.0) 	#Pipe Connection
        op.node(821,  25450, 0.0,  0.0) 	#Pipe Connection
        op.node(822,  25650, 0.0,  0.0) 	#Pipe Connection
        op.node(823,  30350, 0.0,  0.0) 	#Pipe Connection
        op.node(824,  30550, 0.0,  0.0) 	#Pipe Connection
        op.node(825,  30850, 0.0,  0.0) 	#Pipe Connection

        #Branches (1)
        #Branch 1
        op.node(826,   1050,   100,	0.0) 	#Pipe Connection
        #Branch 2
        op.node(827,   4250,   100,	0.0) 	#Pipe Connection
        #Branch 3
        op.node(828,   7050,   100,	0.0) 	#Pipe Connection
        #Branch 4
        op.node(829,   11550,  100,	0.0) 	#Pipe Connection
        #Branch 5
        op.node(830,   14250,  100,	0.0) 	#Pipe Connection
        #Branch 6
        op.node(831,   18350,  100,	0.0) 	#Pipe Connection
        #Branch 7
        op.node(832,   20950,  100,	0.0) 	#Pipe Connection
        #Branch 8
        op.node(833,   25550,  100,	0.0) 	#Pipe Connection
        #Branch 9
        op.node(834,   30450,  100,	0.0) 	#Pipe Connection
        #Branch 10
        op.node(835,   2350,  -100,	0.0) 	#Pipe Connection
        #Branch 11
        op.node(836,   7050,  -100,	0.0) 	#Pipe Connection
        #Branch 12
        op.node(837,   11550, -100,	0.0) 	#Pipe Connection
        #Branch 13
        op.node(838,   19150, -100,	0.0) 	#Pipe Connection
        #Branch 14
        op.node(839,   22950, -100,	0.0) 	#Pipe Connection
        #Branch 15
        op.node(840,   30950, -100,	0.0) 	#Pipe Connection

        #Main Line (2)
        op.node(901,  950,   0.0,  0.0) 	#Pipe Connection
        op.node(902,  1150,	 0.0,  0.0) 	#Pipe Connection
        op.node(903,  2250,	 0.0,  0.0) 	#Pipe Connection
        op.node(904,  2450,	 0.0,  0.0) 	#Pipe Connection
        op.node(905,  4150,	 0.0,  0.0) 	#Pipe Connection
        op.node(906,  4350,	 0.0,  0.0) 	#Pipe Connection
        op.node(907,  6950,	 0.0,  0.0) 	#Pipe Connection
        op.node(908,  7150,	 0.0,  0.0) 	#Pipe Connection
        op.node(909,  11450, 0.0,  0.0) 	#Pipe Connection
        op.node(910,  11650, 0.0,  0.0) 	#Pipe Connection
        op.node(911,  14150, 0.0,  0.0) 	#Pipe Connection
        op.node(912,  14350, 0.0,  0.0) 	#Pipe Connection
        op.node(913,  18250, 0.0,  0.0) 	#Pipe Connection
        op.node(914,  18450, 0.0,  0.0) 	#Pipe Connection
        op.node(915,  19050, 0.0,  0.0) 	#Pipe Connection
        op.node(916,  19250, 0.0,  0.0) 	#Pipe Connection
        op.node(917,  20850, 0.0,  0.0) 	#Pipe Connection
        op.node(918,  21050, 0.0,  0.0) 	#Pipe Connection
        op.node(919,  22850, 0.0,  0.0) 	#Pipe Connection
        op.node(920,  23050, 0.0,  0.0) 	#Pipe Connection
        op.node(921,  25450, 0.0,  0.0) 	#Pipe Connection
        op.node(922,  25650, 0.0,  0.0) 	#Pipe Connection
        op.node(923,  30350, 0.0,  0.0) 	#Pipe Connection
        op.node(924,  30550, 0.0,  0.0) 	#Pipe Connection
        op.node(925,  30850, 0.0,  0.0) 	#Pipe Connection

        #Branches (2)
        #Branch 1
        op.node(926,   1050,   100,	0.0) 	#Pipe Connection
        #Branch 2
        op.node(927,   4250,   100,	0.0) 	#Pipe Connection
        #Branch 3
        op.node(928,   7050,   100,	0.0) 	#Pipe Connection
        #Branch 4
        op.node(929,   11550,  100,	0.0) 	#Pipe Connection
        #Branch 5
        op.node(930,   14250,  100,	0.0) 	#Pipe Connection
        #Branch 6
        op.node(931,   18350,  100,	0.0) 	#Pipe Connection
        #Branch 7
        op.node(932,   20950,  100,	0.0) 	#Pipe Connection
        #Branch 8
        op.node(933,   25550,  100,	0.0) 	#Pipe Connection
        #Branch 9
        op.node(934,   30450,  100,	0.0) 	#Pipe Connection
        #Branch 10
        op.node(935,   2350,  -100,	0.0) 	#Pipe Connection
        #Branch 11
        op.node(936,   7050,  -100,	0.0) 	#Pipe Connection
        #Branch 12
        op.node(937,   11550, -100,	0.0) 	#Pipe Connection
        #Branch 13
        op.node(938,   19150, -100,	0.0) 	#Pipe Connection
        #Branch 14
        op.node(939,   22950, -100,	0.0) 	#Pipe Connection
        #Branch 15
        op.node(940,   30950, -100,	0.0) 	#Pipe Connection



        # 2nd step: Boundary Condition

        op.fix(1,  1,	1,	1,	1,	1,	1) 
        op.fix(2,  1,	1,	1,	1,	1,	1) 
        op.fix(3,  1,	1,	1,	1,	1,	1)
        op.fix(4,  1,	1,	1,	1,	1,	1)
        op.fix(5,  1,	1,	1,	1,	1,	1)
        op.fix(6,  1,	1,	1,	1,	1,	1)
        op.fix(7,  1,	1,	1,	1,	1,	1)
        op.fix(8,  1,	1,	1,	1,	1,	1)
        op.fix(9,  1,	1,	1,	1,	1,	1)
        op.fix(10, 1,	1,	1,	1,	1,	1)
        op.fix(11, 1,	1,	1,	1,	1,	1)
        op.fix(12, 1,	1,	1,	1,	1,	1)
        op.fix(13, 1,	1,	1,	1,	1,	1)
        op.fix(14, 1,	1,	1,	1,	1,	1)
        op.fix(15, 1,	1,	1,	1,	1,	1)
        op.fix(16, 1,	1,	1,	1,	1,	1)
        op.fix(17, 1,	1,	1,	1,	1,	1)
        op.fix(18, 1,	1,	1,	1,	1,	1)
        op.fix(19, 1,	1,	1,	1,	1,	1)
        op.fix(20, 1,	1,	1,	1,	1,	1)
        op.fix(21, 1,	1,	1,	1,	1,	1)
        op.fix(22, 1,	1,	1,	1,	1,	1)
        op.fix(23, 1,	1,	1,	1,	1,	1)
        op.fix(24, 1,	1,	1,	1,	1,	1)
        op.fix(25, 1,	1,	1,	1,	1,	1)
        op.fix(26, 1,	1,	1,	1,	1,	1)
        op.fix(27, 1,	1,	1,	1,	1,	1)
        op.fix(28, 1,	1,	1,	1,	1,	1)
        op.fix(29, 1,	1,	1,	1,	1,	1)
        op.fix(30, 1,	1,	1,	1,	1,	1)
        op.fix(31, 1,	1,	1,	1,	1,	1)
        op.fix(32, 1,	1,	1,	1,	1,	1)
        op.fix(33, 1,	1,	1,	1,	1,	1)
        op.fix(34, 1,	1,	1,	1,	1,	1)
        op.fix(35, 1,	1,	1,	1,	1,	1)
        op.fix(36, 1,	1,	1,	1,	1,	1)
        op.fix(37, 1,	1,	1,	1,	1,	1)
        op.fix(38, 1,	1,	1,	1,	1,	1)
        op.fix(39, 1,	1,	1,	1,	1,	1)
        op.fix(40, 1,	1,	1,	1,	1,	1)
        op.fix(41, 1,	1,	1,	1,	1,	1)

        # 3rd step: Geometric transformation

        vecxz = [0,0,1]
        op.geomTransf('Linear', 1, *vecxz)
        #vecxzr = [0,1,0]
        #op.geomTransf('Linear', 2, *vecxzr)

        # 4th step: Definition Material Hysteretic Behavior: 1.C-TPS-L hysteretic bracing dir) 2.C-TPS-L Elastic perp dir) 3.C-TPL-T hysteretic bracing dir) 4.C-TPS-T Elastic perp dir

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


        # 5th step: element definition

        # Steel
        A = 7761.3 		#area of the pipe section
        E = 210000.0 	#Young modulus of the pipe material
        G = 81000.0		#Shear modulus of the pipe material
        J = 35712656.3 	#torsional moment of the inertia of cross section of pipe
        Iy = 17856328.2 		#second moment of area of the pipe about local y-axix
        Iz = 17856328.2 		#second moment of area of the pipe about local z-axix
        #massu = 0.000121		#mass per unit length of steel pipes (N*s2/mm2)
        massu = 0
        Er = 10000*E
        Gr = 10000*G


        #Main Line pipes
        op.element('elasticBeamColumn', 1,  1001,	101,	A, E, G, J, Iy, Iz, 1, '-mass', massu)
        op.element('elasticBeamColumn', 2,  101,	801, 	A, E, G, J, Iy, Iz, 1, '-mass', massu)
        op.element('elasticBeamColumn', 3,  901,	1002, 	A, E, G, J, Iy, Iz, 1, '-mass', massu)
        op.element('elasticBeamColumn', 4,  1002,	802,	A, E, G, J, Iy, Iz, 1, '-mass', massu)
        op.element('elasticBeamColumn', 5,  902, 	102,	A, E, G, J, Iy, Iz, 1, '-mass', massu)
        op.element('elasticBeamColumn', 6,  102, 	803,	A, E, G, J, Iy, Iz, 1, '-mass', massu)
        op.element('elasticBeamColumn', 7,  903,	1003,	A, E, G, J, Iy, Iz, 1, '-mass', massu)
        op.element('elasticBeamColumn', 8,  1003,	804, 	A, E, G, J, Iy, Iz, 1, '-mass', massu)
        op.element('elasticBeamColumn', 9,  904, 	805, 	A, E, G, J, Iy, Iz, 1, '-mass', massu)
        op.element('elasticBeamColumn', 10,	905, 	1004, 	A, E, G, J, Iy, Iz, 1, '-mass', massu)
        op.element('elasticBeamColumn', 11,	1004,	806,	A, E, G, J, Iy, Iz, 1, '-mass', massu)
        op.element('elasticBeamColumn', 12,	906, 	103,	A, E, G, J, Iy, Iz, 1, '-mass', massu)
        op.element('elasticBeamColumn', 13,	103,	807, 	A, E, G, J, Iy, Iz, 1, '-mass', massu)
        op.element('elasticBeamColumn', 14,	907,	1005, 	A, E, G, J, Iy, Iz, 1, '-mass', massu)
        op.element('elasticBeamColumn', 15,	1005,	808,	A, E, G, J, Iy, Iz, 1, '-mass', massu)
        op.element('elasticBeamColumn', 16,	908, 	104,	A, E, G, J, Iy, Iz, 1, '-mass', massu)
        op.element('elasticBeamColumn', 17,	104,	105, 	A, E, G, J, Iy, Iz, 1, '-mass', massu)
        op.element('elasticBeamColumn', 18,	105,	809, 	A, E, G, J, Iy, Iz, 1, '-mass', massu)
        op.element('elasticBeamColumn', 19,	909,	1006, 	A, E, G, J, Iy, Iz, 1, '-mass', massu)
        op.element('elasticBeamColumn', 20,	1006,	810, 	A, E, G, J, Iy, Iz, 1, '-mass', massu)
        op.element('elasticBeamColumn', 21,	910, 	106, 	A, E, G, J, Iy, Iz, 1, '-mass', massu)
        op.element('elasticBeamColumn', 22,	106,	811, 	A, E, G, J, Iy, Iz, 1, '-mass', massu)
        op.element('elasticBeamColumn', 23,	911,	1007, 	A, E, G, J, Iy, Iz, 1, '-mass', massu)
        op.element('elasticBeamColumn', 24,	1007,	812,	A, E, G, J, Iy, Iz, 1, '-mass', massu)
        op.element('elasticBeamColumn', 25,	912, 	107,	A, E, G, J, Iy, Iz, 1, '-mass', massu)
        op.element('elasticBeamColumn', 26,	107,	813, 	A, E, G, J, Iy, Iz, 1, '-mass', massu)
        op.element('elasticBeamColumn', 27,	913,	1008, 	A, E, G, J, Iy, Iz, 1, '-mass', massu)
        op.element('elasticBeamColumn', 28,	1008,	814, 	A, E, G, J, Iy, Iz, 1, '-mass', massu)
        op.element('elasticBeamColumn', 29,	914, 	815, 	A, E, G, J, Iy, Iz, 1, '-mass', massu)
        op.element('elasticBeamColumn', 30,	915, 	1009, 	A, E, G, J, Iy, Iz, 1, '-mass', massu)
        op.element('elasticBeamColumn', 31,	1009,	816, 	A, E, G, J, Iy, Iz, 1, '-mass', massu)
        op.element('elasticBeamColumn', 32,	916, 	108, 	A, E, G, J, Iy, Iz, 1, '-mass', massu)
        op.element('elasticBeamColumn', 33,	108, 	817, 	A, E, G, J, Iy, Iz, 1, '-mass', massu)
        op.element('elasticBeamColumn', 34,	917, 	1010, 	A, E, G, J, Iy, Iz, 1, '-mass', massu)
        op.element('elasticBeamColumn', 35,	1010,	818, 	A, E, G, J, Iy, Iz, 1, '-mass', massu)
        op.element('elasticBeamColumn', 36,	918, 	819, 	A, E, G, J, Iy, Iz, 1, '-mass', massu)
        op.element('elasticBeamColumn', 37,	919, 	1011, 	A, E, G, J, Iy, Iz, 1, '-mass', massu)
        op.element('elasticBeamColumn', 38,	1011,	820, 	A, E, G, J, Iy, Iz, 1, '-mass', massu)
        op.element('elasticBeamColumn', 39,	920, 	109, 	A, E, G, J, Iy, Iz, 1, '-mass', massu)
        op.element('elasticBeamColumn', 40,	109, 	821, 	A, E, G, J, Iy, Iz, 1, '-mass', massu)
        op.element('elasticBeamColumn', 41,	921, 	1012, 	A, E, G, J, Iy, Iz, 1, '-mass', massu)
        op.element('elasticBeamColumn', 42,	1012,	822, 	A, E, G, J, Iy, Iz, 1, '-mass', massu)
        op.element('elasticBeamColumn', 43,	922, 	110, 	A, E, G, J, Iy, Iz, 1, '-mass', massu)
        op.element('elasticBeamColumn', 44,	110, 	111,	A, E, G, J, Iy, Iz, 1, '-mass', massu)
        op.element('elasticBeamColumn', 45,	111,	823, 	A, E, G, J, Iy, Iz, 1, '-mass', massu)
        op.element('elasticBeamColumn', 46,	923,	1013, 	A, E, G, J, Iy, Iz, 1, '-mass', massu)
        op.element('elasticBeamColumn', 47,	1013,	824, 	A, E, G, J, Iy, Iz, 1, '-mass', massu)
        op.element('elasticBeamColumn', 48,	924, 	825, 	A, E, G, J, Iy, Iz, 1, '-mass', massu)
        op.element('elasticBeamColumn', 49,	925, 	1014, 	A, E, G, J, Iy, Iz, 1, '-mass', massu)

        #Positive branches
        op.element('elasticBeamColumn', 50,	1002,	826,	A,	E,	G,	J,	Iy,	Iz,	1, '-mass', massu)
        op.element('elasticBeamColumn', 51,	926, 	112,	A,	E,	G,	J,	Iy,	Iz,	1, '-mass', massu)
        op.element('elasticBeamColumn', 52,	112,	113,	A,	E,	G,	J,	Iy,	Iz,	1, '-mass', massu)
        op.element('elasticBeamColumn', 53,	113,	1015,	A,	E,	G,	J,	Iy,	Iz,	1, '-mass', massu)
        op.element('elasticBeamColumn', 54,	1004,	827,	A,	E,	G,	J,	Iy,	Iz,	1, '-mass', massu)
        op.element('elasticBeamColumn', 55,	927, 	114,	A,	E,	G,	J,	Iy,	Iz,	1, '-mass', massu)
        op.element('elasticBeamColumn', 56,	114,	115,	A,	E,	G,	J,	Iy,	Iz,	1, '-mass', massu)
        op.element('elasticBeamColumn', 57,	115,	1016,	A,	E,	G,	J,	Iy,	Iz,	1, '-mass', massu)
        op.element('elasticBeamColumn', 58,	1005,	828,	A,	E,	G,	J,	Iy,	Iz,	1, '-mass', massu)
        op.element('elasticBeamColumn', 59,	928, 	116,	A,	E,	G,	J,	Iy,	Iz,	1, '-mass', massu)
        op.element('elasticBeamColumn', 60,	116,	117,	A,	E,	G,	J,	Iy,	Iz,	1, '-mass', massu)
        op.element('elasticBeamColumn', 61,	117,	1017,	A,	E,	G,	J,	Iy,	Iz,	1, '-mass', massu)
        op.element('elasticBeamColumn', 62,	1006,	829,	A,	E,	G,	J,	Iy,	Iz,	1, '-mass', massu)
        op.element('elasticBeamColumn', 63,	929, 	118,	A,	E,	G,	J,	Iy,	Iz,	1, '-mass', massu)
        op.element('elasticBeamColumn', 64,	118,	119,	A,	E,	G,	J,	Iy,	Iz,	1, '-mass', massu)
        op.element('elasticBeamColumn', 65,	119,	1018,	A,	E,	G,	J,	Iy,	Iz,	1, '-mass', massu)
        op.element('elasticBeamColumn', 66,	1007,	830,	A,	E,	G,	J,	Iy,	Iz,	1, '-mass', massu)
        op.element('elasticBeamColumn', 67,	930, 	120,	A,	E,	G,	J,	Iy,	Iz,	1, '-mass', massu)
        op.element('elasticBeamColumn', 68,	120,	121,	A,	E,	G,	J,	Iy,	Iz,	1, '-mass', massu)
        op.element('elasticBeamColumn', 69,	121,	1019,	A,	E,	G,	J,	Iy,	Iz,	1, '-mass', massu)
        op.element('elasticBeamColumn', 70,	1008,	831,	A,	E,	G,	J,	Iy,	Iz,	1, '-mass', massu)
        op.element('elasticBeamColumn', 71,	931, 	122,	A,	E,	G,	J,	Iy,	Iz,	1, '-mass', massu)
        op.element('elasticBeamColumn', 72,	122,	123,	A,	E,	G,	J,	Iy,	Iz,	1, '-mass', massu)
        op.element('elasticBeamColumn', 73,	123,	1020,	A,	E,	G,	J,	Iy,	Iz,	1, '-mass', massu)
        op.element('elasticBeamColumn', 74,	1010,	832,	A,	E,	G,	J,	Iy,	Iz,	1, '-mass', massu)
        op.element('elasticBeamColumn', 75,	932, 	124,	A,	E,	G,	J,	Iy,	Iz,	1, '-mass', massu)
        op.element('elasticBeamColumn', 76,	124,	125,	A,	E,	G,	J,	Iy,	Iz,	1, '-mass', massu)
        op.element('elasticBeamColumn', 77,	125,	1021,	A,	E,	G,	J,	Iy,	Iz,	1, '-mass', massu)
        op.element('elasticBeamColumn', 78,	1012,	833,	A,	E,	G,	J,	Iy,	Iz,	1, '-mass', massu)
        op.element('elasticBeamColumn', 79,	933, 	126,	A,	E,	G,	J,	Iy,	Iz,	1, '-mass', massu)
        op.element('elasticBeamColumn', 80,	126,	127,	A,	E,	G,	J,	Iy,	Iz,	1, '-mass', massu)
        op.element('elasticBeamColumn', 81,	127,	1022,	A,	E,	G,	J,	Iy,	Iz,	1, '-mass', massu)
        op.element('elasticBeamColumn', 82,	1013,	834,	A,	E,	G,	J,	Iy,	Iz,	1, '-mass', massu)
        op.element('elasticBeamColumn', 83,	934, 	128,	A,	E,	G,	J,	Iy,	Iz,	1, '-mass', massu)
        op.element('elasticBeamColumn', 84,	128,	129,	A,	E,	G,	J,	Iy,	Iz,	1, '-mass', massu)
        op.element('elasticBeamColumn', 85,	129,	1023,	A,	E,	G,	J,	Iy,	Iz,	1, '-mass', massu)

        #Negative branches
        op.element('elasticBeamColumn', 86,	1024,	130,	A,	E,	G,	J,	Iy,	Iz,	1, '-mass', massu)
        op.element('elasticBeamColumn', 87,	130,	131,	A,	E,	G,	J,	Iy,	Iz,	1, '-mass', massu)
        op.element('elasticBeamColumn', 88,	131,	835, 	A,	E,	G,	J,	Iy,	Iz,	1, '-mass', massu)
        op.element('elasticBeamColumn', 89,	935,	1003,	A,	E,	G,	J,	Iy,	Iz,	1, '-mass', massu)
        op.element('elasticBeamColumn', 90,	1025,	132,	A,	E,	G,	J,	Iy,	Iz,	1, '-mass', massu)
        op.element('elasticBeamColumn', 91,	132,	133,	A,	E,	G,	J,	Iy,	Iz,	1, '-mass', massu)
        op.element('elasticBeamColumn', 92,	133,	836, 	A,	E,	G,	J,	Iy,	Iz,	1, '-mass', massu)
        op.element('elasticBeamColumn', 93,	936,	1005,	A,	E,	G,	J,	Iy,	Iz,	1, '-mass', massu)
        op.element('elasticBeamColumn', 94,	1026,	134,	A,	E,	G,	J,	Iy,	Iz,	1, '-mass', massu)
        op.element('elasticBeamColumn', 95,	134,	135,	A,	E,	G,	J,	Iy,	Iz,	1, '-mass', massu)
        op.element('elasticBeamColumn', 96,	135,	837, 	A,	E,	G,	J,	Iy,	Iz,	1, '-mass', massu)
        op.element('elasticBeamColumn', 97,	937,	1006,	A,	E,	G,	J,	Iy,	Iz,	1, '-mass', massu)
        op.element('elasticBeamColumn', 98,	1027,	136,	A,	E,	G,	J,	Iy,	Iz,	1, '-mass', massu)
        op.element('elasticBeamColumn', 99,	136,	137,	A,	E,	G,	J,	Iy,	Iz,	1, '-mass', massu)
        op.element('elasticBeamColumn', 100,	137,	838, 	A,	E,	G,	J,	Iy,	Iz,	1, '-mass', massu)
        op.element('elasticBeamColumn', 101,	938,	1009,	A,	E,	G,	J,	Iy,	Iz,	1, '-mass', massu)
        op.element('elasticBeamColumn', 102,	1028,	138,	A,	E,	G,	J,	Iy,	Iz,	1, '-mass', massu)
        op.element('elasticBeamColumn', 103,	138,	139,	A,	E,	G,	J,	Iy,	Iz,	1, '-mass', massu)
        op.element('elasticBeamColumn', 104,	139,	839, 	A,	E,	G,	J,	Iy,	Iz,	1, '-mass', massu)
        op.element('elasticBeamColumn', 105,	939,	1011,	A,	E,	G,	J,	Iy,	Iz,	1, '-mass', massu)
        op.element('elasticBeamColumn', 106,	1029,	140,	A,	E,	G,	J,	Iy,	Iz,	1, '-mass', massu)
        op.element('elasticBeamColumn', 107,	140,	141,	A,	E,	G,	J,	Iy,	Iz,	1, '-mass', massu)
        op.element('elasticBeamColumn', 108,	141,	840, 	A,	E,	G,	J,	Iy,	Iz,	1, '-mass', massu)
        op.element('elasticBeamColumn', 109,	940,	1014,	A,	E,	G,	J,	Iy,	Iz,	1, '-mass', massu)


        #Rigid Links
        op.rigidLink('beam', 1,	    201)	#rigid link
        op.rigidLink('beam', 2,	    202)	#rigid link
        op.rigidLink('beam', 3,	    203)	#rigid link
        op.rigidLink('beam', 4,	    204)	#rigid link
        op.rigidLink('beam', 5,	    205)	#rigid link
        op.rigidLink('beam', 6,	    206)	#rigid link
        op.rigidLink('beam', 7,	    207)	#rigid link
        op.rigidLink('beam', 8,	    208)	#rigid link
        op.rigidLink('beam', 9,	    209)	#rigid link
        op.rigidLink('beam', 10,	210)	#rigid link
        op.rigidLink('beam', 11,	211)	#rigid link
        op.rigidLink('beam', 12,	212)	#rigid link
        op.rigidLink('beam', 13,	213)	#rigid link
        op.rigidLink('beam', 14,	214)	#rigid link
        op.rigidLink('beam', 15,	215)	#rigid link
        op.rigidLink('beam', 16,	216)	#rigid link
        op.rigidLink('beam', 17,	217)	#rigid link
        op.rigidLink('beam', 18,	218)	#rigid link
        op.rigidLink('beam', 19,	219)	#rigid link
        op.rigidLink('beam', 20,	220)	#rigid link
        op.rigidLink('beam', 21,	221)	#rigid link
        op.rigidLink('beam', 22,	222)	#rigid link
        op.rigidLink('beam', 23,	223)	#rigid link
        op.rigidLink('beam', 24,	224)	#rigid link
        op.rigidLink('beam', 25,	225)	#rigid link
        op.rigidLink('beam', 26,	226)	#rigid link
        op.rigidLink('beam', 27,	227)	#rigid link
        op.rigidLink('beam', 28,	228)	#rigid link
        op.rigidLink('beam', 29,	229)	#rigid link
        op.rigidLink('beam', 30,	230)	#rigid link
        op.rigidLink('beam', 31,	231)	#rigid link
        op.rigidLink('beam', 32,	232)	#rigid link
        op.rigidLink('beam', 33,	233)	#rigid link
        op.rigidLink('beam', 34,	234)	#rigid link
        op.rigidLink('beam', 35,	235)	#rigid link
        op.rigidLink('beam', 36,	236)	#rigid link
        op.rigidLink('beam', 37,	237)	#rigid link
        op.rigidLink('beam', 38,	238)	#rigid link
        op.rigidLink('beam', 39,	239)	#rigid link
        op.rigidLink('beam', 40,	240)	#rigid link
        op.rigidLink('beam', 41,	241)	#rigid link

        op.rigidLink('beam', 301, 101)	#rigid link
        op.rigidLink('beam', 302, 102)	#rigid link
        op.rigidLink('beam', 303, 103)	#rigid link
        op.rigidLink('beam', 304, 104)	#rigid link
        op.rigidLink('beam', 305, 105)	#rigid link
        op.rigidLink('beam', 306, 106)	#rigid link
        op.rigidLink('beam', 307, 107)	#rigid link
        op.rigidLink('beam', 308, 108)	#rigid link
        op.rigidLink('beam', 309, 109)	#rigid link
        op.rigidLink('beam', 310, 110)	#rigid link
        op.rigidLink('beam', 311, 111)	#rigid link
        op.rigidLink('beam', 312, 112)	#rigid link
        op.rigidLink('beam', 313, 113)	#rigid link
        op.rigidLink('beam', 314, 114)	#rigid link
        op.rigidLink('beam', 315, 115)	#rigid link
        op.rigidLink('beam', 316, 116)	#rigid link
        op.rigidLink('beam', 317, 117)	#rigid link
        op.rigidLink('beam', 318, 118)	#rigid link
        op.rigidLink('beam', 319, 119)	#rigid link
        op.rigidLink('beam', 320, 120)	#rigid link
        op.rigidLink('beam', 321, 121)	#rigid link
        op.rigidLink('beam', 322, 122)	#rigid link
        op.rigidLink('beam', 323, 123)	#rigid link
        op.rigidLink('beam', 324, 124)	#rigid link
        op.rigidLink('beam', 325, 125)	#rigid link
        op.rigidLink('beam', 326, 126)	#rigid link
        op.rigidLink('beam', 327, 127)	#rigid link
        op.rigidLink('beam', 328, 128)	#rigid link
        op.rigidLink('beam', 329, 129)	#rigid link
        op.rigidLink('beam', 330, 130)	#rigid link
        op.rigidLink('beam', 331, 131)	#rigid link
        op.rigidLink('beam', 332, 132)	#rigid link
        op.rigidLink('beam', 333, 133)	#rigid link
        op.rigidLink('beam', 334, 134)	#rigid link
        op.rigidLink('beam', 335, 135)	#rigid link
        op.rigidLink('beam', 336, 136)	#rigid link
        op.rigidLink('beam', 337, 137)	#rigid link
        op.rigidLink('beam', 338, 138)	#rigid link
        op.rigidLink('beam', 339, 139)	#rigid link
        op.rigidLink('beam', 340, 140)	#rigid link
        op.rigidLink('beam', 341, 141)	#rigid link


        #5.2: Braces behaviour

        #Main Line	
        op.element('zeroLength',  501,	201,  301,  '-mat',   3, 3, 4, 4, 4, 4,	'-dir',  1, 2, 3, 4, 5, 6) #Typology of subassembly
        op.element('zeroLength',  502,	202,  302,  '-mat',   3, 3, 4, 4, 4, 4,	'-dir',  1, 2, 3, 4, 5, 6) #Typology of subassembly
        op.element('zeroLength',  503,	203,  303,  '-mat',   3, 2, 4, 4, 4, 4,	'-dir',  1, 2, 3, 4, 5, 6) #Typology of subassembly
        op.element('zeroLength',  504,	204,  304,  '-mat',   3, 3, 4, 4, 4, 4,	'-dir',  1, 2, 3, 4, 5, 6) #Typology of subassembly
        op.element('zeroLength',  505,	205,  305,  '-mat',   3, 3, 4, 4, 4, 4,	'-dir',  1, 2, 3, 4, 5, 6) #Typology of subassembly 
        op.element('zeroLength',  506,	206,  306,  '-mat',   1, 3, 4, 4, 4, 4,	'-dir',  1, 2, 3, 4, 5, 6) #Typology of subassembly
        op.element('zeroLength',  507,	207,  307,  '-mat',   3, 3, 4, 4, 4, 4,	'-dir',  1, 2, 3, 4, 5, 6) #Typology of subassembly
        op.element('zeroLength',  508,	208,  308,  '-mat',   3, 3, 4, 4, 4, 4,	'-dir',  1, 2, 3, 4, 5, 6) #Typology of subassembly
        op.element('zeroLength',  509,	209,  309,  '-mat',   3, 2, 4, 4, 4, 4,	'-dir',  1, 2, 3, 4, 5, 6) #Typology of subassembly
        op.element('zeroLength',  510,	210,  310,  '-mat',   3, 3, 4, 4, 4, 4,	'-dir',  1, 2, 3, 4, 5, 6) #Typology of subassembly
        op.element('zeroLength',  511,	211,  311,  '-mat',   3, 3, 4, 4, 4, 4,	'-dir',  1, 2, 3, 4, 5, 6) #Typology of subassembly

        #Positive branches
        op.element('zeroLength',  512,	212,  312,  '-mat',   2, 1, 4, 4, 4, 4,	'-dir',  1, 2, 3, 4, 5, 6) #Typology of subassembly
        op.element('zeroLength',  513,	213,  313,  '-mat',   3, 3, 4, 4, 4, 4,	'-dir',  1, 2, 3, 4, 5, 6) #Typology of subassembly

        op.element('zeroLength',  514,	214,  314,  '-mat',   2, 1, 4, 4, 4, 4,	'-dir',  1, 2, 3, 4, 5, 6) #Typology of subassembly
        op.element('zeroLength',  515,	215,  315,  '-mat',   3, 3, 4, 4, 4, 4,	'-dir',  1, 2, 3, 4, 5, 6) #Typology of subassembly

        op.element('zeroLength',  516,	216,  316,  '-mat',   2, 1, 4, 4, 4, 4,	'-dir',  1, 2, 3, 4, 5, 6) #Typology of subassembly
        op.element('zeroLength',  517,	217,  317,  '-mat',   3, 3, 4, 4, 4, 4,	'-dir',  1, 2, 3, 4, 5, 6) #Typology of subassembly

        op.element('zeroLength',  518,	218,  318,  '-mat',   2, 1, 4, 4, 4, 4,	'-dir',  1, 2, 3, 4, 5, 6) #Typology of subassembly
        op.element('zeroLength',  519,	219,  319,  '-mat',   3, 3, 4, 4, 4, 4,	'-dir',  1, 2, 3, 4, 5, 6) #Typology of subassembly

        op.element('zeroLength',  520,	220,  320,  '-mat',   2, 1, 4, 4, 4, 4,	'-dir',  1, 2, 3, 4, 5, 6) #Typology of subassembly
        op.element('zeroLength',  521,	221,  321,  '-mat',   3, 3, 4, 4, 4, 4,	'-dir',  1, 2, 3, 4, 5, 6) #Typology of subassembly

        op.element('zeroLength',  522,	222,  322,  '-mat',   2, 1, 4, 4, 4, 4,	'-dir',  1, 2, 3, 4, 5, 6) #Typology of subassembly
        op.element('zeroLength',  523,	223,  323,  '-mat',   3, 3, 4, 4, 4, 4,	'-dir',  1, 2, 3, 4, 5, 6) #Typology of subassembly

        op.element('zeroLength',  524,	224,  324,  '-mat',   2, 1, 4, 4, 4, 4,	'-dir',  1, 2, 3, 4, 5, 6) #Typology of subassembly
        op.element('zeroLength',  525,	225,  325,  '-mat',   3, 3, 4, 4, 4, 4,	'-dir',  1, 2, 3, 4, 5, 6) #Typology of subassembly

        op.element('zeroLength',  526,	226,  326,  '-mat',   2, 1, 4, 4, 4, 4,	'-dir',  1, 2, 3, 4, 5, 6) #Typology of subassembly
        op.element('zeroLength',  527,	227,  327,  '-mat',   3, 3, 4, 4, 4, 4,	'-dir',  1, 2, 3, 4, 5, 6) #Typology of subassembly

        op.element('zeroLength',  528,	228,  328,  '-mat',   2, 1, 4, 4, 4, 4,	'-dir',  1, 2, 3, 4, 5, 6) #Typology of subassembly
        op.element('zeroLength',  529,	229,  329,  '-mat',   3, 3, 4, 4, 4, 4,	'-dir',  1, 2, 3, 4, 5, 6) #Typology of subassembly

        #Negative branches
        op.element('zeroLength',  530,	230,  330,  '-mat',   2, 1, 4, 4, 4, 4,	'-dir',  1, 2, 3, 4, 5, 6) #Typology of subassembly
        op.element('zeroLength',  531,	231,  331,  '-mat',   3, 3, 4, 4, 4, 4,	'-dir',  1, 2, 3, 4, 5, 6) #Typology of subassembly

        op.element('zeroLength',  532,	232,  332,  '-mat',   2, 1, 4, 4, 4, 4,	'-dir',  1, 2, 3, 4, 5, 6) #Typology of subassembly
        op.element('zeroLength',  533,	233,  333,  '-mat',   3, 3, 4, 4, 4, 4,	'-dir',  1, 2, 3, 4, 5, 6) #Typology of subassembly

        op.element('zeroLength',  534,	234,  334,  '-mat',   2, 1, 4, 4, 4, 4,	'-dir',  1, 2, 3, 4, 5, 6) #Typology of subassembly
        op.element('zeroLength',  535,	235,  335,  '-mat',   3, 3, 4, 4, 4, 4,	'-dir',  1, 2, 3, 4, 5, 6) #Typology of subassembly

        op.element('zeroLength',  536,	236,  336,  '-mat',   2, 1, 4, 4, 4, 4,	'-dir',  1, 2, 3, 4, 5, 6) #Typology of subassembly
        op.element('zeroLength',  537,	237,  337,  '-mat',   3, 3, 4, 4, 4, 4,	'-dir',  1, 2, 3, 4, 5, 6) #Typology of subassembly

        op.element('zeroLength',  538,	238,  338,  '-mat',   2, 1, 4, 4, 4, 4,	'-dir',  1, 2, 3, 4, 5, 6) #Typology of subassembly
        op.element('zeroLength',  539,	239,  339,  '-mat',   3, 3, 4, 4, 4, 4,	'-dir',  1, 2, 3, 4, 5, 6) #Typology of subassembly

        op.element('zeroLength',  540,	240,  340,  '-mat',   2, 1, 4, 4, 4, 4,	'-dir',  1, 2, 3, 4, 5, 6) #Typology of subassembly
        op.element('zeroLength',  541,	241,  341,  '-mat',   3, 3, 4, 4, 4, 4,	'-dir',  1, 2, 3, 4, 5, 6) #Typology of subassembly

        nodesX = [1001, 101, 1002, 102, 1003, 1004, 103, 1005, 104, 105, 1006, 106, 1007, 107, 1008, 1009, 108, 1010, 1011, 109, 1012, 110, 111, 1013, 1014, 
                  112, 113, 1015, 114, 115, 1016, 116, 117, 1017, 118, 119, 1018, 120, 121, 1019, 122, 123, 1020, 124, 125, 1021, 126, 127, 1022, 128, 129, 
                  1023, 1024, 130, 131, 1025, 132, 133, 1026, 134, 135, 1027, 136, 137, 1028, 138, 139, 1029, 140, 141]
        
        nodesXt = [104,108,113,115,117,119,121,123,125,127,129,131,133,135,137,139,141]
        nodesXp = []

        for i in range(len(nodesX)):
            if nodesX[i] not in nodesXt:
                nodesXp.append(nodesX[i])
                   
                  
        nodesY = [1001, 101, 1002, 102, 1003, 1004, 103, 1005, 104, 105, 1006, 106, 1007, 107, 1008, 1009, 108, 1010, 1011, 109, 1012, 110, 111, 1013, 1014, 
                  112, 113, 1015, 114, 115, 1016, 116, 117, 1017, 118, 119, 1018, 120, 121, 1019, 122, 123, 1020, 124, 125, 1021, 126, 127, 1022, 128, 129, 
                  1023, 1024, 130, 131, 1025, 132, 133, 1026, 134, 135, 1027, 136, 137, 1028, 138, 139, 1029, 140, 141]
                  
        nodesYt = [102,106,110,113,115,117,119,121,123,125,127,129,131,133,135,137,139,141]
        nodesYp = []

        for i in range(len(nodesY)):
            if nodesY[i] not in nodesYt:
                nodesYp.append(nodesY[i])

        ## Springs for pipe joints

        op.element('zeroLength',   701,	801,  901,  '-mat',  4, 4, 4, 4, 4, 8, '-dir', 1,2,3,4,5,6) #Typology of subassembly
        op.element('zeroLength',   702,	802,  902,  '-mat',  4, 4, 4, 4, 4, 8, '-dir', 1,2,3,4,5,6) #Typology of subassembly
        op.element('zeroLength',   703,	803,  903,  '-mat',  4, 4, 4, 4, 4, 8, '-dir', 1,2,3,4,5,6) #Typology of subassembly
        op.element('zeroLength',   704,	804,  904,  '-mat',  4, 4, 4, 4, 4, 8, '-dir', 1,2,3,4,5,6) #Typology of subassembly
        op.element('zeroLength',   705,	805,  905,  '-mat',  4, 4, 4, 4, 4, 8, '-dir', 1,2,3,4,5,6) #Typology of subassembly 
        op.element('zeroLength',   706,	806,  906,  '-mat',  4, 4, 4, 4, 4, 8, '-dir', 1,2,3,4,5,6) #Typology of subassembly
        op.element('zeroLength',   707,	807,  907,  '-mat',  4, 4, 4, 4, 4, 8, '-dir', 1,2,3,4,5,6) #Typology of subassembly
        op.element('zeroLength',   708,	808,  908,  '-mat',  4, 4, 4, 4, 4, 8, '-dir', 1,2,3,4,5,6) #Typology of subassembly
        op.element('zeroLength',   709,	809,  909,  '-mat',  4, 4, 4, 4, 4, 8, '-dir', 1,2,3,4,5,6) #Typology of subassembly
        op.element('zeroLength',   710,	810,  910,  '-mat',  4, 4, 4, 4, 4, 8, '-dir', 1,2,3,4,5,6) #Typology of subassembly
        op.element('zeroLength',   711,	811,  911,  '-mat',  4, 4, 4, 4, 4, 8, '-dir', 1,2,3,4,5,6) #Typology of subassembly
        op.element('zeroLength',   712,	812,  912,  '-mat',  4, 4, 4, 4, 4, 8, '-dir', 1,2,3,4,5,6) #Typology of subassembly
        op.element('zeroLength',   713,	813,  913,  '-mat',  4, 4, 4, 4, 4, 8, '-dir', 1,2,3,4,5,6) #Typology of subassembly
        op.element('zeroLength',   714,	814,  914,  '-mat',  4, 4, 4, 4, 4, 8, '-dir', 1,2,3,4,5,6) #Typology of subassembly
        op.element('zeroLength',   715,	815,  915,  '-mat',  4, 4, 4, 4, 4, 8, '-dir', 1,2,3,4,5,6) #Typology of subassembly
        op.element('zeroLength',   716,	816,  916,  '-mat',  4, 4, 4, 4, 4, 8, '-dir', 1,2,3,4,5,6) #Typology of subassembly
        op.element('zeroLength',   717,	817,  917,  '-mat',  4, 4, 4, 4, 4, 8, '-dir', 1,2,3,4,5,6) #Typology of subassembly
        op.element('zeroLength',   718,	818,  918,  '-mat',  4, 4, 4, 4, 4, 8, '-dir', 1,2,3,4,5,6) #Typology of subassembly
        op.element('zeroLength',   719,	819,  919,  '-mat',  4, 4, 4, 4, 4, 8, '-dir', 1,2,3,4,5,6) #Typology of subassembly
        op.element('zeroLength',   720,	820,  920,  '-mat',  4, 4, 4, 4, 4, 8, '-dir', 1,2,3,4,5,6) #Typology of subassembly
        op.element('zeroLength',   721,	821,  921,  '-mat',  4, 4, 4, 4, 4, 8, '-dir', 1,2,3,4,5,6) #Typology of subassembly
        op.element('zeroLength',   722,	822,  922,  '-mat',  4, 4, 4, 4, 4, 8, '-dir', 1,2,3,4,5,6) #Typology of subassembly
        op.element('zeroLength',   723,	823,  923,  '-mat',  4, 4, 4, 4, 4, 8, '-dir', 1,2,3,4,5,6) #Typology of subassembly
        op.element('zeroLength',   724,	824,  924,  '-mat',  4, 4, 4, 4, 4, 8, '-dir', 1,2,3,4,5,6) #Typology of subassembly
        op.element('zeroLength',   725,	825,  925,  '-mat',  4, 4, 4, 4, 4, 8, '-dir', 1,2,3,4,5,6) #Typology of subassembly
        op.element('zeroLength',   726,	826,  926,  '-mat',  4, 4, 4, 4, 4, 8, '-dir', 1,2,3,4,5,6) #Typology of subassembly
        op.element('zeroLength',   727,	827,  927,  '-mat',  4, 4, 4, 4, 4, 8, '-dir', 1,2,3,4,5,6) #Typology of subassembly
        op.element('zeroLength',   728,	828,  928,  '-mat',  4, 4, 4, 4, 4, 8, '-dir', 1,2,3,4,5,6) #Typology of subassembly
        op.element('zeroLength',   729,	829,  929,  '-mat',  4, 4, 4, 4, 4, 8, '-dir', 1,2,3,4,5,6) #Typology of subassembly
        op.element('zeroLength',   730,	830,  930,  '-mat',  4, 4, 4, 4, 4, 8, '-dir', 1,2,3,4,5,6) #Typology of subassembly
        op.element('zeroLength',   731,	831,  931,  '-mat',  4, 4, 4, 4, 4, 8, '-dir', 1,2,3,4,5,6) #Typology of subassembly
        op.element('zeroLength',   732,	832,  932,  '-mat',  4, 4, 4, 4, 4, 8, '-dir', 1,2,3,4,5,6) #Typology of subassembly
        op.element('zeroLength',   733,	833,  933,  '-mat',  4, 4, 4, 4, 4, 8, '-dir', 1,2,3,4,5,6) #Typology of subassembly
        op.element('zeroLength',   734,	834,  934,  '-mat',  4, 4, 4, 4, 4, 8, '-dir', 1,2,3,4,5,6) #Typology of subassembly
        op.element('zeroLength',   735,	835,  935,  '-mat',  4, 4, 4, 4, 4, 8, '-dir', 1,2,3,4,5,6) #Typology of subassembly
        op.element('zeroLength',   736,	836,  936,  '-mat',  4, 4, 4, 4, 4, 8, '-dir', 1,2,3,4,5,6) #Typology of subassembly
        op.element('zeroLength',   737,	837,  937,  '-mat',  4, 4, 4, 4, 4, 8, '-dir', 1,2,3,4,5,6) #Typology of subassembly
        op.element('zeroLength',   738,	838,  938,  '-mat',  4, 4, 4, 4, 4, 8, '-dir', 1,2,3,4,5,6) #Typology of subassembly
        op.element('zeroLength',   739,	839,  939,  '-mat',  4, 4, 4, 4, 4, 8, '-dir', 1,2,3,4,5,6) #Typology of subassembly
        op.element('zeroLength',   740,	840,  940,  '-mat',  4, 4, 4, 4, 4, 8, '-dir', 1,2,3,4,5,6) #Typology of subassembly



        # 6th step: Definition restrain displamentet and rotation
        '''
        op.equalDOF(201, 301,	3,	4,	5,	6)
        op.equalDOF(202, 302,	3,	4,	5,	6)
        op.equalDOF(203, 303,	3,	4,	5,	6)
        op.equalDOF(204, 304,	3,	4,	5,	6)
        op.equalDOF(205, 305,	3,	4,	5,	6)
        op.equalDOF(206, 306,	3,	4,	5,	6)
        op.equalDOF(207, 307,	3,	4,	5,	6)
        op.equalDOF(208, 308,	3,	4,	5,	6)
        op.equalDOF(209, 309,	3,	4,	5,	6)
        op.equalDOF(210, 310,	3,	4,	5,	6)
        op.equalDOF(211, 311,	3,	4,	5,	6)
        op.equalDOF(212, 312,	3,	4,	5,	6)
        op.equalDOF(213, 313,	3,	4,	5,	6)
        op.equalDOF(214, 314,	3,	4,	5,	6)
        op.equalDOF(215, 315,	3,	4,	5,	6)
        op.equalDOF(216, 316,	3,	4,	5,	6)
        op.equalDOF(217, 317,	3,	4,	5,	6)
        op.equalDOF(218, 318,	3,	4,	5,	6)
        op.equalDOF(219, 319,	3,	4,	5,	6)
        op.equalDOF(220, 320,	3,	4,	5,	6)
        op.equalDOF(221, 321,	3,	4,	5,	6)
        op.equalDOF(222, 322,	3,	4,	5,	6)
        op.equalDOF(223, 323,	3,	4,	5,	6)
        op.equalDOF(224, 324,	3,	4,	5,	6)
        op.equalDOF(225, 325,	3,	4,	5,	6)
        op.equalDOF(226, 326,	3,	4,	5,	6)
        op.equalDOF(227, 327,	3,	4,	5,	6)
        op.equalDOF(228, 328,	3,	4,	5,	6)
        op.equalDOF(229, 329,	3,	4,	5,	6)
        op.equalDOF(230, 330,	3,	4,	5,	6)
        op.equalDOF(231, 331,	3,	4,	5,	6)
        op.equalDOF(232, 332,	3,	4,	5,	6)
        op.equalDOF(233, 333,	3,	4,	5,	6)
        op.equalDOF(234, 334,	3,	4,	5,	6)
        op.equalDOF(235, 335,	3,	4,	5,	6)
        op.equalDOF(236, 336,	3,	4,	5,	6)
        op.equalDOF(237, 337,	3,	4,	5,	6)
        op.equalDOF(238, 338,	3,	4,	5,	6)
        op.equalDOF(239, 339,	3,	4,	5,	6)
        op.equalDOF(240, 340,	3,	4,	5,	6)
        op.equalDOF(241, 341,	3,	4,	5,	6)
  
        op.equalDOF(801, 901,	1,	2,	3,	4, 5)
        op.equalDOF(802, 902,	1,	2,	3,	4, 5)
        op.equalDOF(803, 903,	1,	2,	3,	4, 5)
        op.equalDOF(804, 904,	1,	2,	3,	4, 5)
        op.equalDOF(805, 905,	1,	2,	3,	4, 5)
        op.equalDOF(806, 906,	1,	2,	3,	4, 5)
        op.equalDOF(807, 907,	1,	2,	3,	4, 5)
        op.equalDOF(808, 908,	1,	2,	3,	4, 5)
        op.equalDOF(809, 909,	1,	2,	3,	4, 5)
        op.equalDOF(810, 910,	1,	2,	3,	4, 5)
        op.equalDOF(811, 911,	1,	2,	3,	4, 5)
        op.equalDOF(812, 912,	1,	2,	3,	4, 5)
        op.equalDOF(813, 913,	1,	2,	3,	4, 5)
        op.equalDOF(814, 914,	1,	2,	3,	4, 5)
        op.equalDOF(815, 915,	1,	2,	3,	4, 5)
        op.equalDOF(816, 916,	1,	2,	3,	4, 5)
        op.equalDOF(817, 917,	1,	2,	3,	4, 5)
        op.equalDOF(818, 918,	1,	2,	3,	4, 5)
        op.equalDOF(819, 919,	1,	2,	3,	4, 5)
        op.equalDOF(820, 920,	1,	2,	3,	4, 5)
        op.equalDOF(821, 921,	1,	2,	3,	4, 5)
        op.equalDOF(822, 922,	1,	2,	3,	4, 5)
        op.equalDOF(823, 923,	1,	2,	3,	4, 5)
        op.equalDOF(824, 924,	1,	2,	3,	4, 5)
        op.equalDOF(825, 925,	1,	2,	3,	4, 5)
        op.equalDOF(826, 926,	1,	2,	3,	4, 5)
        op.equalDOF(827, 927,	1,	2,	3,	4, 5)
        op.equalDOF(828, 928,	1,	2,	3,	4, 5)
        op.equalDOF(829, 929,	1,	2,	3,	4, 5)
        op.equalDOF(830, 930,	1,	2,	3,	4, 5)
        op.equalDOF(831, 931,	1,	2,	3,	4, 5)
        op.equalDOF(832, 932,	1,	2,	3,	4, 5)
        op.equalDOF(833, 933,	1,	2,	3,	4, 5)
        op.equalDOF(834, 934,	1,	2,	3,	4, 5)
        op.equalDOF(835, 935,	1,	2,	3,	4, 5)
        op.equalDOF(836, 936,	1,	2,	3,	4, 5)
        op.equalDOF(837, 937,	1,	2,	3,	4, 5)
        op.equalDOF(838, 938,	1,	2,	3,	4, 5)
        op.equalDOF(839, 939,	1,	2,	3,	4, 5)
        op.equalDOF(840, 940,	1,	2,	3,	4, 5)
      '''




        # 9th step: Apply of load and gravity with static analysis

        # set l -0.2315; #load per unit length of cpvc piping (N/mm)
        l = -1.183; #load per unit length of steel piping (N/mm)

        op.timeSeries('Constant', 1)
        op.pattern('Plain', 1, 1)

        op.eleLoad('-ele', 1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, '-type', '-beamUniform', 0.0, l, 0.0)
        op.eleLoad('-ele', 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56,  '-type', '-beamUniform', 0.0, l, 0.0)
        op.eleLoad('-ele', 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82,  '-type', '-beamUniform', 0.0, l, 0.0)
        op.eleLoad('-ele', 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109,  '-type', '-beamUniform', 0.0, l, 0.0)

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

        
        Name1 = np.loadtxt('Names.txt')[2*gm]
        Name2 = np.loadtxt('Names.txt')[2*gm+1]

        dts = np.loadtxt('Timesteps.txt')[2*gm]/10


        GMfact = 1 


        acc1 = 1000*np.loadtxt('./ResultsS4/FloorAcc_IM'+str(im+1)+'_'+str(int(Name1))+'.txt')[:,4]
        acc2 = 1000*np.loadtxt('./ResultsS4/FloorAcc_IM'+str(im+1)+'_'+str(int(Name2))+'.txt')[:,4]

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
        op.test('EnergyIncr',*testParams)      # determine if convergence has been achieved at the end of an iteration step
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
                    op.test('EnergyIncr',*testParams2)
                    op.algorithm('Newton','-initial')
                    print("Trying Newton with Initial Tangent ..")
                    ok = op.analyze(1,dta/2)
                    op.test('RelativeEnergyIncr',*testParams) 
                    op.algorithm('Newton') 
                if(ok != 0):
                    op.algorithm('Broyden',50)
                    op.test('EnergyIncr',*testParams2)
                    print("Trying Broyden ..")
                    ok = op.analyze(1,dta/2) 
                    op.test('RelativeEnergyIncr',*testParams) 
                    op.algorithm('Newton') 
                if(ok != 0):
                    op.algorithm('NewtonLineSearch')
                    op.test('EnergyIncr',*testParams2)
                    print("Trying NewtonWithLineSearch ..")
                    ok = op.analyze(1,dta/10)
                    op.test('RelativeEnergyIncr',*testParams) 
                    op.algorithm('Newton') # use Newton's solution algorithm: updates tangent stiffness at every iteration
                if(ok != 0):
                    print("Trying KrylovNewton ..")
                    op.algorithm('KrylovNewton') 
                    op.test('EnergyIncr',*testParams2)
                    ok = op.analyze(1,dta/20)
                    op.test('RelativeEnergyIncr',*testParams) 
                    op.algorithm('Newton')  

        if(op.getTime()<TmaxAnalysis):
            print('Problem with analysis at: '+str(op.getTime()))
        else:
            print("Ground Motion Done. End Time:"+str(op.getTime()))
        op.wipe()