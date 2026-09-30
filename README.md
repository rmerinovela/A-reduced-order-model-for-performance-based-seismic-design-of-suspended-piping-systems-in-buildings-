Data in support of the publication: "A reduced-order model for performance-based seismic design of suspended piping systems in buildings," by Roberto J. Merino, Roberto Gentile and Carmine Galasso.

The folder code_proposed_procedure contains two files that apply the full procedure presented in Section 3. The file equivalent_static.py performs the proposed equivalent static procedure to find the displaced shape of a suspended piping system, while the file NLTHA_SDOF.py uses the displaced shape estimated in the previous code and builds an equivalent SDOF system for performing NLTHA. 

The folder trapeze_model_parameters contains the values of the parameters of the Pinching4 material model in OpenSees used to model the hysteretic loops of the transverse and longitudinal trapeze seismic supports in machine-readable csv files. 

The folder Section2 provides the Opensees model used in the demonstration of Section 2. 

The folder Pushover2D contains the application of the equivalent static procedure and an adaptive pushover based on it to all the suspended piping system archetypes described in the paper, while the folder Pushover_SDOF contains the resulting equivalent SDOF systems. 

The folder Results contains the results of the displacements and displaced shapes for all suspended piping system archetypes in the paper. 

The folder 3D_models contains all the full 3D models of all the suspended piping system archetypes in the paper. 
