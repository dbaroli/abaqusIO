from abaqus import * 
import numpy as np
import os 
homefolder= os.getcwd()
pathfile=os.path.join(homefolder,'F1.inp')
pmodel= mdb.ModelFromInputFile(name='F1', inputFileName=pathfile)
##Nodes
setCZ=pmodel.rootAssembly.sets['CONTRUZ']
NodesCZ=[]
for node in setCZ.nodes:
    NodesCZ.append([node.label,node.coordinates[0],node.coordinates[1],node.coordinates[2]])
np.savetxt("nodes_cz.txt",np.asarray(NodesCZ),delimiter=',')
