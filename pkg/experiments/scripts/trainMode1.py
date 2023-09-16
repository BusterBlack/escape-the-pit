# main script for building, compiling, training and testing machine learning algos on game


# imports
# standards
import sys
# packages
from predict import predictHelper, predict
from ml import modelMode1
from visualise import visualise 
from population import population
from config import training_helper


if __name__ == "__main__":
    # grab command line arguments
    data = training_helper.training_data_import(sys.argv[1:])
    # generate the training, test and validation data sets
    X_train, X_test, X_val, Y_train, Y_test, Y_val = training_helper.create_data_sets(data)
    
    # reset the keras session 
    training_helper.clear_weights()

    # build, compile and train the neural network model 1
    model1 = modelMode1.model1(X_train, X_test, X_val, Y_train, Y_test, Y_val)
    print("======= MODEL 1 TRAINED AND SAVED ==========")
    
    # get param data
    sweepData = population.genParamData(90)

    # predict the progress of all population constructions using model 1
    output = predict.predictSweep(model1, sweepData, "model1")
    visualise.visualise_data(output)

    predictHelper.printProgress(output)   
    
    # build, compile and train the neural network model 2
    model2 = modelMode1.model2(X_train, X_test, X_val, Y_train, Y_test, Y_val)
    print("======= MODEL 2 TRAINED AND SAVED ==========")

    # predict the progress of all population construction using model 2
    output2 = predict.predictSweep(model2, sweepData, "model2")
    visualise.visualise_data(output2)

    predictHelper.printProgress(output)
