"""
An optimized script to perform the training and test to the simple neural network using A-Connect
"""

import tensorflow as tf
import numpy as np
from 2FC_model import build_model	#Load the networks models
from datetime import datetime
import aconnect.layers as layers	#Load layers from the library
import aconnect.scripts as scripts	#Load scripts from the library
Sim_err = [0,0.3,0.5,0.7]	#Define all the simulation errors
Wstd = [0.3,0.5,0.7] 			#Define the stddev for training
Bstd = Wstd
isBin = ["no"]					#Do you want binary weights?
bits = 8 	#Dataset quantization
imgSize = [28,28]	#Dataset size
(x_train, y_train), (x_test, y_test) = scripts.load_ds(imgSize=imgSize, Quant=bits) #Load dataset
bits = str(bits)+'bits'
size = '_'+str(imgSize[0])+'x'+str(imgSize[1])+'_'
for p in range(len(isBin)):
    for c in range(len(Wstd)): #Iterate over the Wstd and Bstd for training
        wstd = str(int(100*Wstd[c]))
        bstd = str(int(100*Bstd[c]))
        name = 'AConnect'+size+bits+'_Wstd_'+wstd+'_Bstd_'+bstd
        if isBin[p] == "yes":
            name = name+'_BW'
        print("*****************************TRAINING NETWORK*********************")
        print("\n\t\t\t", name)
        model = build_model(imgsize=imgSize,Wstd=Wstd[c],Bstd=Bstd[c],isBin=isBin[p], pool=None) #Get the model
        optimizer = tf.keras.optimizers.SGD(learning_rate=0.1,momentum=0.9)#Define optimizer #Model training parameters
        model.compile(optimizer=optimizer,loss=['sparse_categorical_crossentropy'],metrics=['accuracy']) #Compile the model
        print(model.summary()) #Print the summary
        history = model.fit(x_train,y_train,validation_split=0.2,epochs = 20,batch_size=256) #Train the model
        acc = history.history['accuracy'] #Save the accuracy and the validation accuracy
        val_acc = history.history['val_accuracy']
        string = './Models/'+name+'.h5' #Define the folder and the name of the model to be saved
        model.save(string,include_optimizer=True) #Save the model
        np.savetxt('../Results/2FC_MNIST/Training data/'+name+'_acc'+'.txt',acc,fmt="%.2f") #Save in a txt the accuracy and the validation accuracy for further analysis
        np.savetxt('../Results/2FC_MNIST/Training data/'+name+'_val_acc'+'.txt',val_acc,fmt="%.2f")

for k in range(len(isBin)): #Iterate over the networks
    for m in range(len(Wstd)): #Iterate over the training Wstd and Bstd
        wstd = str(int(100*Wstd[m]))
        bstd = str(int(100*Bstd[m]))
        name = 'AConnect'+size+bits+'_Wstd_'+wstd+'_Bstd_'+bstd
        if isBin[k] == "yes":
            name = name+'_BW'
        string = './Models/'+name+'.h5'
        custom_objects = {'Conv_AConnect':layers.Conv_AConnect,'FC_AConnect':layers.FC_AConnect} #Custom objects for model loading purposes
        for j in range(len(Sim_err)): #Iterate over the sim error vector
            Err = Sim_err[j]
            if Err != Wstd[m]: #If the sim error is different from the training error, do not force the error
                force = "yes"
            else:
                force = "no"
            if Err == 0: #If the sim error is 0, take only 1 sample
                N = 1
            else:
                N = 1000
            now = datetime.now()
            starttime = now.time()
            #####
            print('\n\n*******************************************************************************************\n\n')
            print('TESTING NETWORK: ', name)
            print('With simulation error: ', Err)
            print('\n\n*******************************************************************************************')
            acc_noisy, media = scripts.MonteCarlo(string,x_test,y_test,N,Err,Err,force,0,name,custom_objects
            ,run_model_eagerly=True,evaluate_batch_size=10000) #Perform the simulation
            #For more information about MCSim please go to Scripts/MCsim.py
            #####
            now = datetime.now()
            endtime = now.time()

            print('\n\n*******************************************************************************************')
            print('\n Simulation started at: ',starttime)
            print('Simulation finished at: ', endtime)
