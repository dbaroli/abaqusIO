from abaqus import *
from abaqusConstants import *
import os 
import visualization
import numpy as np

#abaqus cae -noGUI nameofthiscript.py

def output_update(pmodel):
    # Set is PART-1-1.FIBRA or PART-1-1.INTERFACCIA.
    myassembly=pmodel.rootAssembly
    #del pmodel.fieldOutputRequests['F-Output-1']
    #del pmodel.historyOutputRequests['H-Output-1']
    print(myassembly.allInstances.keys())
    regionDef= myassembly.allInstances['PART-1-1'].sets['CONTRUZ']
	#regioDef1==assembly.allSets['PART-1-1.INTERFACCIA']
    pmodel.FieldOutputRequest(name='F-Snapshot', createStepName='Step-1', variables=('U', 'V','S','E','COORD','STATUS','SDEG','SDEV'),
                         numIntervals=160,timeMarks=ON, region=regionDef, sectionPoints=DEFAULT, rebar=EXCLUDE)

    regionDef=myassembly.allInstances['PART-1-1'].sets['CONTRUZ']
    pmodel.historyOutputRequests['H-Output-1'].setValues(variables=('S33', 'S13', 'S23', 'E33', 'E13', 'E23', 'U1', 'U2', 'U3'), 
    region=regionDef, sectionPoints=DEFAULT, rebar=EXCLUDE)                            
    


    

def updatematerial(pmodel,mu2):
    originalValues=[1000,0.4,0.03,1,0.25,3.16,9.8,26, 0.3, 0.6, 9, 0,0.003,2.804,233.4,26,0.555,0.5,0,0,28333.3,56666.7,0,0,0,200,100,10000,6000,38,0,0,0,0,0]
    #update the parameter G1 and G2
    originalValues[1] = mu2[0]
    originalValues[2] = mu2[1]

    my_materials = pmodel.materials
    materials_name=list(my_materials.keys())
    my_materials[materials_name[0]].UserMaterial(type=MECHANICAL, mechanicalConstants=originalValues)
    

    


home_directory = os.getcwd() 
abaDir=mdb.pathName
print(abaDir)
print(os.getcwd())
original_modelname = "F1"
usersubroutine_name ="finalbilinearCZM.for"
#num_parameters = 2 
makeParametrization = True # run the creation of inp just once.
runParametrization = False
# _0, _1, _2, _3 ( increase number depend on refiment on parametrize grid.)
parameterFolder = os.path.join(os.getcwd(),"Parameter_sampling")
mu2Matrix=np.loadtxt(os.path.join(parameterFolder,"parameters_0.txt"),delimiter=",")
num_parameters = mu2Matrix.shape[0]

if makeParametrization:
    modelorigin = mdb.ModelFromInputFile(name = "F1", inputFileName = os.path.join(os.getcwd(),"F1.inp"))
   
    #modelorigin = mdb.ModelFromInputFile(name = original_modelname, inputFileName = os.path.join(input_directory, original_file))
    print(type(modelorigin))
    for snap_idx in range(0,num_parameters):
        print("Loop Index {}".format(snap_idx))
        current_model = "ParametrizedCohesive_"+str(snap_idx)
        jobname= "Job_{}".format(current_model)
        mu2 = mu2Matrix[snap_idx,:]
        pmodel = mdb.Model(name=current_model, objectToCopy=modelorigin)
 
        updatematerial(pmodel, mu2)
        # no modify the mass region neither the output variation (just do it in 1st base INP)
        #add_mass_region(pmodel,factor=18)# add_mass_region(pmodel,factor=10.)
        #output_update(pmodel)
        mdb.saveAs(pathName=os.path.join(current_model))
        mdb.save()


        myJob = mdb.Job(model=current_model, name=jobname)
        myJob.setValues(userSubroutine=usersubroutine_name)
        #myJob.setValues(numCpus=2,numDomains=8,multiprocessingMode=THREADS)
        myJob.setValues(explicitPrecision=DOUBLE)
        # abaqua -noGUI Pippo.inp user=INTERSOLO3.f

        myJob.writeInput( consistencyChecking=ON)
        #shutil.move(os.path.join(home_directory,jobname+".inp"),os.path.join(home_directory,jobname+".inp"))  
    

    if runParametrization:
        for snap_idx in range(0,num_parameters):
            current_model = "ParametrizedCohesive_"+str(snap_idx)
            jobname= "Job_{}".format(current_model)
            myJob=mdb.JobFromInputFile(name=jobname,inputFileName=os.getcwd()+'{}'.format(jobname)+'.inp')
            #myJob.setValues(numCpus=2,numDomains=8,multiprocessingMode=THREADS)
            myJob.setValues(userSubroutine=usersubroutine_name)
            #mbd.writeInput()
            #mdb.saveAs(myJob.name)
            myJob.submit(consistencyChecking=OFF)
            myJob.waitForCompletion()
            print("status {}".format(myJob.status))

    

#    current_model = "simulation"+str(i)
#mdb.ModelFromInputFile(name = current_model, inputFileName = os.path.join(outputpath,current_file))
#runJob(currentModel)
