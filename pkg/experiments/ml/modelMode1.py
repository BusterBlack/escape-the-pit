###############################
# define learning models in mode 1
###############################

# imports 
from typing import List, Tuple
# standards
import numpy as np
import tensorflow as tf
from keras import backend as K
from keras.models import Sequential 
from keras.callbacks import ReduceLROnPlateau, EarlyStopping
from keras.layers import Dense, Dropout, BatchNormalization
from keras.optimizers import Adam
# packages
from config import training_helper
from visualise import visualise

tf.random.set_seed(1234)



def model1(X_train: List[int], X_test: List[int], X_val: List[int], 
            Y_train: List[int], Y_test: List[int], Y_val: List[int]) -> Sequential:
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
    training_helper.save_history(history, "1")
    training_helper.save_model(model, "1")

    # perform the validation testing, and display the results 
    score = model.evaluate(X_test, Y_test, verbose="0")
    print('Test loss (model 1):', score[0])
    print('Test metric (model 1):', score[1])

    visualise.plot_error(history, "loss_graph_model1", "mean_squared_error")

    return model


def model2(X_train: List[int], X_test: List[int], X_val: List[int], 
            Y_train: List[int], Y_test: List[int], Y_val: List[int]) -> Sequential:
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
    earlystop = EarlyStopping(monitor='val_accuracy', min_delta=0, patience=4, verbose=0, mode='auto', baseline=None, restore_best_weights=True)
    # add dynamic learning rate based on plateau
    reduce_lr = ReduceLROnPlateau(monitor="val_loss", factor=0.2, patience=1, min_lr=0.00001, min_delta=0.01)

    print("============= MODEL SUMMARY ==============")
    model2.summary()

    # opt = Adam(lr=1e-3, decay=1e-3 / 200)
    opt = Adam(lr=1e-3)
    model2.compile(loss="mean_absolute_error", optimizer=opt, metrics=["mean_absolute_error", "mean_squared_error"])

    # train the model
    print("================= TRAINING MODEL =================")
    history2 = model2.fit(X_train, Y_train, validation_data=(X_val, Y_val), epochs=100, batch_size=64, callbacks=[reduce_lr, earlystop])

    # save hisotry and model for later use
    print("================= SAVING MODEL =================")
    training_helper.save_history(history2, "2")
    training_helper.save_model(model2, "2")

    # perform the validation testing, and display the results 
    print("=========== MODEL 2 ============")
    score2 = model2.evaluate(X_test, Y_test, verbose="1")
    print('Test loss (model 2):', score2[0])
    print('Test metric (model 2):', score2[1])

    visualise.plot_error(history2, "loss_graph_model2.png", "mean_squared_error")

    return model2
