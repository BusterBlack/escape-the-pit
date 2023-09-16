####################################
# script to run the training model
# for the RL agent
####################################

# imports 
# standards
from collections import deque
import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt
import csv
import pandas as pd
# packages
from player import (
    agent,
    game_env
)
from logs import logging
from visualise import visualise


eps = 500
battles = 10      # maybe clear the survivors list (tbut i think this doesn't matter)
done = False
run=10

env = game_env.escapeThePitEnv()  # initiate the environemnt class
state_size = env.state_size
numNewAgents = env.numNewAgents
step_size = 3   # the step size for action space generation
agent = agent.agent(state_size, numNewAgents, step_size)  # initiate the learning agent

batch_size = 32
ep_reward_list = deque(maxlen=50)
av_rewards = []

print("================== STARTING TRAINING ==================")

for e in tqdm(range(eps)):
    state = env.resetRL()
    total_reward = 0
    output = []
    old_next_state = [0,0,0]
    for battle in range(battles):
        action = agent.act(state)
        next_state, reward, done = env.step(action)
        total_reward += reward
        if battle == 0:
            logging.createSurvivorsLog()
        else:
            logging.updateSurvivorsLog()

        agent.remember(state, action, reward, next_state, done)
        state = next_state
        if done:
            break
        if len(agent.memory) >= batch_size:
            agent.lr_decay(e)
            agent.replay(batch_size)

        # store actions and state for visualisation
        output.append([action[0], action[1], action[2], old_next_state[0], old_next_state[1], old_next_state[2], reward])
        old_next_state = next_state[0]

    # append total reward to the deque
    ep_reward_list.append(total_reward)
    # calclate the average over the deque (50 episode average)
    ep_reward_avg = np.array(ep_reward_list).mean()
    # append to average rewards
    av_rewards.append(ep_reward_avg)
    if (e+1) % 5 == 0:
        print("End of Episode {}/{}, Score: {}, Epsilon: {:.2}, Avg Score Over Last 50 Eps: {:.2f}"
            .format(e+1, eps, total_reward, agent.epsilon, ep_reward_avg))
    if (e+1) % 50 == 0:
        pd.DataFrame(output).to_csv(f"./output/RL_gameOutput_{run}_{e+1}.csv", index=False)
    if (e+1) % 100 == 0:
        pd.DataFrame(output).to_csv("./output/gameOutput.csv", index=False)
        visualise.plotAll()
    
print("================== END OF TRAINING ==================")
agent.save(f"RL_agent_mode2_wegihts_{run}")
try:
    with open(f"./RL_average_rewards_{run}.csv", 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(av_rewards)
except:
    pass

# plot average rewards
plt.figure()
plt.plot(range(0,len(av_rewards)), av_rewards, color='blue', label='Average Reward')
plt.legend()
plt.xlabel('Episodes', fontsize=16)
plt.ylabel('Average Reward', fontsize=16)
plt.title('Average Reward vs Episodes', fontsize=25)
plt.savefig(f"Average Reward vs Episodes {run}.png")
plt.show()

    
