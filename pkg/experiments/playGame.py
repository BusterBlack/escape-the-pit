#########################################
# Main script for running the game
#########################################
# move this to the play() package for use in main scripts

# imports 
# standards
import sys, getopt
from tqdm import tqdm
import pandas as pd
import json
# packages
from game import play
from config import training_helper
from player import game_env
from logs import logging
from visualise import visualise


def main(arg) -> int:
    # opts, args = getopt.getopt(arg, ":f")
    # mode can have three values: "random", "fixed", "predict"
    mode = arg[0]
    verbose = arg[1]

    # create the game environment with standard setup (mode=2, battles=10, agents=90)
    env = game_env.escapeThePitEnv()
    env.reset()
    if verbose == "True":
        print(f"=============== GAME STARTING USING {mode} ====================")
    points = 0
    number_of_agents = 90
    rounds = 10
    oldSurvived = [0,0,0]
    output = []

    # define machine learning model to be used
    if mode == "predict":
        try:
            modelNum = "1"
            model = training_helper.loadModel("../Training Data/MODE 2/model "+modelNum+"/progress_predictor_mode2_"+modelNum)
        except:
            print("Model Name ERROR. If you wish to run without prediction, then enter --None-- as model name")
            sys.exit(0)
    else:
        model = "None"

  
    for i in range(rounds):
        if verbose == "True":    
            print(f"========== BATTLE {i+1} STARTS ========")
        if i == 0:
            number_of_new_agents = number_of_agents
            Action, survivedAgents, progress = play.runRound(number_of_new_agents, model, True, mode)
            logging.createSurvivorsLog()

        else:
            number_of_new_agents = number_of_agents - sum(survivedAgents)
            Action, survivedAgents, progress = play.runRound(number_of_new_agents, model, False, mode)
            logging.updateSurvivorsLog()

        output.append([Action[0], Action[1], Action[2], oldSurvived[0], oldSurvived[1], oldSurvived[2], progress])

        oldSurvived = survivedAgents

        points += progress
        if verbose == "True":
            print("========== BATTLE ENDED ========")
            print(f"Points Scored: {progress}")
            print(f"Total Points: {points}")
            print("================================")
    
    print("============ GAME ENDS ===========")
    print(f"Your Total Score: {points}")
    

    pd.DataFrame(output).to_csv("./output/gameOutput.csv", index=False)

    visualise.plotAll()
    
if __name__ == "__main__":
    arg = sys.argv[1:]
    main(arg)
