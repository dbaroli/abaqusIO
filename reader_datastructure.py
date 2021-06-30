from odbAccess import openOdb
from abaqusConstants import ELEMENT_NODAL, INTEGRATION_POINT, NODAL
import numpy as np
import os 

def dataField(odbFile,fieldName=None):
    # Extract ABAQUS ODB into VTK unstructured grid data format
    nbNodes = 0
    nbElements = 0
    nodeCoord = list()
    eleConnection = list()
    cellType = list()
    cellField = list()
    # Open the odb
    
    myOdb = openOdb(odbFile,readOnly=True)
    stepName = 'Step-Rolling'
    frames = myOdb.steps[stepName].frames
    rootassembly = myOdb.rootAssembly
    instance = rootassembly.instances
    names= rootassembly.instances.keys()
    
    
    
    
    
    # Isolate the instances, get the number of nodes and elements
    for instanceName in names:
        
        if instanceName is  names[-1]:
            
            print(instanceName)
            myInstance = myOdb.rootAssembly.instances[instanceName]
            # needed to make mesh 2d (visualization)
            node = myInstance.nodes
            element = myInstance.elements
            n_nodes = len(node)
            n_elements = len(element)    
            node_array = np.zeros([n_nodes,4])
            UlocalSnap1 = np.zeros((n_nodes,len(frames)))
            UlocalSnap2 = np.zeros((n_nodes,len(frames)))
            UlocalMap = np.zeros((n_nodes,len(frames)))

            for iframe in range(0,len(frames)):
                displacements = frames[iframe].fieldOutputs['U']
                displacementsU1 = displacements.getScalarField(componentLabel='U1')
                displacementsU2 = displacements.getScalarField(componentLabel='U2')
                counter=0 
                for n in node:
                    sub_disp1_node=displacementsU1.getSubset(region=n,position=ELEMENT_NODAL)    
                    sub_disp2_node=displacementsU2.getSubset(region=n,position=ELEMENT_NODAL)    
                    UlocalSnap1[counter ,iframe]=sub_disp1_node.values
                    UlocalSnap2[counter ,iframe]=sub_disp2_node.values
                    UlocalMap[counter,iframe]= n.label     
                    counter+=1 
            np.savetxt("metalForming/dataFrame/U1.txt",UlocalSnap1,delimiter=",")
            np.savetxt("metalForming/dataFrame/U2.txt",UlocalSnap2,delimiter=",")
            np.savetxt("metalForming/dataFrame/MapNode.txt",UlocalMap,delimiter=",")

            for n in node:
                node_array[n.label-1,:]=[n.label,n.coordinates[0],n.coordinates[1],n.coordinates[2]]
            np.savetxt("metalForming/data/nodes_fullMesh.txt",node_array,delimiter=",")
            element_array = np.zeros([n_elements,len(element[0].connectivity)+1])
            for e in element:
                con = np.asarray([i for i in e.connectivity])
                element_array[e.label-1,0] = e.label
                element_array[e.label-1,1::] = con-1 #vtk node numbering starts at 0, not 1
            np.savetxt("metalForming/data/connectivity_formingEnd.txt",element_array,delimiter=",")


odbFile="Job-1.odb"
myOdb = openOdb(odbFile,readOnly=True)
##Step names
print(myOdb.steps.keys())
rootassembly = myOdb.rootAssembly
instance = rootassembly.instances
names= rootassembly.instances.keys()
print(names)
instanceName=names[-1]
myInstance = myOdb.rootAssembly.instances[instanceName]
print(myInstance.nodeSets.keys())
