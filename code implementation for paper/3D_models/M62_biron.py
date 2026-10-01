#Piping system layout without branches
# N, mm, s
import openseespy.opensees as op
import os
import numpy as np
import matplotlib.pyplot as plt
import time
import scipy as scp



op.wipe()


print('Model generation started...')

direc = './ResultsM62_biron'

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
        op.node(13,	 37000.0,  0.0,		10.0) 	#fix point	
        op.node(14,	 40000.0,  0.0,		10.0) 	#fix point	
        op.node(15,	 43000.0,  0.0,		10.0) 	#fix point
        op.node(16,	 46000.0,  0.0,		10.0) 	#fix point
        op.node(17,	 49000.0,  0.0,		10.0) 	#fix point
        op.node(18,	 52000.0,  0.0,		10.0) 	#fix point
        op.node(19,	 55000.0,  0.0,		10.0) 	#fix point
        op.node(20,	 58000.0,  0.0,		10.0) 	#fix point
        op.node(21,	 61000.0,  0.0,		10.0) 	#fix point
        op.node(22,	 64000.0,  0.0,		10.0) 	#fix point
        op.node(23,	 67000.0,  0.0,		10.0) 	#fix point
        op.node(24,	 70000.0,  0.0,		10.0) 	#fix point
        op.node(25,	 73000.0,  0.0,		10.0) 	#fix point
        op.node(26,	 76000.0,  0.0,		10.0) 	#fix point
        op.node(27,	 79000.0,  0.0,		10.0) 	#fix point

        #Cross lines fixed points trapezes
        #Second cross line
        op.node(28,	 82000.0,  1000.0,	10.0) 	#fix point
        op.node(29,	 82000.0,  4000.0,	10.0) 	#fix point
        op.node(30,	 82000.0,  7000.0,	10.0) 	#fix point
        op.node(31,	 82000.0,  10000.0,	10.0) 	#fix point
        op.node(32,	 82000.0,  13000.0,	10.0) 	#fix point
        op.node(33,	 82000.0,  16000.0,	10.0) 	#fix point
        op.node(34,	 82000.0,  19000.0,	10.0) 	#fix point
        op.node(35,	 82000.0,  22000.0,	10.0) 	#fix point
        op.node(36,	 82000.0,  25000.0,	10.0) 	#fix point
        op.node(37,	 82000.0,  28000.0,	10.0) 	#fix point
        op.node(38,	 82000.0,  31000.0,	10.0) 	#fix point
        op.node(39,	 82000.0,  34000.0,	10.0) 	#fix point
        op.node(40,	 82000.0,  37000.0,	10.0) 	#fix point
        op.node(41,	 82000.0,  40000.0,	10.0) 	#fix point
        op.node(42,	 82000.0,  43000.0,	10.0) 	#fix point
        op.node(43,	 82000.0,  46000.0,	10.0) 	#fix point
        op.node(44,	 82000.0,  49000.0,	10.0) 	#fix point
        #First cross line
        op.node(45,	 32000.0,  1000.0,	10.0) 	#fix point
        op.node(46,	 32000.0,  4000.0,	10.0) 	#fix point
        op.node(47,  32000.0,  7000.0,	10.0) 	#fix point
        op.node(48,  32000.0,  10000.0,	10.0) 	#fix point
        op.node(49,  32000.0,  13000.0,	10.0) 	#fix point
        op.node(50,  32000.0,  16000.0,	10.0) 	#fix point
        op.node(51,  32000.0,  19000.0,	10.0) 	#fix point
        op.node(52,  32000.0,  22000.0,	10.0) 	#fix point
        op.node(53,  32000.0,  25000.0,	10.0) 	#fix point
        op.node(54,  32000.0,  28000.0,	10.0) 	#fix point
        op.node(55,  32000.0,  31000.0,	10.0) 	#fix point
        op.node(56,  32000.0,  34000.0,	10.0) 	#fix point
        op.node(57,  32000.0,  37000.0,	10.0) 	#fix point
        op.node(58,  32000.0,  40000.0,	10.0) 	#fix point
        op.node(59,  32000.0,  43000.0,	10.0) 	#fix point
        op.node(60,  32000.0,  46000.0,	10.0) 	#fix point
        op.node(61,  32000.0,  49000.0,	10.0) 	#fix point


        massML = [0.37, 0.37, 0, 0, 0, 0]

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
        op.node(1002,	32000.0,	0.0,		0.0) 	#pipe connection	
        op.node(112,	34000.0,	0.0,		0.0, '-mass', *massML) 	#pipe connection	
        op.node(113,    37000.0,	0.0,		0.0, '-mass', *massML) 	#pipe connection
        op.node(114,    40000.0,	0.0,		0.0, '-mass', *massML) 	#pipe connection
        op.node(115, 	43000.0,	0.0,		0.0, '-mass', *massML) 	#pipe connection
        op.node(116, 	46000.0,	0.0,		0.0, '-mass', *massML) 	#pipe connection
        op.node(117, 	49000.0,	0.0,		0.0, '-mass', *massML) 	#pipe connection
        op.node(118, 	52000.0,	0.0,		0.0, '-mass', *massML) 	#pipe connection
        op.node(119, 	55000.0,	0.0,		0.0, '-mass', *massML) 	#pipe connection
        op.node(120, 	58000.0,	0.0,		0.0, '-mass', *massML) 	#pipe connection
        op.node(121, 	61000.0,	0.0,		0.0, '-mass', *massML) 	#pipe connection
        op.node(122, 	64000.0,	0.0,		0.0, '-mass', *massML) 	#pipe connection
        op.node(123, 	67000.0,	0.0,		0.0, '-mass', *massML) 	#pipe connection
        op.node(124,	70000.0,	0.0,		0.0, '-mass', *massML) 	#pipe connection
        op.node(125,	73000.0,	0.0,		0.0, '-mass', *massML) 	#pipe connection
        op.node(126,	76000.0,	0.0,		0.0, '-mass', *massML) 	#pipe connection
        op.node(127, 	79000.0,	0.0,		0.0, '-mass', *massML) 	#pipe connection
        op.node(1003, 	82000.0,	0.0,		0.0) 	#pipe connection



        #Cross lines pipe connections
        #Second cross line
        op.node(128, 	82000.0,	1000.0,		0.0, '-mass', *massML) 	#pipe connection
        op.node(129, 	82000.0,	4000.0,		0.0, '-mass', *massML) 	#pipe connection
        op.node(130, 	82000.0,	7000.0,		0.0, '-mass', *massML) 	#pipe connection
        op.node(131, 	82000.0,	10000.0,	0.0, '-mass', *massML) 	#pipe connection
        op.node(132, 	82000.0,	13000.0,	0.0, '-mass', *massML) 	#pipe connection
        op.node(133, 	82000.0,	16000.0,	0.0, '-mass', *massML) 	#pipe connection
        op.node(134, 	82000.0,	19000.0,	0.0, '-mass', *massML) 	#pipe connection
        op.node(135, 	82000.0,	22000.0,	0.0, '-mass', *massML) 	#pipe connection
        op.node(136, 	82000.0,	25000.0,	0.0, '-mass', *massML) 	#pipe connection
        op.node(137, 	82000.0,	28000.0,	0.0, '-mass', *massML) 	#pipe connection
        op.node(138, 	82000.0,	31000.0,	0.0, '-mass', *massML) 	#pipe connection
        op.node(139, 	82000.0,	34000.0,	0.0, '-mass', *massML) 	#pipe connection
        op.node(140, 	82000.0,	37000.0,	0.0, '-mass', *massML) 	#pipe connection
        op.node(141, 	82000.0,	40000.0,	0.0, '-mass', *massML) 	#pipe connection
        op.node(142, 	82000.0,	43000.0,	0.0, '-mass', *massML) 	#pipe connection
        op.node(143, 	82000.0,	46000.0,	0.0, '-mass', *massML) 	#pipe connection
        op.node(144,	82000.0,	49000.0,	0.0, '-mass', *massML) 	#pipe connection
        op.node(1004,	82000.0,	52000.0,	0.0) 	#pipe connection

        #First cross line
        op.node(145, 	32000.0,	1000.0,		0.0, '-mass', *massML) 	#pipe connection
        op.node(146, 	32000.0,	4000.0,		0.0, '-mass', *massML) 	#pipe connection
        op.node(147, 	32000.0,	7000.0,		0.0, '-mass', *massML) 	#pipe connection
        op.node(148, 	32000.0,	10000.0,	0.0, '-mass', *massML) 	#pipe connection
        op.node(149, 	32000.0,	13000.0,	0.0, '-mass', *massML) 	#pipe connection
        op.node(150, 	32000.0,	16000.0,	0.0, '-mass', *massML) 	#pipe connection
        op.node(151, 	32000.0,	19000.0,	0.0, '-mass', *massML) 	#pipe connection
        op.node(152, 	32000.0,	22000.0,	0.0, '-mass', *massML) 	#pipe connection
        op.node(153, 	32000.0,	25000.0,	0.0, '-mass', *massML) 	#pipe connection
        op.node(154, 	32000.0,	28000.0,	0.0, '-mass', *massML) 	#pipe connection
        op.node(155, 	32000.0,	31000.0,	0.0, '-mass', *massML) 	#pipe connection
        op.node(156, 	32000.0,	34000.0,	0.0, '-mass', *massML) 	#pipe connection
        op.node(157, 	32000.0,	37000.0,	0.0, '-mass', *massML) 	#pipe connection
        op.node(158, 	32000.0,	40000.0,	0.0, '-mass', *massML) 	#pipe connection
        op.node(159, 	32000.0,	43000.0,	0.0, '-mass', *massML) 	#pipe connection
        op.node(160, 	32000.0,	46000.0,	0.0, '-mass', *massML) 	#pipe connection
        op.node(161, 	32000.0,	49000.0,	0.0, '-mass', *massML) 	#pipe connection
        op.node(1005, 	32000.0,	52000.0,	0.0) 	#pipe connection

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
        op.node(213,	37000.0,	0.0,		5.0) 	#spring	
        op.node(214,	40000.0,	0.0,		5.0) 	#spring	
        op.node(215,	43000.0,	0.0,		5.0) 	#spring
        op.node(216,	46000.0,	0.0,		5.0) 	#spring
        op.node(217,	49000.0,	0.0,		5.0) 	#spring
        op.node(218,	52000.0,	0.0,		5.0) 	#spring
        op.node(219,	55000.0,	0.0,		5.0) 	#spring
        op.node(220,	58000.0,	0.0,		5.0) 	#spring
        op.node(221,	61000.0,	0.0,		5.0) 	#spring
        op.node(222,	64000.0,	0.0,		5.0) 	#spring
        op.node(223,	67000.0,	0.0,		5.0) 	#spring
        op.node(224,	70000.0,	0.0,		5.0) 	#spring
        op.node(225,	73000.0,	0.0,		5.0) 	#spring
        op.node(226,	76000.0,	0.0,		5.0) 	#spring
        op.node(227,	79000.0,	0.0,		5.0) 	#spring

        #Cross lines 
        #Second cross line (1)
        op.node(228,	 82000.0,	1000.0,		5.0) 	#spring
        op.node(229,	 82000.0,	4000.0,		5.0) 	#spring
        op.node(230,	 82000.0,	7000.0,		5.0) 	#spring
        op.node(231,	 82000.0,	10000.0,	5.0) 	#spring
        op.node(232,	 82000.0,	13000.0,	5.0) 	#spring
        op.node(233,	 82000.0,	16000.0,	5.0) 	#spring
        op.node(234,	 82000.0,	19000.0,	5.0) 	#spring
        op.node(235,	 82000.0,	22000.0,	5.0) 	#spring
        op.node(236,	 82000.0,	25000.0,	5.0) 	#spring
        op.node(237,	 82000.0,	28000.0,	5.0) 	#spring
        op.node(238,	 82000.0,	31000.0,	5.0) 	#spring
        op.node(239,	 82000.0,	34000.0,	5.0) 	#spring
        op.node(240,	 82000.0,	37000.0,	5.0) 	#spring
        op.node(241,	 82000.0,	40000.0,	5.0) 	#spring
        op.node(242,	 82000.0,	43000.0,	5.0) 	#spring
        op.node(243,	 82000.0,	46000.0,	5.0) 	#spring
        op.node(244,	 82000.0,	49000.0,	5.0) 	#spring

        #Second cross line (1)
        op.node(245,	 32000.0,	1000.0,	   5.0) 	#spring
        op.node(246, 	 32000.0,	4000.0,	   5.0) 	#spring
        op.node(247, 	 32000.0,	7000.0,	   5.0) 	#spring
        op.node(248, 	 32000.0,	10000.0,   5.0) 	#spring
        op.node(249, 	 32000.0,	13000.0,   5.0) 	#spring
        op.node(250, 	 32000.0,	16000.0,   5.0) 	#spring
        op.node(251, 	 32000.0,	19000.0,   5.0) 	#spring
        op.node(252, 	 32000.0,	22000.0,   5.0) 	#spring
        op.node(253, 	 32000.0,	25000.0,   5.0) 	#spring
        op.node(254, 	 32000.0,	28000.0,   5.0) 	#spring
        op.node(255, 	 32000.0,	31000.0,   5.0) 	#spring
        op.node(256, 	 32000.0,	34000.0,   5.0) 	#spring
        op.node(257, 	 32000.0,	37000.0,   5.0) 	#spring
        op.node(258,     32000.0,	40000.0,   5.0) 	#spring
        op.node(259, 	 32000.0,	43000.0,   5.0) 	#spring
        op.node(260, 	 32000.0,	46000.0,   5.0) 	#spring
        op.node(261, 	 32000.0,	49000.0,   5.0) 	#spring

        #Main Line (2)
        op.node(301,	 1000.0,	0.0,	   5.0) 	#spring	
        op.node(302,	 4000.0,	0.0,	   5.0) 	#spring	
        op.node(303,	 7000.0,	0.0,	   5.0) 	#spring	
        op.node(304,	 10000.0,   0.0,	   5.0) 	#spring	
        op.node(305,	 13000.0,	0.0,	   5.0) 	#spring	
        op.node(306,	 16000.0,	0.0,	   5.0) 	#spring	
        op.node(307,	 19000.0,	0.0,	   5.0) 	#spring	
        op.node(308,	 22000.0,	0.0,	   5.0) 	#spring	
        op.node(309,	 25000.0,	0.0,	   5.0) 	#spring	
        op.node(310,	 28000.0,	0.0,	   5.0) 	#spring	
        op.node(311,	 31000.0,	0.0,	   5.0) 	#spring	
        op.node(312,	 34000.0,	0.0,	   5.0) 	#spring	
        op.node(313,	 37000.0,	0.0,	   5.0) 	#spring	
        op.node(314,	 40000.0,	0.0,	   5.0) 	#spring	
        op.node(315,	 43000.0,	0.0,	   5.0) 	#spring
        op.node(316,	 46000.0,	0.0,	   5.0) 	#spring
        op.node(317,	 49000.0,	0.0,	   5.0) 	#spring
        op.node(318,	 52000.0,	0.0,	   5.0) 	#spring
        op.node(319,	 55000.0,	0.0,	   5.0) 	#spring
        op.node(320,	 58000.0,	0.0,	   5.0) 	#spring
        op.node(321,	 61000.0,	0.0,	   5.0) 	#spring
        op.node(322,	 64000.0,	0.0,	   5.0) 	#spring
        op.node(323,	 67000.0,	0.0,	   5.0) 	#spring
        op.node(324,	 70000.0,	0.0,	   5.0) 	#spring
        op.node(325,	 73000.0,	0.0,	   5.0) 	#spring
        op.node(326,	 76000.0,	0.0,	   5.0) 	#spring
        op.node(327,	 79000.0,	0.0,	   5.0) 	#spring

        #Second cross line (2)
        op.node(328,	 82000.0,	1000.0,		5.0) 	#spring
        op.node(329,	 82000.0,	4000.0,		5.0) 	#spring
        op.node(330,	 82000.0,	7000.0,		5.0) 	#spring
        op.node(331,	 82000.0,	10000.0,	5.0) 	#spring
        op.node(332,	 82000.0,	13000.0,	5.0) 	#spring
        op.node(333,	 82000.0,	16000.0,	5.0) 	#spring
        op.node(334,	 82000.0,	19000.0,	5.0) 	#spring
        op.node(335,	 82000.0,	22000.0,	5.0) 	#spring
        op.node(336,	 82000.0,	25000.0,	5.0) 	#spring
        op.node(337,	 82000.0,	28000.0,	5.0) 	#spring
        op.node(338,	 82000.0,	31000.0,	5.0) 	#spring
        op.node(339,	 82000.0,	34000.0,	5.0) 	#spring
        op.node(340,	 82000.0,	37000.0,	5.0) 	#spring
        op.node(341,	 82000.0,	40000.0,	5.0) 	#spring
        op.node(342,	 82000.0,	43000.0,	5.0) 	#spring
        op.node(343,	 82000.0,	46000.0,	5.0) 	#spring
        op.node(344,	 82000.0,	49000.0,	5.0) 	#spring

        #First cross line (2)
        op.node(345,	32000.0,	1000.0,		5.0) 	#spring
        op.node(346, 	32000.0,	4000.0,		5.0) 	#spring
        op.node(347, 	32000.0,	7000.0,		5.0) 	#spring
        op.node(348, 	32000.0,	10000.0,	5.0) 	#spring
        op.node(349, 	32000.0,	13000.0,	5.0) 	#spring
        op.node(350, 	32000.0,	16000.0,	5.0) 	#spring
        op.node(351, 	32000.0,	19000.0,	5.0) 	#spring
        op.node(352, 	32000.0,	22000.0,	5.0) 	#spring
        op.node(353, 	32000.0,	25000.0,	5.0) 	#spring
        op.node(354, 	32000.0,	28000.0,	5.0) 	#spring
        op.node(355, 	32000.0,	31000.0,		5.0) 	#spring
        op.node(356, 	32000.0,	34000.0,	5.0) 	#spring
        op.node(357, 	32000.0,	37000.0,	5.0) 	#spring
        op.node(358, 	32000.0,	40000.0,	5.0) 	#spring
        op.node(359, 	32000.0,	43000.0,	5.0) 	#spring
        op.node(360, 	32000.0,	46000.0,	5.0) 	#spring
        op.node(361, 	32000.0,	49000.0,	5.0) 	#spring

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
        op.node(811, 	31900.0,	0.0,		0.0) 	#Pipe connection
        op.node(812, 	32100.0,	0.0,		0.0) 	#Pipe connection
        op.node(813, 	37940.0,	0.0,		0.0) 	#Pipe connection
        op.node(814, 	38060.0,	0.0,		0.0) 	#Pipe connection
        op.node(815, 	43940.0,	0.0,		0.0) 	#Pipe connection
        op.node(816, 	44060.0,	0.0,		0.0) 	#Pipe connection
        op.node(817, 	49940.0,	0.0,		0.0) 	#Pipe connection
        op.node(818, 	50060.0,	0.0,		0.0) 	#Pipe connection
        op.node(819, 	55940.0,	0.0,		0.0) 	#Pipe connection
        op.node(820, 	56060.0,	0.0,		0.0) 	#Pipe connection
        op.node(821, 	61940.0,	0.0,		0.0) 	#Pipe connection
        op.node(822, 	62060.0,	0.0,		0.0) 	#Pipe connection
        op.node(823, 	67940.0,	0.0,		0.0) 	#Pipe connection
        op.node(824, 	68060.0,	0.0,		0.0) 	#Pipe connection
        op.node(825, 	73940.0,	0.0,		0.0) 	#Pipe connection
        op.node(826, 	74060.0,	0.0,		0.0) 	#Pipe connection
        op.node(827, 	79940.0,	0.0,		0.0) 	#Pipe connection
        op.node(828, 	80060.0,	0.0,		0.0) 	#Pipe connection
        op.node(829, 	81900.0,	0.0,		0.0) 	#Pipe connection

        #First cross line (1)
        op.node(830, 	32000.0,	100.0,	    0.0) 	#Pipe connection
        op.node(831, 	32000.0,	5940.0,	    0.0) 	#Pipe connection
        op.node(832, 	32000.0,	6060.0,	    0.0) 	#Pipe connection
        op.node(833, 	32000.0,	11940.0,	0.0) 	#Pipe connection
        op.node(834, 	32000.0,	12060.0,	0.0) 	#Pipe connection
        op.node(835, 	32000.0,	17940.0,	0.0) 	#Pipe connection
        op.node(836, 	32000.0,	18060.0,	0.0) 	#Pipe connection
        op.node(837, 	32000.0,	23940.0,	0.0) 	#Pipe connection
        op.node(838, 	32000.0,	24060.0,	0.0) 	#Pipe connection
        op.node(839, 	32000.0,	29940.0,	0.0) 	#Pipe connection
        op.node(840, 	32000.0,	30060.0,	0.0) 	#Pipe connection
        op.node(841, 	32000.0,	35940.0,	0.0) 	#Pipe connection
        op.node(842, 	32000.0,	36060.0,	0.0) 	#Pipe connection
        op.node(843, 	32000.0,	41940.0,	0.0) 	#Pipe connection
        op.node(844, 	32000.0,	42060.0,	0.0) 	#Pipe connection
        op.node(845, 	32000.0,	47940.0,	0.0) 	#Pipe connection
        op.node(846, 	32000.0,	48060.0,	0.0) 	#Pipe connection

        #Second cross line (1)
        op.node(847, 	82000.0,	100.0,	    0.0) 	#Pipe connection
        op.node(848, 	82000.0,	5940.0,	    0.0) 	#Pipe connection
        op.node(849, 	82000.0,	6060.0,	    0.0) 	#Pipe connection
        op.node(850, 	82000.0,	11940.0,	0.0) 	#Pipe connection
        op.node(851, 	82000.0,	12060.0,	0.0) 	#Pipe connection
        op.node(852, 	82000.0,	17940.0,	0.0) 	#Pipe connection
        op.node(853, 	82000.0,	18060.0,	0.0) 	#Pipe connection
        op.node(854, 	82000.0,	23940.0,	0.0) 	#Pipe connection
        op.node(855, 	82000.0,	24060.0,	0.0) 	#Pipe connection
        op.node(856, 	82000.0,	29940.0,	0.0) 	#Pipe connection
        op.node(857, 	82000.0,	30060.0,	0.0) 	#Pipe connection
        op.node(858, 	82000.0,	35940.0,	0.0) 	#Pipe connection
        op.node(859, 	82000.0,	36060.0,	0.0) 	#Pipe connection
        op.node(860, 	82000.0,	41940.0,	0.0) 	#Pipe connection
        op.node(861, 	82000.0,	42060.0,	0.0) 	#Pipe connection
        op.node(862, 	82000.0,	47940.0,	0.0) 	#Pipe connection
        op.node(863, 	82000.0,	48060.0,	0.0) 	#Pipe connection

        #Main line (2)
        op.node(901, 	5940.0,	    0.0,		0.0) 	#Pipe connection
        op.node(902, 	6060.0,	    0.0,		0.0) 	#Pipe connection
        op.node(903, 	11940.0,	0.0,		0.0) 	#Pipe connection
        op.node(904, 	12060.0,	0.0,		0.0) 	#Pipe connection
        op.node(905, 	17940.0,	0.0,		0.0) 	#Pipe connection
        op.node(906, 	18060.0,	0.0,		0.0) 	#Pipe connection
        op.node(907, 	23940.0,	0.0,		0.0) 	#Pipe connection
        op.node(908, 	24060.0,	0.0,		0.0) 	#Pipe connection
        op.node(909, 	29940.0,	0.0,		0.0) 	#Pipe connection
        op.node(910, 	30060.0,	0.0,		0.0) 	#Pipe connection
        op.node(911, 	31900.0,	0.0,		0.0) 	#Pipe connection
        op.node(912, 	32100.0,	0.0,		0.0) 	#Pipe connection
        op.node(913, 	37940.0,	0.0,		0.0) 	#Pipe connection
        op.node(914, 	38060.0,	0.0,		0.0) 	#Pipe connection
        op.node(915, 	43940.0,	0.0,		0.0) 	#Pipe connection
        op.node(916, 	44060.0,	0.0,		0.0) 	#Pipe connection
        op.node(917, 	49940.0,	0.0,		0.0) 	#Pipe connection
        op.node(918, 	50060.0,	0.0,		0.0) 	#Pipe connection
        op.node(919, 	55940.0,	0.0,		0.0) 	#Pipe connection
        op.node(920, 	56060.0,	0.0,		0.0) 	#Pipe connection
        op.node(921, 	61940.0,	0.0,		0.0) 	#Pipe connection
        op.node(922, 	62060.0,	0.0,		0.0) 	#Pipe connection
        op.node(923, 	67940.0,	0.0,		0.0) 	#Pipe connection
        op.node(924, 	68060.0,	0.0,		0.0) 	#Pipe connection
        op.node(925, 	73940.0,	0.0,		0.0) 	#Pipe connection
        op.node(926, 	74060.0,	0.0,		0.0) 	#Pipe connection
        op.node(927, 	79940.0,	0.0,		0.0) 	#Pipe connection
        op.node(928, 	80060.0,	0.0,		0.0) 	#Pipe connection
        op.node(929, 	81900.0,	0.0,		0.0) 	#Pipe connection

        #First cross line (2)
        op.node(930, 	32000.0,	100.0,	    0.0) 	#Pipe connection
        op.node(931, 	32000.0,	5940.0,	    0.0) 	#Pipe connection
        op.node(932, 	32000.0,	6060.0,	    0.0) 	#Pipe connection
        op.node(933, 	32000.0,	11940.0,	0.0) 	#Pipe connection
        op.node(934, 	32000.0,	12060.0,	0.0) 	#Pipe connection
        op.node(935, 	32000.0,	17940.0,	0.0) 	#Pipe connection
        op.node(936, 	32000.0,	18060.0,	0.0) 	#Pipe connection
        op.node(937, 	32000.0,	23940.0,	0.0) 	#Pipe connection
        op.node(938, 	32000.0,	24060.0,	0.0) 	#Pipe connection
        op.node(939, 	32000.0,	29940.0,	0.0) 	#Pipe connection
        op.node(940, 	32000.0,	30060.0,	0.0) 	#Pipe connection
        op.node(941, 	32000.0,	35940.0,	0.0) 	#Pipe connection
        op.node(942,	32000.0,	36060.0,	0.0) 	#Pipe connection
        op.node(943, 	32000.0,	41940.0,	0.0) 	#Pipe connection
        op.node(944, 	32000.0,	42060.0,	0.0) 	#Pipe connection
        op.node(945, 	32000.0,	47940.0,	0.0) 	#Pipe connection
        op.node(946, 	32000.0,	48060.0,	0.0) 	#Pipe connection

        #Second cross line (2)
        op.node(947, 	82000.0,	100.0,	    0.0) 	#Pipe connection
        op.node(948, 	82000.0,	5940.0,	    0.0) 	#Pipe connection
        op.node(949, 	82000.0,	6060.0,	    0.0) 	#Pipe connection
        op.node(950, 	82000.0,	11940.0,	0.0) 	#Pipe connection
        op.node(951, 	82000.0,	12060.0,	0.0) 	#Pipe connection
        op.node(952, 	82000.0,	17940.0,	0.0) 	#Pipe connection
        op.node(953, 	82000.0,	18060.0,	0.0) 	#Pipe connection
        op.node(954, 	82000.0,	23940.0,	0.0) 	#Pipe connection
        op.node(955, 	82000.0,	24060.0,	0.0) 	#Pipe connection
        op.node(956, 	82000.0,	29940.0,	0.0) 	#Pipe connection
        op.node(957, 	82000.0,	30060.0,	0.0) 	#Pipe connection
        op.node(958, 	82000.0,	35940.0,	0.0) 	#Pipe connection
        op.node(959, 	82000.0,	36060.0,	0.0) 	#Pipe connection
        op.node(960, 	82000.0,	41940.0,	0.0) 	#Pipe connection
        op.node(961, 	82000.0,	42060.0,	0.0) 	#Pipe connection
        op.node(962, 	82000.0,	47940.0,	0.0) 	#Pipe connection
        op.node(963, 	82000.0,	48060.0,	0.0) 	#Pipe connection


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
        op.fix(19,	1,	1,	1,	1,	1,	1)
        op.fix(20,	1,	1,	1,	1,	1,	1)
        op.fix(21,	1,	1,	1,	1,	1,	1)
        op.fix(22,	1,	1,	1,	1,	1,	1)
        op.fix(23,	1,	1,	1,	1,	1,	1)
        op.fix(24,	1,	1,	1,	1,	1,	1)
        op.fix(25,	1,	1,	1,	1,	1,	1)
        op.fix(26,	1,	1,	1,	1,	1,	1)
        op.fix(27,	1,	1,	1,	1,	1,	1)
        op.fix(28,	1,	1,	1,	1,	1,	1)
        op.fix(29,	1,	1,	1,	1,	1,	1)
        op.fix(30,	1,	1,	1,	1,	1,	1)
        op.fix(31,	1,	1,	1,	1,	1,	1)
        op.fix(32,	1,	1,	1,	1,	1,	1)
        op.fix(33,	1,	1,	1,	1,	1,	1)
        op.fix(34,	1,	1,	1,	1,	1,	1)
        op.fix(35,	1,	1,	1,	1,	1,	1)
        op.fix(36,	1,	1,	1,	1,	1,	1)
        op.fix(37,	1,	1,	1,	1,	1,	1)
        op.fix(38,	1,	1,	1,	1,	1,	1)
        op.fix(39,	1,	1,	1,	1,	1,	1)
        op.fix(40,	1,	1,	1,	1,	1,	1)
        op.fix(41,	1,	1,	1,	1,	1,	1)
        op.fix(42,	1,	1,	1,	1,	1,	1)
        op.fix(43,	1,	1,	1,	1,	1,	1)
        op.fix(44,	1,	1,	1,	1,	1,	1)
        op.fix(45,	1,	1,	1,	1,	1,	1)
        op.fix(46,	1,	1,	1,	1,	1,	1)
        op.fix(47,	1,	1,	1,	1,	1,	1)
        op.fix(48,	1,	1,	1,	1,	1,	1)
        op.fix(49,	1,	1,	1,	1,	1,	1)
        op.fix(50,	1,	1,	1,	1,	1,	1)
        op.fix(51,	1,	1,	1,	1,	1,	1)
        op.fix(52,	1,	1,	1,	1,	1,	1)
        op.fix(53,	1,	1,	1,	1,	1,	1)
        op.fix(54,	1,	1,	1,	1,	1,	1)
        op.fix(55,	1,	1,	1,	1,	1,	1)
        op.fix(56,	1,	1,	1,	1,	1,	1)
        op.fix(57,	1,	1,	1,	1,	1,	1)
        op.fix(58,	1,	1,	1,	1,	1,	1)
        op.fix(59,	1,	1,	1,	1,	1,	1)
        op.fix(60,	1,	1,	1,	1,	1,	1)
        op.fix(61,	1,	1,	1,	1,	1,	1)

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
        op.element('elasticBeamColumn', 1,	 1001,	101,	A,	E,	G,	J,	Iy,	Iz,	1, '-mass', massu) #pipe element
        op.element('elasticBeamColumn', 2,	 101,	102,	A,	E,	G,	J,	Iy,	Iz,	1, '-mass', massu) #pipe element
        op.element('elasticBeamColumn', 3,	 102,	801,	A,	E,	G,	J,	Iy,	Iz,	1, '-mass', massu) #pipe element
        op.element('elasticBeamColumn', 4,	 901,	802,	A,	E,	G,	J,	Iy,	Iz,	1, '-mass', massu) #pipe element
        op.element('elasticBeamColumn', 5,	 902,	103,	A,	E,	G,	J,	Iy,	Iz,	1, '-mass', massu) #pipe element
        op.element('elasticBeamColumn', 6,	 103,	104,	A,	E,	G,	J,	Iy,	Iz,	1, '-mass', massu) #pipe element
        op.element('elasticBeamColumn', 7,	 104,	803,	A,	E,	G,	J,	Iy,	Iz,	1, '-mass', massu) #pipe element
        op.element('elasticBeamColumn', 8,	 903,	804,	A,	E,	G,	J,	Iy,	Iz,	1, '-mass', massu) #pipe element
        op.element('elasticBeamColumn', 9,	 904,	105,	A,	E,	G,	J,	Iy,	Iz,	1, '-mass', massu) #pipe element
        op.element('elasticBeamColumn', 10,	 105,	106,	A,	E,	G,	J,	Iy,	Iz,	1, '-mass', massu) #pipe element
        op.element('elasticBeamColumn', 11,	 106,	805,	A,	E,	G,	J,	Iy,	Iz,	1, '-mass', massu) #pipe element
        op.element('elasticBeamColumn', 12,	 905,	806,	A,	E,	G,	J,	Iy,	Iz,	1, '-mass', massu) #pipe element
        op.element('elasticBeamColumn', 13,	 906,	107,	A,	E,	G,	J,	Iy,	Iz,	1, '-mass', massu) #pipe element
        op.element('elasticBeamColumn', 14,	 107,	108,	A,	E,	G,	J,	Iy,	Iz,	1, '-mass', massu) #pipe element
        op.element('elasticBeamColumn', 15,	 108,	807,	A,	E,	G,	J,	Iy,	Iz,	1, '-mass', massu) #pipe element
        op.element('elasticBeamColumn', 16,	 907,	808,	A,	E,	G,	J,	Iy,	Iz,	1, '-mass', massu) #pipe element
        op.element('elasticBeamColumn', 17,	 908,	109,	A,	E,	G,	J,	Iy,	Iz,	1, '-mass', massu) #pipe element
        op.element('elasticBeamColumn', 18,	 109,	110,	A,	E,	G,	J,	Iy,	Iz,	1, '-mass', massu) #pipe element
        op.element('elasticBeamColumn', 19,	 110,	809,	A,	E,	G,	J,	Iy,	Iz,	1, '-mass', massu) #pipe element
        op.element('elasticBeamColumn', 20,	 909,	810,	A,	E,	G,	J,	Iy,	Iz,	1, '-mass', massu) #pipe element
        op.element('elasticBeamColumn', 21,	 910,	111,	A,	E,	G,	J,	Iy,	Iz,	1, '-mass', massu) #pipe element
        op.element('elasticBeamColumn', 22,	 111,	811, 	A,	E,	G,	J,	Iy,	Iz,	1, '-mass', massu) #pipe element
        op.element('elasticBeamColumn', 23,	 911,	1002, 	A,	E,	G,	J,	Iy,	Iz,	1, '-mass', massu) #pipe element
        op.element('elasticBeamColumn', 24,	 1002,	812, 	A,	E,	G,	J,	Iy,	Iz,	1, '-mass', massu) #pipe element
        op.element('elasticBeamColumn', 25,	 912, 	112, 	A,	E,	G,	J,	Iy,	Iz,	1, '-mass', massu) #pipe element
        op.element('elasticBeamColumn', 26,	 112,	113,	A,	E,	G,	J,	Iy,	Iz,	1, '-mass', massu) #pipe element
        op.element('elasticBeamColumn', 27,	 113,	813, 	A,	E,	G,	J,	Iy,	Iz,	1, '-mass', massu) #pipe element
        op.element('elasticBeamColumn', 28,	 913,	814, 	A,	E,	G,	J,	Iy,	Iz,	1, '-mass', massu) #pipe element
        op.element('elasticBeamColumn', 29,	 914,	114, 	A,	E,	G,	J,	Iy,	Iz,	1, '-mass', massu) #pipe element
        op.element('elasticBeamColumn', 30,	 114,	115,	A,	E,	G,	J,	Iy,	Iz,	1, '-mass', massu) #pipe element
        op.element('elasticBeamColumn', 31,	 115,	815,	A,	E,	G,	J,	Iy,	Iz,	1, '-mass', massu) #pipe element
        op.element('elasticBeamColumn', 32,	 915,	816,	A,	E,	G,	J,	Iy,	Iz,	1, '-mass', massu) #pipe element
        op.element('elasticBeamColumn', 33,	 916,	116,	A,	E,	G,	J,	Iy,	Iz,	1, '-mass', massu) #pipe element
        op.element('elasticBeamColumn', 34,	 116,	117,	A,	E,	G,	J,	Iy,	Iz,	1, '-mass', massu) #pipe element
        op.element('elasticBeamColumn', 35,	 117,	817,	A,	E,	G,	J,	Iy,	Iz,	1, '-mass', massu) #pipe element
        op.element('elasticBeamColumn', 36,	 917,	818,	A,	E,	G,	J,	Iy,	Iz,	1, '-mass', massu) #pipe element
        op.element('elasticBeamColumn', 37,	 918,	118,	A,	E,	G,	J,	Iy,	Iz,	1, '-mass', massu) #pipe element
        op.element('elasticBeamColumn', 38,	 118,	119,	A,	E,	G,	J,	Iy,	Iz,	1, '-mass', massu) #pipe element
        op.element('elasticBeamColumn', 39,	 119,	819,	A,	E,	G,	J,	Iy,	Iz,	1, '-mass', massu) #pipe element
        op.element('elasticBeamColumn', 40,	 919,	820,	A,	E,	G,	J,	Iy,	Iz,	1, '-mass', massu) #pipe element
        op.element('elasticBeamColumn', 41,	 920,	120,	A,	E,	G,	J,	Iy,	Iz,	1, '-mass', massu) #pipe element
        op.element('elasticBeamColumn', 42,	 120,	121,	A,	E,	G,	J,	Iy,	Iz,	1, '-mass', massu) #pipe element
        op.element('elasticBeamColumn', 43,	 121,	821,	A,	E,	G,	J,	Iy,	Iz,	1, '-mass', massu) #pipe element
        op.element('elasticBeamColumn', 44,	 921,	822,	A,	E,	G,	J,	Iy,	Iz,	1, '-mass', massu) #pipe element
        op.element('elasticBeamColumn', 45,	 922,	122,	A,	E,	G,	J,	Iy,	Iz,	1, '-mass', massu) #pipe element
        op.element('elasticBeamColumn', 46,	 122,	123,	A,	E,	G,	J,	Iy,	Iz,	1, '-mass', massu) #pipe element
        op.element('elasticBeamColumn', 47,	 123,	823,	A,	E,	G,	J,	Iy,	Iz,	1, '-mass', massu) #pipe element
        op.element('elasticBeamColumn', 48,	 923,	824,	A,	E,	G,	J,	Iy,	Iz,	1, '-mass', massu) #pipe element
        op.element('elasticBeamColumn', 49,	 924,	124,	A,	E,	G,	J,	Iy,	Iz,	1, '-mass', massu) #pipe element
        op.element('elasticBeamColumn', 50,	 124,	125,	A,	E,	G,	J,	Iy,	Iz,	1, '-mass', massu) #pipe element
        op.element('elasticBeamColumn', 51,	 125,	825,	A,	E,	G,	J,	Iy,	Iz,	1, '-mass', massu) #pipe element
        op.element('elasticBeamColumn', 52,	 925,	826,	A,	E,	G,	J,	Iy,	Iz,	1, '-mass', massu) #pipe element
        op.element('elasticBeamColumn', 53,	 926,	126,	A,	E,	G,	J,	Iy,	Iz,	1, '-mass', massu) #pipe element
        op.element('elasticBeamColumn', 54,	 126,	127,	A,	E,	G,	J,	Iy,	Iz,	1, '-mass', massu) #pipe element
        op.element('elasticBeamColumn', 55,	 127,	827,	A,	E,	G,	J,	Iy,	Iz,	1, '-mass', massu) #pipe element
        op.element('elasticBeamColumn', 56,	 927,	828,	A,	E,	G,	J,	Iy,	Iz,	1, '-mass', massu) #pipe element
        op.element('elasticBeamColumn', 57,	 928,	829,	A,	E,	G,	J,	Iy,	Iz,	1, '-mass', massu) #pipe element
        op.element('elasticBeamColumn', 58,	 929,	1003,	A,	E,	G,	J,	Iy,	Iz,	1, '-mass', massu) #pipe element

        #Second cross line
        op.element('elasticBeamColumn', 59,	 1003,	847, 	A,	E,	G,	J,	Iy,	Iz,	1, '-mass', massu) #pipe element
        op.element('elasticBeamColumn', 60,	 947, 	128, 	A,	E,	G,	J,	Iy,	Iz,	1, '-mass', massu) #pipe element
        op.element('elasticBeamColumn', 61,	 128,	129, 	A,	E,	G,	J,	Iy,	Iz,	1, '-mass', massu) #pipe element
        op.element('elasticBeamColumn', 62,	 129,	848,	A,	E,	G,	J,	Iy,	Iz,	1, '-mass', massu) #pipe element
        op.element('elasticBeamColumn', 63,	 948,	849,	A,	E,	G,	J,	Iy,	Iz,	1, '-mass', massu) #pipe element
        op.element('elasticBeamColumn', 64,	 949,	130,	A,	E,	G,	J,	Iy,	Iz,	1, '-mass', massu) #pipe element
        op.element('elasticBeamColumn', 65,	 130,	131, 	A,	E,	G,	J,	Iy,	Iz,	1, '-mass', massu) #pipe element
        op.element('elasticBeamColumn', 66,	 131,	850,	A,	E,	G,	J,	Iy,	Iz,	1, '-mass', massu) #pipe element
        op.element('elasticBeamColumn', 67,	 950,	851,	A,	E,	G,	J,	Iy,	Iz,	1, '-mass', massu) #pipe element
        op.element('elasticBeamColumn', 68,	 951,	132,	A,	E,	G,	J,	Iy,	Iz,	1, '-mass', massu) #pipe element
        op.element('elasticBeamColumn', 69,	 132,	133,	A,	E,	G,	J,	Iy,	Iz,	1, '-mass', massu) #pipe element
        op.element('elasticBeamColumn', 70,	 133,	852,	A,	E,	G,	J,	Iy,	Iz,	1, '-mass', massu) #pipe element
        op.element('elasticBeamColumn', 71,	 952,	853,	A,	E,	G,	J,	Iy,	Iz,	1, '-mass', massu) #pipe element
        op.element('elasticBeamColumn', 72,	 953,	134,	A,	E,	G,	J,	Iy,	Iz,	1, '-mass', massu) #pipe element
        op.element('elasticBeamColumn', 73,	 134,	135,	A,	E,	G,	J,	Iy,	Iz,	1, '-mass', massu) #pipe element
        op.element('elasticBeamColumn', 74,	 135,	854,	A,	E,	G,	J,	Iy,	Iz,	1, '-mass', massu) #pipe element
        op.element('elasticBeamColumn', 75,	 954,	855,	A,	E,	G,	J,	Iy,	Iz,	1, '-mass', massu) #pipe element
        op.element('elasticBeamColumn', 76,	 955,	136,	A,	E,	G,	J,	Iy,	Iz,	1, '-mass', massu) #pipe element
        op.element('elasticBeamColumn', 77,	 136,	137,	A,	E,	G,	J,	Iy,	Iz,	1, '-mass', massu) #pipe element
        op.element('elasticBeamColumn', 78,	 137,	856,	A,	E,	G,	J,	Iy,	Iz,	1, '-mass', massu) #pipe element
        op.element('elasticBeamColumn', 79,	 956,	857,	A,	E,	G,	J,	Iy,	Iz,	1, '-mass', massu) #pipe element
        op.element('elasticBeamColumn', 80,	 957,	138,	A,	E,	G,	J,	Iy,	Iz,	1, '-mass', massu) #pipe element
        op.element('elasticBeamColumn', 81,	 138,	139,	A,	E,	G,	J,	Iy,	Iz,	1, '-mass', massu) #pipe element
        op.element('elasticBeamColumn', 82,	 139,	858,	A,	E,	G,	J,	Iy,	Iz,	1, '-mass', massu) #pipe element
        op.element('elasticBeamColumn', 83,	 958,	859,	A,	E,	G,	J,	Iy,	Iz,	1, '-mass', massu) #pipe element
        op.element('elasticBeamColumn', 84,	 959,	140,	A,	E,	G,	J,	Iy,	Iz,	1, '-mass', massu) #pipe element
        op.element('elasticBeamColumn', 85,	 140,	141,	A,	E,	G,	J,	Iy,	Iz,	1, '-mass', massu) #pipe element
        op.element('elasticBeamColumn', 86,	 141,	860,	A,	E,	G,	J,	Iy,	Iz,	1, '-mass', massu) #pipe element
        op.element('elasticBeamColumn', 87,	 960,	861,	A,	E,	G,	J,	Iy,	Iz,	1, '-mass', massu) #pipe element
        op.element('elasticBeamColumn', 88,	 961,	142,	A,	E,	G,	J,	Iy,	Iz,	1, '-mass', massu) #pipe element
        op.element('elasticBeamColumn', 89,	 142,	143,	A,	E,	G,	J,	Iy,	Iz,	1, '-mass', massu) #pipe element
        op.element('elasticBeamColumn', 90,	 143,	862,	A,	E,	G,	J,	Iy,	Iz,	1, '-mass', massu) #pipe element
        op.element('elasticBeamColumn', 91,	 962,	863,	A,	E,	G,	J,	Iy,	Iz,	1, '-mass', massu) #pipe element
        op.element('elasticBeamColumn', 92,	 963,	144,	A,	E,	G,	J,	Iy,	Iz,	1, '-mass', massu) #pipe element
        op.element('elasticBeamColumn', 93,	 144,	1004,	A,	E,	G,	J,	Iy,	Iz,	1, '-mass', massu) #pipe element

        #First cross line
        op.element('elasticBeamColumn', 94,	 1002,	830, 	A,	E,	G,	J,	Iy,	Iz,	1, '-mass', massu) #pipe element
        op.element('elasticBeamColumn', 95,	 930, 	145, 	A,	E,	G,	J,	Iy,	Iz,	1, '-mass', massu) #pipe element
        op.element('elasticBeamColumn', 96,	 145,	146, 	A,	E,	G,	J,	Iy,	Iz,	1, '-mass', massu) #pipe element
        op.element('elasticBeamColumn', 97,	 146,	831,	A,	E,	G,	J,	Iy,	Iz,	1, '-mass', massu) #pipe element
        op.element('elasticBeamColumn', 98,	 931,	832,	A,	E,	G,	J,	Iy,	Iz,	1, '-mass', massu) #pipe element
        op.element('elasticBeamColumn', 99,	 932,	147,	A,	E,	G,	J,	Iy,	Iz,	1, '-mass', massu) #pipe element
        op.element('elasticBeamColumn', 100, 147,	148,	A,	E,	G,	J,	Iy,	Iz,	1, '-mass', massu) #pipe element
        op.element('elasticBeamColumn', 101, 148,	833, 	A,	E,	G,	J,	Iy,	Iz,	1, '-mass', massu) #pipe element
        op.element('elasticBeamColumn', 102, 933,	834, 	A,	E,	G,	J,	Iy,	Iz,	1, '-mass', massu) #pipe element
        op.element('elasticBeamColumn', 103, 934,	149, 	A,	E,	G,	J,	Iy,	Iz,	1, '-mass', massu) #pipe element
        op.element('elasticBeamColumn', 104, 149,	150,	A,	E,	G,	J,	Iy,	Iz,	1, '-mass', massu) #pipe element
        op.element('elasticBeamColumn', 105, 150,	835,	A,	E,	G,	J,	Iy,	Iz,	1, '-mass', massu) #pipe element
        op.element('elasticBeamColumn', 106, 935,	836,	A,	E,	G,	J,	Iy,	Iz,	1, '-mass', massu) #pipe element
        op.element('elasticBeamColumn', 107, 936,	151,	A,	E,	G,	J,	Iy,	Iz,	1, '-mass', massu) #pipe element
        op.element('elasticBeamColumn', 108, 151,	152,	A,	E,	G,	J,	Iy,	Iz,	1, '-mass', massu) #pipe element
        op.element('elasticBeamColumn', 109, 152,	837,	A,	E,	G,	J,	Iy,	Iz,	1, '-mass', massu) #pipe element
        op.element('elasticBeamColumn', 110, 937,	838,	A,	E,	G,	J,	Iy,	Iz,	1, '-mass', massu) #pipe element
        op.element('elasticBeamColumn', 111, 938,	153,	A,	E,	G,	J,	Iy,	Iz,	1, '-mass', massu) #pipe element
        op.element('elasticBeamColumn', 112, 153,	154,	A,	E,	G,	J,	Iy,	Iz,	1, '-mass', massu) #pipe element
        op.element('elasticBeamColumn', 113, 154,	839,	A,	E,	G,	J,	Iy,	Iz,	1, '-mass', massu) #pipe element
        op.element('elasticBeamColumn', 114, 939,	840,	A,	E,	G,	J,	Iy,	Iz,	1, '-mass', massu) #pipe element
        op.element('elasticBeamColumn', 115, 940,	155,	A,	E,	G,	J,	Iy,	Iz,	1, '-mass', massu) #pipe element
        op.element('elasticBeamColumn', 116, 155,	156,	A,	E,	G,	J,	Iy,	Iz,	1, '-mass', massu) #pipe element
        op.element('elasticBeamColumn', 117, 156,	841,	A,	E,	G,	J,	Iy,	Iz,	1, '-mass', massu) #pipe element
        op.element('elasticBeamColumn', 118, 941,	842,	A,	E,	G,	J,	Iy,	Iz,	1, '-mass', massu) #pipe element
        op.element('elasticBeamColumn', 119, 942,	157,	A,	E,	G,	J,	Iy,	Iz,	1, '-mass', massu) #pipe element
        op.element('elasticBeamColumn', 120, 157,	158,	A,	E,	G,	J,	Iy,	Iz,	1, '-mass', massu) #pipe element
        op.element('elasticBeamColumn', 121, 158,	843,	A,	E,	G,	J,	Iy,	Iz,	1, '-mass', massu) #pipe element
        op.element('elasticBeamColumn', 122, 943,	844,	A,	E,	G,	J,	Iy,	Iz,	1, '-mass', massu) #pipe element
        op.element('elasticBeamColumn', 123, 944,	159,	A,	E,	G,	J,	Iy,	Iz,	1, '-mass', massu) #pipe element
        op.element('elasticBeamColumn', 124, 159,	160,	A,	E,	G,	J,	Iy,	Iz,	1, '-mass', massu) #pipe element
        op.element('elasticBeamColumn', 125, 160,	845,	A,	E,	G,	J,	Iy,	Iz,	1, '-mass', massu) #pipe element
        op.element('elasticBeamColumn', 126, 945,	846,	A,	E,	G,	J,	Iy,	Iz,	1, '-mass', massu) #pipe element
        op.element('elasticBeamColumn', 127, 946,	161,	A,	E,	G,	J,	Iy,	Iz,	1, '-mass', massu) #pipe element
        op.element('elasticBeamColumn', 128, 161,	1005,	A,	E,	G,	J,	Iy,	Iz,	1, '-mass', massu) #pipe element

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
        op.rigidLink('beam',	19,	219)	#rigid link
        op.rigidLink('beam',	20,	220)	#rigid link
        op.rigidLink('beam',	21,	221)	#rigid link
        op.rigidLink('beam',	22,	222)	#rigid link
        op.rigidLink('beam',	23,	223)	#rigid link
        op.rigidLink('beam',	24,	224)	#rigid link
        op.rigidLink('beam',	25,	225)	#rigid link
        op.rigidLink('beam',	26,	226)	#rigid link
        op.rigidLink('beam',	27,	227)	#rigid link
        op.rigidLink('beam',	28,	228)	#rigid link
        op.rigidLink('beam',	29,	229)	#rigid link
        op.rigidLink('beam',	30,	230)	#rigid link
        op.rigidLink('beam',	31,	231)	#rigid link
        op.rigidLink('beam',	32,	232)	#rigid link
        op.rigidLink('beam',	33,	233)	#rigid link
        op.rigidLink('beam',	34,	234)	#rigid link
        op.rigidLink('beam',	35,	235)	#rigid link
        op.rigidLink('beam',	36,	236)	#rigid link
        op.rigidLink('beam',	37,	237)	#rigid link
        op.rigidLink('beam',	38,	238)	#rigid link
        op.rigidLink('beam',	39,	239)	#rigid link
        op.rigidLink('beam',	40,	240)	#rigid link
        op.rigidLink('beam',	41,	241)	#rigid link
        op.rigidLink('beam',	42,	242)	#rigid link
        op.rigidLink('beam',	43,	243)	#rigid link
        op.rigidLink('beam',	44,	244)	#rigid link
        op.rigidLink('beam',	45,	245)	#rigid link
        op.rigidLink('beam',	46,	246)	#rigid link
        op.rigidLink('beam',	47,	247)	#rigid link
        op.rigidLink('beam',	48,	248)	#rigid link
        op.rigidLink('beam',	49,	249)	#rigid link
        op.rigidLink('beam',	50,	250)	#rigid link
        op.rigidLink('beam',	51,	251)	#rigid link
        op.rigidLink('beam',	52,	252)	#rigid link
        op.rigidLink('beam',	53,	253)	#rigid link
        op.rigidLink('beam',	54,	254)	#rigid link
        op.rigidLink('beam',	55,	255)	#rigid link
        op.rigidLink('beam',	56,	256)	#rigid link
        op.rigidLink('beam',	57,	257)	#rigid link
        op.rigidLink('beam',	58,	258)	#rigid link
        op.rigidLink('beam',	59,	259)	#rigid link
        op.rigidLink('beam',	60,	260)	#rigid link
        op.rigidLink('beam',	61,	261)	#rigid link

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
        op.rigidLink('beam',	319, 119)	#rigid link
        op.rigidLink('beam',	320, 120)	#rigid link
        op.rigidLink('beam',	321, 121)	#rigid link
        op.rigidLink('beam',	322, 122)	#rigid link
        op.rigidLink('beam',	323, 123)	#rigid link
        op.rigidLink('beam',	324, 124)	#rigid link
        op.rigidLink('beam',	325, 125)	#rigid link
        op.rigidLink('beam',	326, 126)	#rigid link
        op.rigidLink('beam',	327, 127)	#rigid link
        op.rigidLink('beam',	328, 128)	#rigid link
        op.rigidLink('beam',	329, 129)	#rigid link
        op.rigidLink('beam',	330, 130)	#rigid link
        op.rigidLink('beam',	331, 131)	#rigid link
        op.rigidLink('beam',	332, 132)	#rigid link
        op.rigidLink('beam',	333, 133)	#rigid link
        op.rigidLink('beam',	334, 134)	#rigid link
        op.rigidLink('beam',	335, 135)	#rigid link
        op.rigidLink('beam',	336, 136)	#rigid link
        op.rigidLink('beam',	337, 137)	#rigid link
        op.rigidLink('beam',	338, 138)	#rigid link
        op.rigidLink('beam',	339, 139)	#rigid link
        op.rigidLink('beam',	340, 140)	#rigid link
        op.rigidLink('beam',	341, 141)	#rigid link
        op.rigidLink('beam',	342, 142)	#rigid link
        op.rigidLink('beam',	343, 143)	#rigid link
        op.rigidLink('beam',	344, 144)	#rigid link
        op.rigidLink('beam',	345, 145)	#rigid link
        op.rigidLink('beam',	346, 146)	#rigid link
        op.rigidLink('beam',	347, 147)	#rigid link
        op.rigidLink('beam',	348, 148)	#rigid link
        op.rigidLink('beam',	349, 149)	#rigid link
        op.rigidLink('beam',	350, 150)	#rigid link
        op.rigidLink('beam',	351, 151)	#rigid link
        op.rigidLink('beam',	352, 152)	#rigid link
        op.rigidLink('beam',	353, 153)	#rigid link
        op.rigidLink('beam',	354, 154)	#rigid link
        op.rigidLink('beam',	355, 155)	#rigid link
        op.rigidLink('beam',	356, 156)	#rigid link
        op.rigidLink('beam',	357, 157)	#rigid link
        op.rigidLink('beam',	358, 158)	#rigid link
        op.rigidLink('beam',	359, 159)	#rigid link
        op.rigidLink('beam',	360, 160)	#rigid link
        op.rigidLink('beam',	361, 161)	#rigid link

        #5.2: Braces behaviour
            
        op.element('zeroLength', 	501,		201,		301,  '-mat',	1, 2, 4, 4, 4, 4,	'-dir', 	1, 2, 3, 4, 5, 6) #Typology of subassembly
        op.element('zeroLength', 	502,		202,		302,  '-mat',	3, 3, 4, 4, 4, 4,	'-dir', 	1, 2, 3, 4, 5, 6) #Typology of subassembly 
        op.element('zeroLength', 	503,		203,		303,  '-mat',	3, 3, 4, 4, 4, 4,	'-dir', 	1, 2, 3, 4, 5, 6) #Typology of subassembly
        op.element('zeroLength', 	504,		204,		304,  '-mat',	3, 2, 4, 4, 4, 4,	'-dir', 	1, 2, 3, 4, 5, 6) #Typology of subassembly
        op.element('zeroLength', 	505,		205,		305,  '-mat',	1, 3, 4, 4, 4, 4,	'-dir', 	1, 2, 3, 4, 5, 6) #Typology of subassembly 
        op.element('zeroLength', 	506,		206,		306,  '-mat',	3, 3, 4, 4, 4, 4,	'-dir', 	1, 2, 3, 4, 5, 6) #Typology of subassembly
        op.element('zeroLength', 	507,		207,		307,  '-mat',	3, 3, 4, 4, 4, 4,	'-dir', 	1, 2, 3, 4, 5, 6) #Typology of subassembly
        op.element('zeroLength', 	508,		208,		308,  '-mat',	1, 2, 4, 4, 4, 4,	'-dir', 	1, 2, 3, 4, 5, 6) #Typology of subassembly
        op.element('zeroLength', 	509,		209,		309,  '-mat',	3, 3, 4, 4, 4, 4,	'-dir', 	1, 2, 3, 4, 5, 6) #Typology of subassembly
        op.element('zeroLength', 	510,		210,		310,  '-mat',	3, 3, 4, 4, 4, 4,	'-dir', 	1, 2, 3, 4, 5, 6) #Typology of subassembly
        op.element('zeroLength', 	511,		211,		311,  '-mat',	3, 3, 4, 4, 4, 4,	'-dir', 	1, 2, 3, 4, 5, 6) #Typology of subassembly
        op.element('zeroLength', 	512,		212,		312,  '-mat',	1, 2, 4, 4, 4, 4,	'-dir', 	1, 2, 3, 4, 5, 6) #Typology of subassembly
        op.element('zeroLength', 	513,		213,		313,  '-mat',	3, 3, 4, 4, 4, 4,	'-dir', 	1, 2, 3, 4, 5, 6) #Typology of subassembly
        op.element('zeroLength', 	514,		214,		314,  '-mat',	3, 3, 4, 4, 4, 4,	'-dir', 	1, 2, 3, 4, 5, 6) #Typology of subassembly
        op.element('zeroLength', 	515,		215,		315,  '-mat',	3, 2, 4, 4, 4, 4,	'-dir', 	1, 2, 3, 4, 5, 6) #Typology of subassembly
        op.element('zeroLength', 	516,		216,		316,  '-mat',	1, 3, 4, 4, 4, 4,	'-dir', 	1, 2, 3, 4, 5, 6) #Typology of subassembly
        op.element('zeroLength', 	517,		217,		317,  '-mat',	3, 3, 4, 4, 4, 4,	'-dir', 	1, 2, 3, 4, 5, 6) #Typology of subassembly
        op.element('zeroLength', 	518,		218,		318,  '-mat',	3, 3, 4, 4, 4, 4,	'-dir', 	1, 2, 3, 4, 5, 6) #Typology of subassembly
        op.element('zeroLength', 	519,		219,		319,  '-mat',	3, 2, 4, 4, 4, 4,	'-dir', 	1, 2, 3, 4, 5, 6) #Typology of subassembly
        op.element('zeroLength', 	520,		220,		320,  '-mat',	1, 3, 4, 4, 4, 4,	'-dir', 	1, 2, 3, 4, 5, 6) #Typology of subassembly
        op.element('zeroLength', 	521,		221,		321,  '-mat',	3, 3, 4, 4, 4, 4,	'-dir', 	1, 2, 3, 4, 5, 6) #Typology of subassembly
        op.element('zeroLength', 	522,		222,		322,  '-mat',	3, 3, 4, 4, 4, 4,	'-dir', 	1, 2, 3, 4, 5, 6) #Typology of subassembly
        op.element('zeroLength', 	523,		223,		323,  '-mat',	1, 2, 4, 4, 4, 4,	'-dir', 	1, 2, 3, 4, 5, 6) #Typology of subassembly
        op.element('zeroLength', 	524,		224,		324,  '-mat',	3, 3, 4, 4, 4, 4,	'-dir', 	1, 2, 3, 4, 5, 6) #Typology of subassembly
        op.element('zeroLength', 	525,		225,		325,  '-mat',	3, 3, 4, 4, 4, 4,	'-dir', 	1, 2, 3, 4, 5, 6) #Typology of subassembly
        op.element('zeroLength', 	526,		226,		326,  '-mat',	3, 2, 4, 4, 4, 4,	'-dir', 	1, 2, 3, 4, 5, 6) #Typology of subassembly
        op.element('zeroLength', 	527,		227,		327,  '-mat',	1, 3, 4, 4, 4, 4,	'-dir', 	1, 2, 3, 4, 5, 6) #Typology of subassembly

        #First Cross line
        op.element('zeroLength', 	528,		228,		328,  '-mat',	3, 1, 4, 4, 4, 4,	'-dir', 	1, 2, 3, 4, 5, 6) #Typology of subassembly
        op.element('zeroLength', 	529,		229,		329,  '-mat',	2, 3, 4, 4, 4, 4,	'-dir', 	1, 2, 3, 4, 5, 6) #Typology of subassembly
        op.element('zeroLength', 	530,		230,		330,  '-mat',	3, 3, 4, 4, 4, 4,	'-dir', 	1, 2, 3, 4, 5, 6) #Typology of subassembly
        op.element('zeroLength', 	531,		231,		331,  '-mat',	3, 3, 4, 4, 4, 4,	'-dir', 	1, 2, 3, 4, 5, 6) #Typology of subassembly
        op.element('zeroLength', 	532,		232,		332,  '-mat',	2, 1, 4, 4, 4, 4,	'-dir', 	1, 2, 3, 4, 5, 6) #Typology of subassembly
        op.element('zeroLength', 	533,		233,		333,  '-mat',	3, 3, 4, 4, 4, 4,	'-dir', 	1, 2, 3, 4, 5, 6) #Typology of subassembly
        op.element('zeroLength', 	534,		234,		334,  '-mat',	3, 3, 4, 4, 4, 4,	'-dir', 	1, 2, 3, 4, 5, 6) #Typology of subassembly
        op.element('zeroLength', 	535,		235,		335,  '-mat',	3, 3, 4, 4, 4, 4,	'-dir', 	1, 2, 3, 4, 5, 6) #Typology of subassembly
        op.element('zeroLength', 	536,		236,		336,  '-mat',	2, 1, 4, 4, 4, 4,	'-dir', 	1, 2, 3, 4, 5, 6) #Typology of subassembly
        op.element('zeroLength', 	537,		237,		337,  '-mat',	3, 3, 4, 4, 4, 4,	'-dir', 	1, 2, 3, 4, 5, 6) #Typology of subassembly
        op.element('zeroLength', 	538,		238,		338,  '-mat',	3, 3, 4, 4, 4, 4,	'-dir', 	1, 2, 3, 4, 5, 6) #Typology of subassembly
        op.element('zeroLength', 	539,		239,		339,  '-mat',	3, 3, 4, 4, 4, 4,	'-dir', 	1, 2, 3, 4, 5, 6) #Typology of subassembly
        op.element('zeroLength', 	540,		240,		340,  '-mat',	2, 1, 4, 4, 4, 4,	'-dir', 	1, 2, 3, 4, 5, 6) #Typology of subassembly
        op.element('zeroLength', 	541,		241,		341,  '-mat',	3, 3, 4, 4, 4, 4,	'-dir', 	1, 2, 3, 4, 5, 6) #Typology of subassembly
        op.element('zeroLength', 	542,		242,		342,  '-mat',	3, 3, 4, 4, 4, 4,	'-dir', 	1, 2, 3, 4, 5, 6) #Typology of subassembly
        op.element('zeroLength', 	543,		243,		343,  '-mat',	2, 3, 4, 4, 4, 4,	'-dir', 	1, 2, 3, 4, 5, 6) #Typology of subassembly
        op.element('zeroLength', 	544,		244,		344,  '-mat',	3, 1, 4, 4, 4, 4,	'-dir', 	1, 2, 3, 4, 5, 6) #Typology of subassembly

        #Second Cross line
        op.element('zeroLength', 	545,		245,		345,  '-mat',	3, 1, 4, 4, 4, 4,	'-dir', 	1, 2, 3, 4, 5, 6) #Typology of subassembly
        op.element('zeroLength', 	546,		246,		346,  '-mat',	2, 3, 4, 4, 4, 4,	'-dir', 	1, 2, 3, 4, 5, 6) #Typology of subassembly 
        op.element('zeroLength', 	547,		247,		347,  '-mat',	3, 3, 4, 4, 4, 4,	'-dir', 	1, 2, 3, 4, 5, 6) #Typology of subassembly
        op.element('zeroLength', 	548,		248,		348,  '-mat',	3, 3, 4, 4, 4, 4,	'-dir', 	1, 2, 3, 4, 5, 6) #Typology of subassembly
        op.element('zeroLength', 	549,		249,		349,  '-mat',	2, 1, 4, 4, 4, 4,	'-dir', 	1, 2, 3, 4, 5, 6) #Typology of subassembly
        op.element('zeroLength', 	550,		250,		350,  '-mat',	3, 3, 4, 4, 4, 4,	'-dir', 	1, 2, 3, 4, 5, 6) #Typology of subassembly 
        op.element('zeroLength', 	551,		251,		351,  '-mat',	3, 3, 4, 4, 4, 4,	'-dir', 	1, 2, 3, 4, 5, 6) #Typology of subassembly
        op.element('zeroLength', 	552,		252,		352,  '-mat',	3, 3, 4, 4, 4, 4,	'-dir', 	1, 2, 3, 4, 5, 6) #Typology of subassembly
        op.element('zeroLength', 	553,		253,		353,  '-mat',	2, 1, 4, 4, 4, 4,	'-dir', 	1, 2, 3, 4, 5, 6) #Typology of subassembly
        op.element('zeroLength', 	554,		254,		354,  '-mat',	3, 3, 4, 4, 4, 4,	'-dir', 	1, 2, 3, 4, 5, 6) #Typology of subassembly
        op.element('zeroLength', 	555,		255,		355,  '-mat',	3, 3, 4, 4, 4, 4,	'-dir', 	1, 2, 3, 4, 5, 6) #Typology of subassembly
        op.element('zeroLength', 	556,		256,		356,  '-mat',	3, 3, 4, 4, 4, 4,	'-dir', 	1, 2, 3, 4, 5, 6) #Typology of subassembly
        op.element('zeroLength', 	557,		257,		357,  '-mat',	2, 1, 4, 4, 4, 4,	'-dir', 	1, 2, 3, 4, 5, 6) #Typology of subassembly
        op.element('zeroLength', 	558,		258,		358,  '-mat',	3, 3, 4, 4, 4, 4,	'-dir', 	1, 2, 3, 4, 5, 6) #Typology of subassembly
        op.element('zeroLength', 	559,		259,		359,  '-mat',	3, 3, 4, 4, 4, 4,	'-dir', 	1, 2, 3, 4, 5, 6) #Typology of subassembly
        op.element('zeroLength', 	560,		260,		360,  '-mat',	2, 3, 4, 4, 4, 4,	'-dir', 	1, 2, 3, 4, 5, 6) #Typology of subassembly
        op.element('zeroLength', 	561,		261,		361,  '-mat',	3, 1, 4, 4, 4, 4,	'-dir', 	1, 2, 3, 4, 5, 6) #Typology of subassembly

        nodesX = [1001, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 1002, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 1003,
                  128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 1004,
                  145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 1005]
                  
        nodesXt = [101,105,108,112,116,120,123,127,129,132,136,140,143,146,149,153,157,160]
        nodesXp = []

        for i in range(len(nodesX)):
            if nodesX[i] not in nodesXt:
                nodesXp.append(nodesX[i])          
                  
                  
        nodesY = [1001, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 1002, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 1003,
                  128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 1004,
                  145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 1005]
                  
        nodesYt = [102,104,108,112,115,119,123,126,128,132,136,140,144,145,149,153,157,161]
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
        op.element('zeroLength',	717,		817,		917,   '-mat', 4, 4, 4, 4, 4, 8, '-dir', 1, 2, 3, 4, 5, 6) #Typology of subassembly
        op.element('zeroLength',	718,		818,		918,   '-mat', 4, 4, 4, 4, 4, 8, '-dir', 1, 2, 3, 4, 5, 6) #Typology of subassembly
        op.element('zeroLength',	719,		819,		919,   '-mat', 4, 4, 4, 4, 4, 8, '-dir', 1, 2, 3, 4, 5, 6) #Typology of subassembly
        op.element('zeroLength',	720,		820,		920,   '-mat', 4, 4, 4, 4, 4, 8, '-dir', 1, 2, 3, 4, 5, 6) #Typology of subassembly
        op.element('zeroLength',	721,		821,		921,   '-mat', 4, 4, 4, 4, 4, 8, '-dir', 1, 2, 3, 4, 5, 6) #Typology of subassembly
        op.element('zeroLength',	722,		822,		922,   '-mat', 4, 4, 4, 4, 4, 8, '-dir', 1, 2, 3, 4, 5, 6) #Typology of subassembly
        op.element('zeroLength',	723,		823,		923,   '-mat', 4, 4, 4, 4, 4, 8, '-dir', 1, 2, 3, 4, 5, 6) #Typology of subassembly
        op.element('zeroLength',	724,		824,		924,   '-mat', 4, 4, 4, 4, 4, 8, '-dir', 1, 2, 3, 4, 5, 6) #Typology of subassembly
        op.element('zeroLength',	725,		825,		925,   '-mat', 4, 4, 4, 4, 4, 8, '-dir', 1, 2, 3, 4, 5, 6) #Typology of subassembly
        op.element('zeroLength',	726,		826,		926,   '-mat', 4, 4, 4, 4, 4, 8, '-dir', 1, 2, 3, 4, 5, 6) #Typology of subassembly
        op.element('zeroLength',	727,		827,		927,   '-mat', 4, 4, 4, 4, 4, 8, '-dir', 1, 2, 3, 4, 5, 6) #Typology of subassembly
        op.element('zeroLength',	728,		828,		928,   '-mat', 4, 4, 4, 4, 4, 8, '-dir', 1, 2, 3, 4, 5, 6) #Typology of subassembly
        op.element('zeroLength',	729,		829,		929,   '-mat', 4, 4, 4, 4, 4, 8, '-dir', 1, 2, 3, 4, 5, 6) #Typology of subassembly

        op.element('zeroLength',	730,		830,		930,   '-mat', 4, 4, 4, 4, 4, 8, '-dir', 1, 2, 3, 4, 5, 6) #Typology of subassembly
        op.element('zeroLength',	731,		831,		931,   '-mat', 4, 4, 4, 4, 4, 8, '-dir', 1, 2, 3, 4, 5, 6) #Typology of subassembly
        op.element('zeroLength',	732,		832,		932,   '-mat', 4, 4, 4, 4, 4, 8, '-dir', 1, 2, 3, 4, 5, 6) #Typology of subassembly
        op.element('zeroLength',	733,		833,		933,   '-mat', 4, 4, 4, 4, 4, 8, '-dir', 1, 2, 3, 4, 5, 6) #Typology of subassembly
        op.element('zeroLength',	734,		834,		934,   '-mat', 4, 4, 4, 4, 4, 8, '-dir', 1, 2, 3, 4, 5, 6) #Typology of subassembly
        op.element('zeroLength',	735,		835,		935,   '-mat', 4, 4, 4, 4, 4, 8, '-dir', 1, 2, 3, 4, 5, 6) #Typology of subassembly
        op.element('zeroLength',	736,		836,		936,   '-mat', 4, 4, 4, 4, 4, 8, '-dir', 1, 2, 3, 4, 5, 6) #Typology of subassembly
        op.element('zeroLength',	737,		837,		937,   '-mat', 4, 4, 4, 4, 4, 8, '-dir', 1, 2, 3, 4, 5, 6) #Typology of subassembly
        op.element('zeroLength',	738,		838,		938,   '-mat', 4, 4, 4, 4, 4, 8, '-dir', 1, 2, 3, 4, 5, 6) #Typology of subassembly
        op.element('zeroLength',	739,		839,		939,   '-mat', 4, 4, 4, 4, 4, 8, '-dir', 1, 2, 3, 4, 5, 6) #Typology of subassembly
        op.element('zeroLength',	740,		840,		940,   '-mat', 4, 4, 4, 4, 4, 8, '-dir', 1, 2, 3, 4, 5, 6) #Typology of subassembly
        op.element('zeroLength',	741,		841,		941,   '-mat', 4, 4, 4, 4, 4, 8, '-dir', 1, 2, 3, 4, 5, 6) #Typology of subassembly
        op.element('zeroLength',	742,		842,		942,   '-mat', 4, 4, 4, 4, 4, 8, '-dir', 1, 2, 3, 4, 5, 6) #Typology of subassembly
        op.element('zeroLength',	743,		843,		943,   '-mat', 4, 4, 4, 4, 4, 8, '-dir', 1, 2, 3, 4, 5, 6) #Typology of subassembly
        op.element('zeroLength',	744,		844,		944,   '-mat', 4, 4, 4, 4, 4, 8, '-dir', 1, 2, 3, 4, 5, 6) #Typology of subassembly
        op.element('zeroLength',	745,		845,		945,   '-mat', 4, 4, 4, 4, 4, 8, '-dir', 1, 2, 3, 4, 5, 6) #Typology of subassembly
        op.element('zeroLength',	746,		846,		946,   '-mat', 4, 4, 4, 4, 4, 8, '-dir', 1, 2, 3, 4, 5, 6) #Typology of subassembly
        op.element('zeroLength',	747,		847,		947,   '-mat', 4, 4, 4, 4, 4, 8, '-dir', 1, 2, 3, 4, 5, 6) #Typology of subassembly
        op.element('zeroLength',	748,		848,		948,   '-mat', 4, 4, 4, 4, 4, 8, '-dir', 1, 2, 3, 4, 5, 6) #Typology of subassembly
        op.element('zeroLength',	749,		849,		949,   '-mat', 4, 4, 4, 4, 4, 8, '-dir', 1, 2, 3, 4, 5, 6) #Typology of subassembly
        op.element('zeroLength',	750,		850,		950,   '-mat', 4, 4, 4, 4, 4, 8, '-dir', 1, 2, 3, 4, 5, 6) #Typology of subassembly
        op.element('zeroLength',	751,		851,		951,   '-mat', 4, 4, 4, 4, 4, 8, '-dir', 1, 2, 3, 4, 5, 6) #Typology of subassembly
        op.element('zeroLength',	752,		852,		952,   '-mat', 4, 4, 4, 4, 4, 8, '-dir', 1, 2, 3, 4, 5, 6) #Typology of subassembly
        op.element('zeroLength',	753,		853,		953,   '-mat', 4, 4, 4, 4, 4, 8, '-dir', 1, 2, 3, 4, 5, 6) #Typology of subassembly
        op.element('zeroLength',	754,		854,		954,   '-mat', 4, 4, 4, 4, 4, 8, '-dir', 1, 2, 3, 4, 5, 6) #Typology of subassembly
        op.element('zeroLength',	755,		855,		955,   '-mat', 4, 4, 4, 4, 4, 8, '-dir', 1, 2, 3, 4, 5, 6) #Typology of subassembly
        op.element('zeroLength',	756,		856,		956,   '-mat', 4, 4, 4, 4, 4, 8, '-dir', 1, 2, 3, 4, 5, 6) #Typology of subassembly
        op.element('zeroLength',	757,		857,		957,   '-mat', 4, 4, 4, 4, 4, 8, '-dir', 1, 2, 3, 4, 5, 6) #Typology of subassembly
        op.element('zeroLength',	758,		858,		958,   '-mat', 4, 4, 4, 4, 4, 8, '-dir', 1, 2, 3, 4, 5, 6) #Typology of subassembly
        op.element('zeroLength',	759,		859,		959,   '-mat', 4, 4, 4, 4, 4, 8, '-dir', 1, 2, 3, 4, 5, 6) #Typology of subassembly
        op.element('zeroLength',	760,		860,		960,   '-mat', 4, 4, 4, 4, 4, 8, '-dir', 1, 2, 3, 4, 5, 6) #Typology of subassembly
        op.element('zeroLength',	761,		861,		961,   '-mat', 4, 4, 4, 4, 4, 8, '-dir', 1, 2, 3, 4, 5, 6) #Typology of subassembly
        op.element('zeroLength',	762,		862,		962,   '-mat', 4, 4, 4, 4, 4, 8, '-dir', 1, 2, 3, 4, 5, 6) #Typology of subassembly
        op.element('zeroLength',	763,		863,		963,   '-mat', 4, 4, 4, 4, 4, 8, '-dir', 1, 2, 3, 4, 5, 6) #Typology of subassembly


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
        op.equalDOF(219, 319,  3, 4, 5, 6)
        op.equalDOF(220, 320,  3, 4, 5, 6)
        op.equalDOF(221, 321,  3, 4, 5, 6)
        op.equalDOF(222, 322,  3, 4, 5, 6)
        op.equalDOF(223, 323,  3, 4, 5, 6)
        op.equalDOF(224, 324,  3, 4, 5, 6)
        op.equalDOF(225, 325,  3, 4, 5, 6)
        op.equalDOF(226, 326,  3, 4, 5, 6)
        op.equalDOF(227, 327,  3, 4, 5, 6)
        op.equalDOF(228, 328,  3, 4, 5, 6)
        op.equalDOF(229, 329,  3, 4, 5, 6)
        op.equalDOF(230, 330,  3, 4, 5, 6)
        op.equalDOF(231, 331,  3, 4, 5, 6)
        op.equalDOF(232, 332,  3, 4, 5, 6)
        op.equalDOF(233, 333,  3, 4, 5, 6)
        op.equalDOF(234, 334,  3, 4, 5, 6)
        op.equalDOF(235, 335,  3, 4, 5, 6)
        op.equalDOF(236, 336,  3, 4, 5, 6)
        op.equalDOF(237, 337,  3, 4, 5, 6)
        op.equalDOF(238, 338,  3, 4, 5, 6)
        op.equalDOF(239, 339,  3, 4, 5, 6)
        op.equalDOF(240, 340,  3, 4, 5, 6)
        op.equalDOF(241, 341,  3, 4, 5, 6)
        op.equalDOF(242, 342,  3, 4, 5, 6)
        op.equalDOF(243, 343,  3, 4, 5, 6)
        op.equalDOF(244, 344,  3, 4, 5, 6)
        op.equalDOF(245, 345,  3, 4, 5, 6)
        op.equalDOF(246, 346,  3, 4, 5, 6)
        op.equalDOF(247, 347,  3, 4, 5, 6)
        op.equalDOF(248, 348,  3, 4, 5, 6)
        op.equalDOF(249, 349,  3, 4, 5, 6)
        op.equalDOF(250, 350,  3, 4, 5, 6)
        op.equalDOF(251, 351,  3, 4, 5, 6)
        op.equalDOF(252, 352,  3, 4, 5, 6)
        op.equalDOF(253, 353,  3, 4, 5, 6)
        op.equalDOF(254, 354,  3, 4, 5, 6)
        op.equalDOF(255, 355,  3, 4, 5, 6)
        op.equalDOF(256, 356,  3, 4, 5, 6)
        op.equalDOF(257, 357,  3, 4, 5, 6)
        op.equalDOF(258, 358,  3, 4, 5, 6)
        op.equalDOF(259, 359,  3, 4, 5, 6)
        op.equalDOF(260, 360,  3, 4, 5, 6)
        op.equalDOF(261, 361,  3, 4, 5, 6)

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
        op.equalDOF(817, 917, 1, 2, 3, 4, 5)
        op.equalDOF(818, 918, 1, 2, 3, 4, 5)
        op.equalDOF(819, 919, 1, 2, 3, 4, 5)
        op.equalDOF(820, 920, 1, 2, 3, 4, 5)
        op.equalDOF(821, 921, 1, 2, 3, 4, 5)
        op.equalDOF(822, 922, 1, 2, 3, 4, 5)
        op.equalDOF(823, 923, 1, 2, 3, 4, 5)
        op.equalDOF(824, 924, 1, 2, 3, 4, 5)
        op.equalDOF(825, 925, 1, 2, 3, 4, 5)
        op.equalDOF(826, 926, 1, 2, 3, 4, 5)
        op.equalDOF(827, 927, 1, 2, 3, 4, 5)
        op.equalDOF(828, 928, 1, 2, 3, 4, 5)
        op.equalDOF(829, 929, 1, 2, 3, 4, 5)

        op.equalDOF(830, 930, 1, 2, 3, 4, 5)
        op.equalDOF(831, 931, 1, 2, 3, 4, 5)
        op.equalDOF(832, 932, 1, 2, 3, 4, 5)
        op.equalDOF(833, 933, 1, 2, 3, 4, 5)
        op.equalDOF(834, 934, 1, 2, 3, 4, 5)
        op.equalDOF(835, 935, 1, 2, 3, 4, 5)
        op.equalDOF(836, 936, 1, 2, 3, 4, 5)
        op.equalDOF(837, 937, 1, 2, 3, 4, 5)
        op.equalDOF(838, 938, 1, 2, 3, 4, 5)
        op.equalDOF(839, 939, 1, 2, 3, 4, 5)
        op.equalDOF(840, 940, 1, 2, 3, 4, 5)
        op.equalDOF(841, 941, 1, 2, 3, 4, 5)
        op.equalDOF(842, 942, 1, 2, 3, 4, 5)
        op.equalDOF(843, 943, 1, 2, 3, 4, 5)
        op.equalDOF(844, 944, 1, 2, 3, 4, 5)
        op.equalDOF(845, 945, 1, 2, 3, 4, 5)
        op.equalDOF(846, 946, 1, 2, 3, 4, 5)
        op.equalDOF(847, 947, 1, 2, 3, 4, 5)
        op.equalDOF(848, 948, 1, 2, 3, 4, 5)
        op.equalDOF(849, 949, 1, 2, 3, 4, 5)
        op.equalDOF(850, 950, 1, 2, 3, 4, 5)
        op.equalDOF(851, 951, 1, 2, 3, 4, 5)
        op.equalDOF(852, 952, 1, 2, 3, 4, 5)
        op.equalDOF(853, 953, 1, 2, 3, 4, 5)
        op.equalDOF(854, 954, 1, 2, 3, 4, 5)
        op.equalDOF(855, 955, 1, 2, 3, 4, 5)
        op.equalDOF(856, 956, 1, 2, 3, 4, 5)
        op.equalDOF(857, 957, 1, 2, 3, 4, 5)
        op.equalDOF(858, 958, 1, 2, 3, 4, 5)
        op.equalDOF(859, 959, 1, 2, 3, 4, 5)
        op.equalDOF(860, 960, 1, 2, 3, 4, 5)
        op.equalDOF(861, 961, 1, 2, 3, 4, 5)
        op.equalDOF(862, 962, 1, 2, 3, 4, 5)
        op.equalDOF(863, 963, 1, 2, 3, 4, 5)
        '''
        # 9th step: Apply of load and gravity with static analysis

        # set l -0.2315; #load per unit length of cpvc piping (N/mm)
        l = -1.183; #load per unit length of steel piping (N/mm)

        op.timeSeries('Constant', 1)
        op.pattern('Plain', 1, 1)

        op.eleLoad('-ele', 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, '-type', '-beamUniform',0.0, l, 0.0)
        op.eleLoad('-ele', 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, '-type', '-beamUniform',0.0, l, 0.0)
        op.eleLoad('-ele', 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, '-type', '-beamUniform',0.0, l, 0.0)
        op.eleLoad('-ele', 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, '-type', '-beamUniform',0.0, l, 0.0)


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
                    op.test('RelativeEnergyIncr',*testParams2)
                    op.algorithm('Newton','-initial')
                    print("Trying Newton with Initial Tangent ..")
                    ok = op.analyze(1,dta/2)
                    op.test('EnergyIncr',*testParams) 
                    op.algorithm('Newton') 
                if(ok != 0):
                    op.algorithm('Broyden',50)
                    op.test('RelativeEnergyIncr',*testParams2)
                    print("Trying Broyden ..")
                    ok = op.analyze(1,dta/2) 
                    op.test('EnergyIncr',*testParams) 
                    op.algorithm('Newton') 
                if(ok != 0):
                    op.algorithm('NewtonLineSearch')
                    op.test('RelativeEnergyIncr',*testParams2)
                    print("Trying NewtonWithLineSearch ..")
                    ok = op.analyze(1,dta/10)
                    op.test('EnergyIncr',*testParams) 
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
