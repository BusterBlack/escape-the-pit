###################################
# script for generating the training data
# for neural network training
# this is for game mode 2
###################################

# imports
# standards
from tqdm import tqdm
import csv, dotenv
# packages
from config import environment_helper as eh
from player import game_env
from game import play

dotenv_file = dotenv.find_dotenv()
dotenv.load_dotenv(dotenv_file)

def trainingData(num_iters: int, dynamic: bool = True):
    """
        function to generate training data. Graduated sanctions are used with a max of 10 levels.
        This is set according to the research conducted on optimal sanctioning methods
        @args:
            num_iters : number of iterations that the game is played for
            dynamic : determins whether personality dynamics are on or off.
    """

    env = game_env.escapeThePitEnv()
    env.reset()


    if dynamic == True: 
        name = 'dynamic'
        eh.setenv("UPDATE_PERSONALITY", "true", dotenv_file)
    else:
        name = "non_dynamic"
        eh.setenv("UPDATE_PERSONALITY", "false", dotenv_file)
    

    output = [["NewSelfish", "NewSelfless", "NewCollective", "SurvivorSelfish", "SurvivorSelfless", "SurvivorCollective", "Progress"]]
    # define initial number of survivors
    oldSurvived = [0,0,0]

    for i in tqdm(range(num_iters)):
        print("========== BATTLE STARTS ========")
        if i == 0:
            total_agents = 90
        else:
            total_agents = 90 - sum(survivedAgents)
        # run the round using random action
        if i == 0:
            newAgents, survivedAgents, lvl = play.runRound(total_agents, "None", True, "random")
        else:
            newAgents, survivedAgents, lvl = play.runRound(total_agents, "None", False, "random")
        
        print("========== BATTLE ENDED ========")

        # append the constructions to the output file new agents + old surviving agents
        output.append([newAgents[0], newAgents[1], newAgents[2], oldSurvived[0], oldSurvived[1], oldSurvived[2], lvl])
        # store survived agents for the next round
        oldSurvived = survivedAgents

    with open("training_data_mode2_"+name+".csv", "w", newline='') as file:
        writer = csv.writer(file)
        writer.writerows(output)

if __name__ == "__main__":
    print("START GENERATING")
    trainingData(600)
    print("FINSIHED GENERATING")
