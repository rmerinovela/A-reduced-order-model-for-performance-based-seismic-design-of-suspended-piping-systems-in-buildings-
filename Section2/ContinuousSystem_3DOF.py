import openseespy.opensees as op
import numpy as np
import vfo.vfo as vfo

def build_model(n_elem=10, Lpipe=6000, kT=600, kL=625,
                Dext=127, Dint=113, npipes=1,
                E=210000.0, G=81000.0, rho=7.85e-9,
                n=1, h=10, n_springs=0):

    op.wipe()
    op.model('basic', '-ndm', 3, '-ndf', 6)

    # ------------------------------------------------------------
    # 1. Geometry and mesh
    # ------------------------------------------------------------
    node_tags = []
    x_coords = np.linspace(0, Lpipe, n_elem + 1)

    for i, x in enumerate(x_coords):
        tag = 100 + i
        op.node(tag, x, 0.0, 0.0)
        node_tags.append(tag)

    # ------------------------------------------------------------
    # 2. Lumped mass
    # ------------------------------------------------------------
    A = npipes * np.pi * ((Dext/2)**2 - (Dint/2)**2)
    mass_per_length = rho * A
    m_node = mass_per_length * (Lpipe / n_elem)
    
    Aw = npipes * np.pi * ((Dint/2)**2)
    mass_per_lengthw = rho/7.8 * Aw
    m_nodew = mass_per_lengthw * (Lpipe / n_elem)

    for nd in node_tags:
        #if(nd==node_tags[0]):
            #op.mass(nd, m_node+(rho*A+rho/7.8*Aw)*36000, m_node+(rho*A+rho/7.8*Aw)*36000, 0, 0, 0, 0)
        #else:
        op.mass(nd, m_node+m_nodew, m_node+m_nodew, 0, 0, 0, 0)
        
    #+rho*A*36000
    # ------------------------------------------------------------
    # 3. Boundary nodes (fixed)
    # ------------------------------------------------------------
    op.node(1, 0.0, 0.0, 10.0)
    op.node(2, Lpipe, 0.0, 10.0)
    op.fix(1, 1,1,1,1,1,1)
    op.fix(2, 1,1,1,1,1,1)

    # ------------------------------------------------------------
    # 4. End springs 
    # ------------------------------------------------------------
    op.node(201, 0.0,   0.0, 5.0)
    op.node(202, Lpipe, 0.0, 5.0)
    op.node(301, 0.0,   0.0, 5.0)
    op.node(302, Lpipe, 0.0, 5.0)

    op.uniaxialMaterial('Elastic', 1, kL)
    op.uniaxialMaterial('Elastic', 2, kL)
    op.uniaxialMaterial('Elastic', 3, kT)
    op.uniaxialMaterial('Elastic', 4, 1e12)

    op.rigidLink('beam', 1, 201)
    op.rigidLink('beam', 2, 202)
    op.rigidLink('beam', 301, node_tags[0])
    op.rigidLink('beam', 302, node_tags[-1])

    op.element('zeroLength', 501, 201, 301,
               '-mat', 1,2,4,4,4,4, '-dir', 1,2,3,4,5,6)
    op.element('zeroLength', 502, 202, 302,
               '-mat', 1,3,4,4,4,4, '-dir', 1,2,3,4,5,6)

    # ------------------------------------------------------------
    # 4b. Internal transversal springs
    # ------------------------------------------------------------
    if n_springs > 0:
        x_spr = np.linspace(0, Lpipe, n_springs + 2)[1:-1]

        for i, xs in enumerate(x_spr, start=1):
            idx = int(np.argmin(np.abs(x_coords - xs)))
            beam_node = node_tags[idx]

            top = 10000 + i
            bot = 11000 + i

            op.node(top, x_coords[idx], 0.0, 10.0)
            op.fix(top, 1,1,1,1,1,1)

            op.node(bot, x_coords[idx], 0.0, 5.0)
            op.rigidLink('beam', beam_node, bot)

            op.element('zeroLength', 12000 + i, top, bot,
                       '-mat', 1,2,4,4,4,4, '-dir', 1,2,3,4,5,6)

    # ------------------------------------------------------------
    # 5. Beam elements
    # ------------------------------------------------------------
    J  = npipes*np.pi/2*((Dext/2)**4 - (Dint/2)**4)
    Iy = npipes*np.pi/4*((Dext/2)**4 - (Dint/2)**4)
    Iz = Iy

    op.geomTransf('Linear', 1, 0, 0, 1)

    for i in range(n_elem):
        op.element('elasticBeamColumn',
                   1000 + i,
                   node_tags[i], node_tags[i+1],
                   A, E, G, J, Iy, Iz, 1)

    # ------------------------------------------------------------
    # 6. Compute fundamental mode and extract UY only
    # ------------------------------------------------------------
    lambdas = op.eigen(1)
    if lambdas[0] <= 0:
        raise RuntimeError("Eigenvalue is non-positive.")

    uy_mode = {nd: op.nodeEigenvector(nd, 1, 2) for nd in node_tags}

    # Also return sorted arrays for plotting
    x_sorted = np.array([op.nodeCoord(nd)[0] for nd in node_tags])
    uy_sorted = np.array([uy_mode[nd] for nd in node_tags])
    order = np.argsort(x_sorted)
    
    model_name = "CS"
    vfo.createODB(model=model_name, Nmodes=4)
    vfo.plot_modeshape(model="CS",modenumber=1,scale=5000,contour='y')
    #vfo.plot_model()
    #vfo.animate_modeshape(1, 50)

    return node_tags, uy_mode, x_sorted[order], uy_sorted[order]
#L = np.array([3000,6000,9000,12000,15000,18000,21000,24000],dtype=float)

#for i in range(len(L)):
    #node_tags = build_model(n_elem=20, Lpipe=L[i], kT=600, npipes=3, E=210000)
    


node_tags = build_model(n_elem=50, Lpipe=24000, kT=600, npipes=3, E=210000, n_springs=0)

'''
L = np.array([6000,9000,12000,15000,18000,21000,24000],dtype=float)
for i in range(len(L)):
    node_tags = build_model(n_elem=20, Lpipe=L[i], kT=600, npipes=3, E=210000, n_springs=2)
'''





