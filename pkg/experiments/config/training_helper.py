## helper functions for when doing NN training

# imports 
from typing import Tuple, List, Any
# standards
import getopt
import pandas as pd
import tensorflow as tf
import keras.backend as K
from keras.models import load_model, Sequential
import pickle


def loadModel(modelName: str) -> Any:
    """
        function to load a machine learning model
        ---------------------------------
        @args:
            modelName : name of the model to be loaded
        @returns:
            model : pre-training network
    """
    model = load_model(modelName+".h5")
    return model

def clear_weights() -> None:
    """
        function to clear current keras session and reset any current nn weights
    """
    K.clear_session()
    tf.compat.v1.reset_default_graph()

def save_history(history: Any, modelNumber: str) -> None:
    """
        function to save the .fit() training history
        @args:
            history : .fit() training history for data extraction
            modelNumber : the number of the ML architecture model being used
    """
    # with open("./trainingHistoryModel"+modelNumber, 'wb') as file:
    #     pickle.dump(history.history, file)

    df = pd.DataFrame(history.history)
    df.to_csv("trainingHistoryModel"+modelNumber+".csv", index=False)


def save_model(model: Sequential, modelNumber: str) -> None:
    """
        function to save the current ML architecture model
        @args:
            model: machine learning model (compiled and trained)
            modelNumber : the number of the ML architecture model being used
    """
    model.save("progress_predictor_"+modelNumber+".h5")


def save_prediction(dict: dict, modelName: str) -> None:
    """
        function to save the predicted data after completion
        -----------------------------
        @args:
            dict : dictionary of the population construction andpredicted progress
            modelName : machine learning model name
    """

    df = pd.DataFrame(dict)
    df.to_csv("prediction_results_model"+modelName+".csv", index=False)

    # df.to_csv(f"predictionResults_{name}.csv", index=False)


def training_data_import(argv) -> Any:
    """
    function to import the training data .csv data and store as a pandas.dataframe
    -----------------------------------------
    @args:
      argv : command line imputs - name of the file to extract the .csv data

    @returns:
        data : (pd.DataFrame) the loaded data in a pandas data frame
    """
    opts, args = getopt.getopt(argv,":f")
    filename = args[0]
    # import training data
    data = pd.read_csv(filename)
    # visualise the dataframe
    print("============= VISUALISE DATAFRAME ==============")
    print(data)

    return data


def create_data_sets(data: pd.DataFrame, mode: bool = False) -> Tuple[List, List, List, List, List, List]:
    """
    function to create the training, test and validation data sets from the dataframe set
    -------------------------------------------
    @args:
      data : the training input dataframe for extaction
      mode : defines the mode of game under play. False = mode 1 (no survivors)
    """

    if mode == False:
        # format training data into input features and output label
        input_data = data.iloc[:,[0,1,2]].to_numpy()
        labels = data.iloc[:,[3]].to_numpy()
    elif mode == True:
        # format training data into input features and output labels, according to game play mode 2 (survivors)
        input_data = data.iloc[:,[0,1,2,3,4,5]].to_numpy()
        labels = data.iloc[:,[6]].to_numpy()

    num_items = len(labels) # how many samples are there

    # split data into training, test and validation
    X_train, X_test, X_val = input_data[:int(num_items*0.7)], input_data[int(num_items*0.7):int(num_items*0.9)], input_data[int(num_items*0.9):]
    Y_train, Y_test, Y_val = labels[:int(num_items*0.7)], labels[int(num_items*0.7):int(num_items*0.9)], labels[int(num_items*0.9):]

    # is there any data augmentation that needs to be performed (i doubt it )

    return X_train, X_test, X_val, Y_train, Y_test, Y_val
