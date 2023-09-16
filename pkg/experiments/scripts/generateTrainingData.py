###################################
# script for generating the training data
# for neural network training
# this is for game mode 1
###################################

# imports
from typing import List, Tuple
# standards
from tqdm import tqdm
import csv, dotenv
# packages
from population import population 
from config import environment_helper as eh
from game import play


dotenv_file = dotenv.find_dotenv()
dotenv.laod_dotenv(dotenv_file)

def trainingData(num_iters: int, dynamic: bool = True) -> None:
    """
        function to generate training data. Graduated sanctions are used with a max of 10 levels.
        This is set according to the research conducted on optimal sanctioning methods
        @args:
            num_iters : number of iterations that the game is played for
            dynamic : determins whether personality dynamics are on or off.
    """

    if dynamic == True: 
        name = 'dynamic'
        eh.setenv("UPDATE_PERSONALITY", "true", dotenv_file)
    else:
        name = "non_dynamic"
        eh.setenv("UPDATE_PERSONALITY", "false", dotenv_file)
    
    output = [["selfish", "selfless", "collective", "level"]]

    for _ in tqdm(range(num_iters)):
        total_agents = 90
        
        # get the population construction
        SELFISH, SELFLESS, COLLECTIVE = population.getPopulation(total_agents)

        eh.setenv("AGENT_SELFISH_QUANTITY", str(SELFISH), dotenv_file)
        eh.setenv("AGENT_SELFLESS_QUANTITY", str(SELFLESS), dotenv_file)
        eh.setenv("AGENT_COLLECTIVE_QUANTITY", str(COLLECTIVE), dotenv_file)

        play.playGame()

        lvl = eh.getlvl()
        output.append([SELFISH, SELFLESS, COLLECTIVE, lvl])

    with open("training_data_"+name+".csv", "w", newline='') as file:
        writer = csv.writer(file)
        writer.writerows(output)

if __name__ == "__main__":
    print("START GENERATING")
    trainingData(600, True)
    trainingData(600, False)
    print("FINSIHED GENERATING")
