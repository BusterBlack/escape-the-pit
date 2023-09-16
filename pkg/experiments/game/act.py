##################################
# Functions to get actions based on surviving agents
##################################

# imports
from typing import List, Tuple
# standards
import random
import numpy as np
# packages
from population import population
from predict import predict, predictHelper
from keras.models import Sequential


def getAction(survivedAgents: List[int], model: Sequential, numNewAgents: int) -> np.ndarray:
    """
        Function to get game action based on prediction
        -------------------------------------
        @args:
            survivedAgents: Listing containing the numbers of each different agent type in the form [selfish, selfless, collective]
            model (keras.model.sequential): the machine learning model used in prediction 
            numNewAgents : number of fresh agents neededs

        @returns:
            action: contains the new population construct to be used in the game (i.e. the action)
    """
    # get parameter sweep data
    newAgentSweep = population.genParamData(numNewAgents)
    # build data set
    data = predictHelper.createData(newAgentSweep, survivedAgents)
    # run prediction
    predictedProgress = predict.predictSweep(model, data, verb=0)
    # get max
    max, construct = predictHelper.getBestProgress(predictedProgress)

    # return action
    return construct[0][0][0:3].astype(int)

def getRandomAction(total_agents: int) -> List[int]:
    """
        function to get the selfish, selfless and collective number of agents in the population.
        This is done by random using a flat distribution method for unbias training data
        --------------------------------------
        @args:
            total_agents: number of agents in the population

        @returns:
            output: random population construction (i.e. the action)
    """
    state = random.randint(0,2)
    if state == 0:
        # start with selfish 
        SELFISH = random.randint(0, total_agents)
        SELFLESS = random.randint(0, (total_agents-SELFISH))
        COLLECTIVE = total_agents - SELFISH - SELFLESS
    elif state == 1:
        # next selfless
        SELFLESS = random.randint(0, total_agents)
        SELFISH = random.randint(0, (total_agents-SELFLESS))
        COLLECTIVE = total_agents - SELFISH - SELFLESS
    else:
        # next collective 
        COLLECTIVE = random.randint(0, total_agents)
        SELFLESS = random.randint(0, (total_agents-COLLECTIVE))
        SELFISH = total_agents - SELFLESS - COLLECTIVE

    return [SELFISH, SELFLESS, COLLECTIVE]
