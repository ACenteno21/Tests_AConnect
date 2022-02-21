"""
Script for training and testing VGG-16 with A-Connect
INSTRUCTIONS:
Due to the memory usage we recommend to uncomment the first train the model and save it. Then just comment the training
stage and then load the model to test it using the Monte Carlo simulation.
"""
import tensorflow as tf
from aconnect1.layers import Conv_AConnect, FC_AConnect
#from aconnect.layers import Conv_AConnect, FC_AConnect
from tensorflow.keras.layers import InputLayer, Conv2D, Dense, MaxPool2D, Flatten, RandomFlip, RandomRotation, RandomZoom
from tensorflow.keras.layers import BatchNormalization, Dropout, ReLU, Softmax, Rescaling, RandomTranslation, RandomCrop
Xsz = 32

def model_creation(isAConnect=False,Wstd=0,Bstd=0,
        Conv_pool=16,FC_pool=16,errDistr="normal",
        isQuant=['no','no'],bw=[8,8],isBin="yes"):

        if(not(isAConnect)):
                model = tf.keras.models.Sequential([
                        InputLayer(input_shape=(32,32,3)),
                        tf.keras.layers.experimental.preprocessing.Resizing(Xsz,Xsz),
                        ## Data augmentation layers
                        #RandomRotation(1/24),   # Rotate randomly the image 15°
                        RandomFlip("horizontal"),
                        RandomTranslation(0.1,0.1),
                        RandomZoom(0.2),
                        Conv2D(filters=128,kernel_size=(3,3),strides=(1,1),activation='relu',padding="same",kernel_regularizer = tf.keras.regularizers.l2(0.0005)),
                        BatchNormalization(),
                        Conv2D(filters=128,kernel_size=(3,3),strides=(1,1),activation='relu',padding="same",kernel_regularizer = tf.keras.regularizers.l2(0.0005)),
                        BatchNormalization(),
                        MaxPool2D(pool_size=(2,2),strides=(2,2),padding="same"),
                        Conv2D(filters=256,kernel_size=(3,3),strides=(1,1),activation='relu',padding="same",kernel_regularizer = tf.keras.regularizers.l2(0.0005)),
                        BatchNormalization(),
                        Conv2D(filters=256,kernel_size=(3,3),strides=(1,1),activation='relu',padding="same",kernel_regularizer = tf.keras.regularizers.l2(0.0005)),
                        BatchNormalization(),
                        MaxPool2D(pool_size=(2,2),strides=(2,2),padding="same"),
                        Conv2D(filters=512,kernel_size=(3,3),strides=(1,1),activation='relu',padding="same",kernel_regularizer = tf.keras.regularizers.l2(0.0005)),
                        BatchNormalization(),
                        Conv2D(filters=512,kernel_size=(3,3),strides=(1,1),activation='relu',padding="same",kernel_regularizer = tf.keras.regularizers.l2(0.0005)),
                        BatchNormalization(),
                        MaxPool2D(pool_size=(2,2),strides=(2,2)),
                        Flatten(),
                        #Dropout(0.5),
                        Dense(1024,activation='relu',kernel_regularizer = tf.keras.regularizers.l2(0.0005)),
                        BatchNormalization(),
                        #Dropout(0.5),
                        Dense(10,activation='softmax',kernel_regularizer = tf.keras.regularizers.l2(0.0005))
            ])
        else:

                model = tf.keras.models.Sequential([
                        InputLayer(input_shape=[32,32,3]),
                        tf.keras.layers.experimental.preprocessing.Resizing(Xsz,Xsz),
                        ## Data augmentation layers
                        RandomFlip("horizontal"),
                        RandomTranslation(0.1,0.1),
                        RandomZoom(0.2),
                        Conv_AConnect(filters=128,kernel_size=(3,3),Wstd=Wstd,Bstd=Bstd,errDistr=errDistr,pool=Conv_pool,padding="SAME",isQuant=isQuant,bw=bw,weights_regularizer = tf.keras.regularizers.l2(0.0005)),
                        ReLU(),
                        BatchNormalization(),
                        Conv_AConnect(filters=128,kernel_size=(3,3),Wstd=Wstd,Bstd=Bstd,errDistr=errDistr,pool=Conv_pool,padding="SAME",isQuant=isQuant,bw=bw,weights_regularizer = tf.keras.regularizers.l2(0.0005)),
                        ReLU(),
                        BatchNormalization(),
                        MaxPool2D(pool_size=(2,2),strides=(2,2),padding="SAME"),
                        Conv_AConnect(filters=256,kernel_size=(3,3),Wstd=Wstd,Bstd=Bstd,errDistr=errDistr,pool=Conv_pool,padding="SAME",isQuant=isQuant,bw=bw,weights_regularizer = tf.keras.regularizers.l2(0.0005)),
                        ReLU(),
                        BatchNormalization(),
                        Conv_AConnect(filters=256,kernel_size=(3,3),Wstd=Wstd,Bstd=Bstd,errDistr=errDistr,pool=Conv_pool,padding="SAME",isQuant=isQuant,bw=bw,weights_regularizer = tf.keras.regularizers.l2(0.0005)),
                        ReLU(),
                        BatchNormalization(),
                        MaxPool2D(pool_size=(2,2),strides=(2,2),padding="SAME"),
                        Conv_AConnect(filters=512,kernel_size=(3,3),Wstd=Wstd,Bstd=Bstd,errDistr=errDistr,pool=Conv_pool,padding="SAME",isQuant=isQuant,bw=bw,weights_regularizer = tf.keras.regularizers.l2(0.0005)),
                        ReLU(),
                        BatchNormalization(),
                        Conv_AConnect(filters=512,kernel_size=(3,3),Wstd=Wstd,Bstd=Bstd,errDistr=errDistr,pool=Conv_pool,padding="SAME",isQuant=isQuant,bw=bw,weights_regularizer = tf.keras.regularizers.l2(0.0005)),
                        ReLU(),
                        BatchNormalization(),
                        MaxPool2D(pool_size=(2,2),strides=(2,2),padding="same"),
                        Flatten(),
                        #Dropout(0.1),
                        FC_AConnect(1024,Wstd=Wstd,Bstd=Bstd,errDistr=errDistr,pool=FC_pool,isQuant=isQuant,bw=bw,weights_regularizer = tf.keras.regularizers.l2(0.0005)),
                        ReLU(),
                        BatchNormalization(),
                        #Dropout(0.1),
                        FC_AConnect(10,Wstd=Wstd,Bstd=Bstd,errDistr=errDistr,pool=FC_pool,isQuant=isQuant,bw=bw,weights_regularizer = tf.keras.regularizers.l2(0.0005)),
                        Softmax()
            ])


        return model
