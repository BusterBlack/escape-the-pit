########################################################################
# Script for determining the progress within the simulation based on the 
# population dynamics at the start of the game.
########################################################################

# import packages
import tensorflow as tf
from keras import backend as K
import pandas as pd
import numpy as np
import pickle 
from keras.models import Sequential 
from keras.callbacks import LearningRateScheduler, ReduceLROnPlateau, EarlyStopping
from keras.layers import Dense
from keras.layers import Dropout, BatchNormalization
from keras.optimizers import Adam
import sys, getopt, csv
import matplotlib as plt
tf.random.set_seed(1234)

############################# HELPER FUNCTIONS #################################

# function to plot the training errors
def plot_error(history, filename, metric):
  """
    function to plot the training and validation errors and save the file in a .png file
    ----------------------------------
    @args:
      history (dict): The .fit() training history for loss metric extraction
      filename (str): Name of the filename to be saved
      metric (str): Name of the metric to be used (not loss)
  """

  if metric != None:
    fig, ax = plt.subplots(2,1)
    ax[0].plot(history.history[metric])
    ax[0].plot(history.history['val_'+metric])
    ax[0].legend(['Train', 'Val'])
    ax[0].set_title(f"{metric}")
    ax[0].set_ylabel(f"{metric}")
    ax[0].set_xlabel("Epoch")

    fig.subplots_adjust(hspace=0.5)

    ax[1].plot(history.history['loss'])
    ax[1].plot(history.history['val_loss'])
    ax[1].legend(["Train","Val"])
    ax[1].set_title("Model Loss")
    ax[1].set_ylabel("Loss")
    ax[1].set_xlabel("Epoch")
  else:
    plt.plot(history.history['loss'])
    plt.plot(history.history['val_loss'])
    plt.legend(["Train","Val"])
    plt.set_title("Model Loss")
    plt.set_ylabel("Loss")
    plt.set_xlabel("Epoch")

  plt.savefig(filename)
  plt.show()

# What is the optimum enterance population. 
def visualise_data(output):
    """
        function to visualise the progress data generated from prediction or training generation. 
        Graph is a 3-D scatter plot with a color bar representing game progress.
        -------------------------------------
        @args:
        output (np.array): 
        modelName (str): number of the model in string format
        filename (str): [default == None] name of the file to be save (if the user desires)
    """
    selfish = output[:,0]
    selfless = output[:,1]
    collective = output[:,2]
    progress = output[:,3]

    fig = plt.pyplot.figure()
    ax = fig.add_subplot(111, projection='3d')

    img = ax.scatter(selfish, selfless, collective, c=progress, cmap='YlOrRd', alpha=1)
    ax.set_xlabel("Selfish")
    ax.set_ylabel("Selfless")
    ax.set_zlabel("Collective")
    ax.set_title("Game Progress Using Prediction Model")
    fig.colorbar(img, shrink=0.6, pad=0.2)
    plt.pyplot.show()


def save_history(history, modelNumber):
    """
        function to save the .fit() training history
        @args:
            history (dict): .fit() training history for data extraction
            modelNumber (str): the number of the ML architecture model being used
    """
    with open("./trainingHistoryModel"+modelNumber, 'wb') as file:
        pickle.dump(history.history, file)

def save_model(model, modelNumber):
    """
        function to save the current ML architecture model
        @args:
            model: machine learning model (post-compilation)
            modelNumber (str): the number of the ML architecture model being used
    """
    model.save("progress_predictor_"+modelNumber+".h5")

def clear_weights():
    """
        function to clear the current keras session and reset the weights for a new training session
    """
    K.clear_session()
    tf.compact.v1.reset_default_graph()

############################# DATA HANDLING FUNCTIONS ####################

def data_import(argv):
    """
    function to import the .csv data and store as a pandas.dataframe
    -----------------------------------------
    @args:
      filename (str): name of the file to extract the .csv data
    """
    opts, args = getopt.getopt(argv,":f")
    filename = args[0]
    # import training data
    data = pd.read_csv(filename)
    # visualise the dataframe
    print("============= VISUALISE DATAFRAME ==============")
    print(data)

    return data

def create_data_sets(data):
    """
    function to create the training, test and validation data sets from the dataframe set
    -------------------------------------------
    @args:
      data (pandas.dataframe): the training input dataframe for extaction
    """
    # format training data into input features and output label
    input_data = data.iloc[:,[0,1,2]].to_numpy()
    labels = data.iloc[:,[3]].to_numpy()

    num_items = len(labels) # how many samples are there

    # split data into training, test and validation
    X_train, X_test, X_val = input_data[:int(num_items*0.7)], input_data[int(num_items*0.7):int(num_items*0.9)], input_data[int(num_items*0.9):]
    Y_train, Y_test, Y_val = labels[:int(num_items*0.7)], labels[int(num_items*0.7):int(num_items*0.9)], labels[int(num_items*0.9):]

    # is there any data augmentation that needs to be performed (i doubt it )

    return X_train, X_test, X_val, Y_train, Y_test, Y_val



############################# MACHINE EARNING MODELS ################################# 


def train_and_test_model1(X_train, X_test, X_val, Y_train, Y_test, Y_val):
    """
        function to build and train a machine learning model, then saving the model in .h5 form
        @args:
            X_train (numpy.array): inputing train data
            X_test (numpy.array): input test data
            X_val (numpy.array): input validation data
            Y_train (numpy.array): labels corresponding to the input training data
            Y_test (numpy.array): labels corresponding to the input test data
            Y_val (numpy.array): labels corresponding to the input validation data
    """
    # define the NN architecture using the sequential package
    model = Sequential()
    model.add(Dense(64, activation='relu', input_dim=3))
    model.add(Dense(32, activation='relu'))
    model.add(Dense(1))

    # print the architecture summary for figure purposes
    print("============= MODEL SUMMARY ==============")
    model.summary()

    # define the optimisation function for the model and then compile
    opt = Adam(lr=1e-3, decay=1e-3 / 200)
    model.compile(loss="mean_absolute_percentage_error", optimizer=opt, metrics=['mean_absolute_percentage_error'])

    # perform the trainings
    print("[INFO] ============== Training Model ================ ")
    history = model.fit(X_train, Y_train, validation_data=(X_val,Y_val), epochs=100, batch_size=32)

    # save hisotry and model for later use
    print("================= SAVING MODEL =================")
    save_history(history, "1")
    save_model(model, "1")

    # perform the validation testing, and display the results 
    score = model.evaluate(X_test, Y_test, verbose=0)
    print('Test loss (model 1):', score[0])
    print('Test metric (model 1):'. score[1])

    plot_error(history, "loss_graph_model1", "mean_squared_error")

    return model

def train_and_test_model2(X_train, X_test, X_val, Y_train, Y_test, Y_val):
    """
        function to build and train a machine learning model, then saving the model in .h5 form
        @args:
            X_train (numpy.array): inputing train data
            X_test (numpy.array): input test data
            X_val (numpy.array): input validation data
            Y_train (numpy.array): labels corresponding to the input training data
            Y_test (numpy.array): labels corresponding to the input test data
            Y_val (numpy.array): labels corresponding to the input validation data
    """
    # # second model containing batch normalisation, dropout and normally distributed random initialized weights. 
    model2 = Sequential()
    model2.add(Dense(128, activation='relu', input_dim=3, kernel_initializer='random_normal', bias_initializer='zeros'))
    model2.add(BatchNormalization())
    model2.add(Dense(64, activation='relu'))
    model2.add(BatchNormalization())
    model2.add(Dropout(0.3))
    model2.add(Dense(32, activation='relu'))
    model2.add(BatchNormalization())
    model2.add(Dense(1))
    # add early stopping and returning best weights
    earlystop = EarlyStopping(monitor='val_accuracy', min_delta=0, patience=4, verbose=0, model='auto', baseline=None, restore_best_weights=True)
    # add dynamic learning rate based on plateau
    reduce_lr = ReduceLROnPlateau(monitor="val_loss", factor=0.2, patience=1, min_lr=0.00001, min_delta=0.01)

    print("============= MODEL SUMMARY ==============")
    model2.summary()

    # opt = Adam(lr=1e-3, decay=1e-3 / 200)
    opt = Adam(lr=1e-3)
    model2.compile(loss="mean_absolute_error", optimizer=opt, metrics=["mean_absolute_error", "mean_squared_error"])

    # train the model
    print("================= TRAINING MODEL =================")
    history2 = model.fit(X_train, Y_train, validation_data=(X_val, Y_val), epochs=100, batch_size=64, callbacks=[reduce_lr, earlystop])

    # save hisotry and model for later use
    print("================= SAVING MODEL =================")
    save_history(history2, "2")
    save_model(model2, "2")

    # perform the validation testing, and display the results 
    print("=========== MODEL 2 ============")
    score2 = model2.evaluate(X_test, Y_test, verbose=1)
    print('Test loss (model 2):', score2[0])
    print('Test metric (model 2):'. score2[1])

    plot_error(history2, "loss_graph_model2.png", "mean_squared_error")

    return model2

# function to perform a parameter sweep of population constructs and predict the output. 
def predict_progress(model, name):
    """
        function to predict the progress within the game based on the population constuction using a pre-training neural network
        --------------------------------------------------
        @args:
            model: machine learning model to be used to perform the predictions
            name (str): name of the model for file saving purposes    
    """    
    # import the parameter data csv
    param_data = pd.read_csv('./parametersSweepData.csv')
    predict_data = param_data.iloc[:,[0,1,2]].to_numpy()
    # run prediction on it 
    progress = model.predict(predict_data, verbose=2, batch_size=32)
    # results are in a numpy array
    # concatenate results and output to another csv file for visualisation
    output = np.concatenate((predict_data, progress), axis=1)
    # output to a csv file with titles
    dict = {
                "Selfish": output[:,0], 
                "Selfless": output[:,1], 
                "Collective": output[:,2], 
                "Progress": output[:,3]
            }
    df = pd.DataFrame(dict)
    df.to_csv(f"predictionResults_{name}.csv", index=False)
    # return output for visualisation
    return output


############################## MAIN SCRIPT #################################

if __name__ == "__main__":
    # grab files from the input arguments
    data = data_import(sys.argv[1:])
    # generate the training, test and validation data sets
    X_train, X_test, X_val, Y_train, Y_test, Y_val = create_data_sets(data)
    # build, compile and train the neural network model 1
    model = train_and_test_model1(X_train, X_test, X_val, Y_train, Y_test, Y_val)
    # predict the progress of all population constructions using model 1
    output = predict_progress(model, "model1")
    visualise_data(output)
    # build, compile and train the neural network model 2
    model2 = train_and_test_model2(X_train, X_test, X_val, Y_train, Y_test, Y_val)
    # predict the progress of all population construction using model 2
    output2 = predict_progress(model2, "model2")
    visualise_data(output2)
    
