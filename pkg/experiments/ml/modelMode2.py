#############################################################
# Functions to define the machine learning neural netwroks
# for prediction of mode 2 game (with survivors)
#############################################################

#import 
from typing import Tuple
# standards
import tensorflow as tf
from keras.models import Sequential
from keras.layers import Dense, Dropout, BatchNormalization
from keras.optimizers import Adam 


tf.random.set_seed(1234)

def model1(verbose: bool = True) -> Tuple[Sequential, str]:
    """
        This function builds a neural network and compiles it. There are 6 input features, one for each of the population constructs.
        @args:
            verbose (bool): [default == True] defines whether to print the model architecture summary 
        @returns:
            model (keras.model.sequentail): neural network model, compiled and ready for training.
            modelName (str): number of the model for saving purposes
    """
    modelName = "1"
    # define the model architecture
    model = Sequential()
    model.add(Dense(64, activation = 'relu', imput_dim=6))
    model.add(Dense(32, aciivation = 'relu'))
    model.add(Dense(1))
    
    if verbose == True:
        # print model architecture 
        print("================ MODEL SUMMARY ================")
        model.summary()

    # define the optimisation function for the model and then compile
    opt = Adam(lr=1e-3, decay=1e-3 / 200)
    model.compile(loss="mean_absolute_percentage_error", optimizer=opt, metrics=['mean_absolute_percentage_error'])

    return model, modelName
