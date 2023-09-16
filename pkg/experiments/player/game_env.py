####################################
# These functions act as the game environment
# for the RL agent to interact with
####################################

# imports 
from typing import List, Tuple
# standards
from keras.models import Sequential
import numpy as np
import dotenv
import json
# packages
from game import (
    play
)
from config import environment_helper as eh


# mqk3 i5 q class
class escapeThePitEnv:
    """
    Environment set up to play the escape the pit game.

    This class is used to set up the environment for the escape the pit game. It is used to
    set up the game with the correct parameters and then run the game with the given action for
    either mode of game play. 

    ** Action Space **
    The action space is a list of integers, with each integer corresponding to a population
    dynamic. The action space is as follows:
        - Action[0]: Number of new Selfish agents
        - Action[1]: Number of new Selfless agents
        - Action[2]: Number of new Collective agents

    However, the action space and size is determined by the agent in this case. Who creates the
    Action size and Action space using the number of new agents needed in the game (env.numNewAgents)
    
    ** State Space **
    A tuple dictating the surviiving construct of the agents. The state space is as follows:

        | num       | Observation                           | Min   | Max   |
        |-----------|---------------------------------------|-------|-------|
        | State[0]  | Number of surviving Selfish agents    |   0   |  90   |
        | State[1]  | Number of surviving Selfless agents   |   0   |  90   |
        | State[2]  | Number of surviving Collective agents |   0   |  90   |

    ** Reward **
    The reward is the progress made in the game. This is a positive integer value.
    Each level completed with worth 1 point, up to the max number of levels (80).

    ** Starting State **
    The starting state is a list of zeros, with each index corresponding to an agent type.
    (as there are no survivors at the beginning of the game)

    ** Episode Termination **
    The episode terminates when the counter reaches the number of battles.

    ** Arguments **
    mode : type of game played
    number_of_battles : number of battles to be played
    num_agents : number of agents in the game
    counter : holds the current battle number
    done : is the game over?
    state_size : size of the state space
    numNewAgents : The number of agents to be injected into the game at each round 
    game_threshold : The percentage of agents left before the game ends
    """

    def __init__(self, battles: int = 10, mode: int = 2, state_size: int = 3):
        """
        Set up the game environment
        """
        self.mode = mode
        self.number_of_battles = battles
        self.num_agents = 90
        self.game_threshold = 0.4
        self.numNewAgents = int(self.num_agents*(1-self.game_threshold))
        self.step_size = 5
        self.counter = 1
        self.done = False
        self.state_size = state_size 
        self.state = np.zeros(self.state_size)


    def step(self, action: List[int]) -> Tuple[List[int], int, bool]:
        """
        Take a steph with a give action
        
        This function takes an action and runs the game with that action. It then returns the
        survived agent sconstruct as well as the progress made in the game. Finally it retruns
        a boolean value to indicate if the game is over or not, based on the counter value.
        ----------------------------------------
        @args:
            action (List[int]): The action to be taken in the game
        @returns:
            survivedAgents (List[int]): The population construct of the surviving agents
            progress (int): The progress made in the game
            done (bool): Is the game over?
        """


        # convert action (Q()) into actual action for environment 

        # run the game with the action and retriee the results
        if self.counter == 1:
            action = [action[0], action[1] + 36, action[2]]  # for the first sound, add the extra agents (to mkae 90) as action only considers new agents (60% of total)
            survivedAgents, progress = play.runBattle(action, True)
        else: 
            survivedAgents, progress = play.runBattle(action, False)

        # counter to see if done should be set
        if self.counter == self.number_of_battles:
            self.done = True
        else:
            self.counter += 1


        return np.array([survivedAgents]), progress, self.done
    
    def testStep(self, newAgents: int, model: Sequential) -> Tuple[np.ndarray, int, bool]:
        """
        Take step with random actions
        """

        if self.counter == 1:
            survivedAgents, _, progress = play.runRound(newAgents, model, True, "random")
        else:
            survivedAgents, _, progress = play.runRound(newAgents, model, False, "random")

        if self.counter == self.number_of_battles:
            self.done = True
        else:
            self.counter += 1

        return survivedAgents, progress, self.done

    def reset(self) -> np.ndarray:
        """
        Reset the environment parameteres to start the game over
        
        This envolves reseting the counter, done and state values whilst also setting the 
        environment START parameter to TRUE so that the first game uses the corrent 
        initialiseation functions.
        ----------------------------------------
        @args:
            None
        @returns:
            None
        """
        # reset the counter and done values
        self.done = False
        self.counter = 1 
        self.state = np.array([np.zeros(self.state_size).astype(int)])
        # change the .env file START to true
        dotenv_file = dotenv.find_dotenv()
        dotenv.load_dotenv(dotenv_file)
        eh.setenv("START", True, dotenv_file)
        survivors = "{}"
        with open("./output/survivors.json", "w") as json_file:
            json_file.write(survivors)

        return self.state
    
    def resetRL(self) -> np.ndarray:
        """
        Reset the environment parameteres to start the game over when using Reinforcement Learning
        
        This envolves reseting the counter, done and state values whilst also setting the 
        environment START parameter to TRUE so that the first game uses the corrent 
        initialiseation functions.
        ----------------------------------------
        @args:
            None
        @returns:
            None
        """
        # reset the counter and done values
        self.done = False
        self.counter = 1 
        self.state = np.array([np.array([36,0,0]).astype(int)])
        # change the .env file START to true
        dotenv_file = dotenv.find_dotenv()
        dotenv.load_dotenv(dotenv_file)
        eh.setenv("START", True, dotenv_file)
        survivors = "{}"
        with open("./output/survivors.json", "w") as json_file:
            json_file.write(survivors)

        return self.state



            
