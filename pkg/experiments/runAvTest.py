##########################################
# Script to run the game for multiple
# iteration and calculate the average 
# points scored
##########################################

# imports
# standards
from tqdm import tqdm
# packages
from game import play
from player import game_env
from config import training_helper

def main():
    env = game_env.escapeThePitEnv()
    env.reset()

    number_of_agents = 90
    number_of_games = 30
    rounds = 10


    print("============== RANDOM GAME ==================")
    list_of_points_random = []
    for i in tqdm(range(number_of_games)):
        points = 0
        for j in range(rounds):
            if j == 0:
                number_of_new_agents = number_of_agents
                Action, survivedAgents, progress = play.runRound(number_of_new_agents, "None", True, "random")
            else:
                number_of_new_agents = number_of_agents - sum(survivedAgents)
                Action, survivedAgents, progress = play.runRound(number_of_new_agents, "None", False, "random")

            points += progress

        list_of_points_random.append(points)
        env.reset()

    print("Average Points For Random Game Play: ", sum(list_of_points_random)/len(list_of_points_random))
    print("============== PREDICTED GAME ==================")
    list_of_points_predict = []
    model = training_helper.loadModel("../Training Data/MODE 2/model 1/progress_predictor_mode2_1")

    for i in tqdm(range(number_of_games)):
        points = 0
        for j in range(rounds):
            if j == 0:
                number_of_new_agents = number_of_agents
                Action, survivedAgents, progress = play.runRound(number_of_new_agents, model, True, "predict")
            else:
                number_of_new_agents = number_of_agents - sum(survivedAgents)
                Action, survivedAgents, progress = play.runRound(number_of_new_agents, model, False, "predict")

            points += progress
            
        list_of_points_predict.append(points)
        env.reset()

    print("Average Points For Predicted Game Play: ", sum(list_of_points_predict)/len(list_of_points_predict))

if __name__ == "__main__":
    main()