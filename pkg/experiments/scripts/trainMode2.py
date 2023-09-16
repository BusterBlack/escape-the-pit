#################################################
# Script for training of models
#################################################

# imports
# standards
import sys
from keras.callbacks import ReduceLROnPlateau, EarlyStopping
# packages
from config import training_helper
from ml import modelMode2
from visualise import visualise


def main() -> None:
    # import the data
    data = training_helper.training_data_import(sys.argv[1:])

    # create the datasets
    X_train, X_test, X_val, Y_train, Y_test, Y_val = training_helper.create_data_sets(data, True)

    # reset keras
    training_helper.clear_weights()

    # get the pre-compiled model
    model, name = modelMode2.model1()

    # define early stopping 
    earlystop = EarlyStopping(monitor='val_accuracy', min_delta=0, patience=4, verbose=0, mode='auto', baseline=None, restore_best_weights=True)
    # add dynamic learning rate based on plateau
    reduce_lr = ReduceLROnPlateau(monitor="val_loss", factor=0.2, patience=1, min_lr=0.00001, min_delta=0.01)


    # perform the training
    history = model.fit(X_train, Y_train, validation_data=(X_val,Y_val), epochs=100, batch_size=32)
    
    # fit using early stop and reducing learning rate
    # history = model.fit(X_train, Y_train, validation_data = (X_val, Y_val), epochs = 100, batch_size=32, callbacks=[reduce_lr, earlystop])

    # sve the history and the model
    training_helper.save_history(history, name)
    training_helper.save_model(model, name)

    # evaluate
    score = model.evaluate(X_test, Y_test, verbose="0")
    print('Test loss:', score[0])
    print('Test metric:', score[1])

    visualise.plot_error(history, "loss_graph_model"+name, "mean_squared_error")

if __name__ == "__main__":
    main()
