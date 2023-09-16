# functions to create population dynamics

# imports 
from typing import Tuple, Any
# standards
import numpy as np
import csv, random



def genParamData(cap: int) -> np.ndarray:
    """
        function to generate the parameter sweep training data of every population dynamic
        ---------------------------------------
        @args:
            cap : the total number of agents to create parameter sweet data for
        @returns:
            output : the output parameter sweep data
    """

    output = []

    for i in range(0,cap+1):
        for j in range(cap,0,-1):
            if i == cap:
                j=0
                l=0
                output.append([i,j,l])
                break
            if (j-i)<0:
                break
            j=j-i
            l=cap-j-i
            output.append([i,j,l])

    return np.array(output)

def saveParamData(data: Any) -> None:
    """
        function to save the parameter sweep data as a csv file
        --------------------------------------
        @args:
            data : the parameter sweep data
    """
    with open('parametersSweepData.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)

def getPopulation(total_agents: int) -> Tuple[int, int, int]:
    """
        function to get the selfish, selfless and collective number of agents in the population. 
        This is done by random using a flat distribution method for unbias training data
        @args:
            num_agents : number of agents in the population
        
        @returns:
            SELFISH : number of selfish agents
            SELFLESS : number of selfless agents
            COLLECTIVE : number of collective agents
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

    return SELFISH, SELFLESS, COLLECTIVE
