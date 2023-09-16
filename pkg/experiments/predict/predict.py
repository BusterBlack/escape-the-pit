
# imports
# standards
import pandas as pd
import numpy as np
from keras.models import Sequential



def predictSweep(model: Sequential, data: np.ndarray, verb: str = "2") -> np.ndarray:
    """
        function to predict the progress for the parameter sweep data
        --------------------------------------------------
        @args:
            model : machine learning model used to perform predictions
            data : parameter sweep data
            verb : The verbose setting for the prediction run
        @returns:
            output (numpy.array): The progress corresponding to each parameter
    """
    # print data type
    progress = model.predict(data, verbose = verb, batch_size = 32)

    output = np.concatenate((data, progress), axis=1)
    return output


def predictProgress(model: Sequential, data: np.ndarray, verb: str = "2") -> int:
    """
        function to predict the progress of a single parameter input
        --------------------------------------------------
        @args:
            model : machine learning model used to perform predictions
            data : input data
            verb : The verbose setting for the prediction run 
        @returns:
            progress : the predicted progress
    """

    progress = model.predict(data, verbose=verb)
    # in what format is the progress? do i need to change to int (or round)
    return progress

