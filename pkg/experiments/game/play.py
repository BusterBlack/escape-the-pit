################################################
# These functions are used to play the game
# callling runRound() plays the game fully,
# including action choice and results extraction
################################################

# imports
from typing import Tuple, List, Any
# standard libs
import os, dotenv
import numpy as np
from keras.models import Sequential
# packages
from config import environment_helper as eh
from population import survivors
from game import act


dotenv_file = dotenv.find_dotenv()
dotenv.load_dotenv(dotenv_file)


def runBattle(action: List[int], start: bool) -> Tuple[List[int], int]:
    """
        Run a Battle round within the game.
        ----------------------------------
        @args:
            action : the population dynamic to be set
            start : is it the first round in the game?
        
        @returns:
            survivedAgents : Agent IDs corresponding to the surviving players
            num_survivors : Number of survivors
            progress : Level reached within the game
    """

    eh.setPopulation(action, dotenv_file)

    if not start:
        eh.setenv("START", False, dotenv_file)

    max_sanc = 10
    full_run_command = "go run ./pkg/infra " + \
             f"-gSanc=true -gSancMax={max_sanc} -verbose=false -pSanc=true"

    os.system(full_run_command)

    progress = eh.getLvl()
    survivedAgents = survivors.getSurvivorConstuct()
    # print(f"Progress: {progress}, Survived: {survivedAgents}")

    return survivedAgents, progress


def runRound(total_agents: int, model: Sequential, start: bool, mode: str = "random")  -> Tuple[np.ndarray, Any, int]:
    """
        A full run of the game, including choosing actions, recreiving progress and surviving population construct
        ----------------------------------------
        @args:
            total_agents : total number of agents needed to be injected into the game
            model : machine learning model used for prediction. Set to None if we are using random actions. 
            start : dictates whether this is the first battle in the game or not
            mode : sets the play mode to random, fixed or predict actions  (i.e choosing population)

        @returns:
            action : population construct of new agents
            survivedAgnets : population construct of survived agents 
            lvl : progress of game just completed
    """
    
    # use random if we are doing a training run
    if mode == "random":
        action = act.getRandomAction(total_agents)
        # print(f"Action: {action}")
    elif mode == "fixed":
        # change here for different fixed actions (here it is 100% selfish)
        action = [total_agents,0,0]
    else:
        # get the survivor constuction to pass to the prediction algo
        survivedAgents = survivors.getSurvivorConstuct()
        # get action in form of a tuple
        action = act.getAction(survivedAgents, model, total_agents)
        # print(f"Action: {action}")

    survivedAgents, lvl = runBattle(action, start)

    # return new state, progress
    # return as np.array for compatability with learning model
    return np.array(action), np.array(survivedAgents), lvl

