from abaqus import * 
import numpy as np
pmodel= mdb.ModelFromInputFile(name='F1', inputFileName='C:/Users/elidi/Documents/Abaqus_job/cohesive_model/F1.inp')
##Nodes
setCZ=pmodel.rootAssembly.sets['CONTRUZ']
NodesCZ=[]
for node in setCZ.nodes:
    NodesCZ.append([node.label,node.coordinates[0],node.coordinates[1],node.coordinates[2]])
np.savetxt("C:/Users/elidi/Documents/Abaqus_job/cohesive_model/nodes_cz.txt",np.asarray(NodesCZ),delimiter=',')
