
# imports
from typing import List, Tuple, Any
# standards
import numpy as np
import pandas as pd
# packages
from config import training_helper



def printProgress(output: np.ndarray) -> None:
    """ 
        function to find the maximum progress of all the prediction and return the population construction that achieved it
        --------------------------------------
        @args:
            output (numpy.ndarray): the output of the prediction in the format - (selfish, selfless, collective, progress)
    """
    max = np.max(output[:,4])

    idx = np.where(output[:,4]==max)

    print(f"Maximum Progress: {max}")
    print(f"Achieved with population: {output[idx,:]}")


def getBestProgress(output: np.ndarray) -> Tuple[int, np.ndarray]:
    """
        function to find the maximum progress from the parameter sweep predictions, and the construction that achieved it
        -------------------------------------
        @args:
            output : the output of the prediction in the format - (selfish, selfless, collective, progress)
        @returns:
            progress : the maximum progress
            construct : the population construct that achieved the maximum progress
    """

    max = np.max(output[:,-1])
    idx = np.where(output[:,-1]==max)

    return int(max), output[idx,:]


def createData(paramData: np.ndarray, survivors: List[int]) -> np.ndarray:
    """
        function to create the data set for the parameter sweep data coupled with the current survivor construct
        ---------------------------------------------------
        @args: 
            paramData : the set of parameter sweep data
            survivors : the construct of the surviving agents
        @returns:
            dataSet : the coupled parameter sweep data with the survivor construct
    """
    dataSet = np.concatenate( (paramData, np.repeat(np.array([survivors]).astype(int), len(paramData), axis=0)), axis=1)
    # return
    return dataSet


def savePredictOutput(output: np.ndarray, name: str, mode: int = 1) -> None:
    """ 
        function to save the output of the prediction as a dictionary. This works for both type of game
        This function is used to store a parameter sweep dataset for visualisation
        In the case of mode=2, this would meaning saving the parameter sweep prediction for a single surviving constuction
        ---------------------------------------------------
        @args:
            output : the output of the prediction process in the form - selfish, selfless, collective, progress
            name : the name of the model for saving purposes
            mode : determines which mode of the game is being played, 1 mean no survivors
    """
    if mode == 1:
        dict = {
                    "selfish": output[:,0],
                    "Selfless": output[:,1],
                    "Collective": output[:,2],
                    "Progress": output[:,3]
                }
    else:
        dict = {
                    "NewSelfish": output[:,0],
                    "NewSelfless": output[:,1],
                    "NewCollective": output[:,2],
                    "SurvivorSelfish": output[:,3],
                    "SurvivorSelfless": output[:,4],
                    "SurvivorCollective": output[:,5],
                    "Progress": output[:,6]
            } 
    training_helper.save_prediction(dict, name)


def loadParamData() -> np.ndarray:
    """
        function to load the parameter sweep data
        -------------------------------------------------
        @returns:
            predict_data : the parameter sweep data in an.ndarray
    """
    
    # import the parameter data csv
    param_data = pd.read_csv('./parametersSweepData.csv')
    predict_data = param_data.iloc[:,[0,1,2]].to_numpy()
    return predict_data
    
