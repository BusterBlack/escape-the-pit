# helper functions for visualising different parts of the training, testing and data sections of the experiements

# imports
from typing import Any, List
# standards
import random
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import pandas as pd
import json
# packages
from logs import logging


# function to plot the training errors
def plot_error(history: Any, filename: str, metric: str) -> None:
  """
    function to plot the training and validation errors and save the file in a .png file
    ----------------------------------
    @args:
      history : The .fit() training history for loss metric extraction
      filename : Name of the filename to be saved
      metric : Name of the metric to be used (not loss)
  """

  if metric != None:
    fig, ax = plt.subplots(2,1)
    ax[0].plot(history.history[metric])
    ax[0].plot(history.history['val_'+metric])
    ax[0].legend(['Train', 'Val'])
    ax[0].set_title(f"{metric}")
    ax[0].set_ylabel(f"{metric}")
    ax[0].set_xlabel("Epoch")

    fig.subplots_adjust(hspace=0.5)

    ax[1].plot(history.history['loss'])
    ax[1].plot(history.history['val_loss'])
    ax[1].legend(["Train","Val"])
    ax[1].set_title("Model Loss")
    ax[1].set_ylabel("Loss")
    ax[1].set_xlabel("Epoch")
  else:
    plt.plot(history.history['loss'])
    plt.plot(history.history['val_loss'])
    plt.legend(["Train","Val"])
    plt.set_title("Model Loss")
    plt.set_ylabel("Loss")
    plt.set_xlabel("Epoch")

  plt.savefig(filename)
  plt.show()

# What is the optimum enterance population. 
def visualise_data(output: np.ndarray, modelName: str, filename: str = ""):
    """
        function to visualise the progress data generated from prediction or training generation. 
        Graph is a 3-D scatter plot with a color bar representing game progress.
        -------------------------------------
        @args:
        output : prediction output including the input data
        modelName : number of the model in string format
        filename : name of the file to be save (if the user desires)
    """
    selfish = output[:,0]
    selfless = output[:,1]
    collective = output[:,2]
    progress = output[:,3]

    fig = plt.figure(figsize=(7.5,6))
    ax = fig.add_subplot(111, projection='3d')

    img = ax.scatter(selfish, selfless, collective, c=progress, cmap='YlOrRd', alpha=1)
    ax.set_xlabel("Selfish")
    ax.set_ylabel("Selfless")
    ax.set_zlabel("Collective")
    fig.colorbar(img, shrink=0.6, pad=0.2, orientation = "horizontal")
    # change orientation so graphs are all in the same angle
    ax.view_init(-161,53)
    plt.title("Game Progress Using Prediction Model"+modelName+" Based Om Population Construction")
    plt.show()
    if filename == "":
        plt.savefig(filename)


def plot_lr(history: Any, filename: str):
    """
        function to plot the evolution of the learning rate over the course of training
        ---------------------------------------
        @args:
            history : .fit() training history for data extraction
            filename : name of the file to be saved
    """
    lr = history.history['lr'] # extract the learning rate data
    plt.figure()
    plt.plot(range(0,len(lr)), lr)
    plt.title("Learning Rate Evolution")
    plt.ylabel("Learning Rate")
    plt.xlabel("Epochs")
    plt.savefig(filename)
    print("================== FILE SAVED ================")
    plt.show()

def plot_track(tracking: Any,filename: str):
    """
        plot a collection of graphs showing a selection of agents from the tracking data
        -------------------------------
        @args:
            tracking : the data to be plotted
            filename : str of the filename to be saved
    """

    # if its a data frame
    agents = tracking.columns

    plotAgents = []
    # get 5 random numbers in length on survivors
    for i in range(min(len(agents),5)):
        if len(agents) < 5:
            idx = i
        else:
            idx = random.randint(0,len(agents))
        plotAgents.append(tracking[agents[idx-1]])

    # plot
    plt.figure(figsize=(13,10))
    # list of colors
    colors = ["blue", "red", "cyan", "pink", "yellow"]

    plt.subplot(2,2,1)
    for i in range(min(len(agents),5)):
        plt.plot(range(0, len( plotAgents[i]["Personality"] )), plotAgents[i]["Personality"], color=colors[i])

    plt.title("Personality Evolution", fontsize=16)
    plt.ylabel("Personality", fontsize=12)
    plt.xlabel("Round", fontsize=12)

    plt.subplot(2,2,2)
    for i in range(min(len(agents),5)):
        plt.plot(range(0, len( plotAgents[i]["TSNlength"] )), plotAgents[i]["TSNlength"], color=colors[i])

    plt.title("TSN Size Evolution", fontsize=16)
    plt.ylabel("TSN Size", fontsize=12)
    plt.xlabel("Round", fontsize=12)

    plt.subplot(2,2,3)
    for i in range(min(len(agents),5)):
        plt.plot(range(0, len( plotAgents[i]["Hp"] )), plotAgents[i]["Hp"], color=colors[i])

    plt.title("Health Evolution", fontsize=16)
    plt.ylabel("Hp", fontsize=12)
    plt.xlabel("Round", fontsize=12)

    plt.subplot(2,2,4)
    for i in range(min(len(agents),5)):
        plt.plot(range(0, len( plotAgents[i]["FightAction"] )), plotAgents[i]["FightAction"], color=colors[i])

    plt.title("Fight Action Evolution", fontsize=16)
    plt.ylabel("Fight Action", fontsize=12)
    plt.xlabel("Round", fontsize=12)

    plt.savefig(filename)
    plt.show()


def plot_sanctioned(tracking: Any, filename: str) -> None:
    """
    Plot weather the agent has been sanctioned or not at each stage of the game
    -------------------------------
    @args:
        tracking : the data to be plotted
        filename : str of the filename to be saved
    """
        # if its a data frame
    agents = tracking.columns

    plotAgents = []
    # get 5 random numbers in length on survivors
    for i in range(min(len(agents), 5)):
        if len(agents) < 5:
            idx = i
        else:
            idx = random.randint(0,len(agents))
      
        plotAgents.append(tracking[agents[idx-1]])

    for agent in plotAgents:
        # agent["Sanctioned"] = [3 if item else 2 for item in agent["Sanctioned"]]

        agent["Defector"] = [3 if item else 2 for item in agent["Defector"]]

    # plot
    plt.figure(figsize=(13,10))
    colors = ["black", "red", "green", "blue", "yellow"]
    for i in range(min(len(plotAgents), 5)):
        plt.plot(range(0, len( plotAgents[i]["Sanctioned"] )), plotAgents[i]["Sanctioned"], label="Sanctioned", color=colors[i])
        plt.plot(range(0, len( plotAgents[i]["Defector"] )), plotAgents[i]["Defector"], linestyle="--", label="Defector", color=colors[i])

    plt.ylim(0,4)

    plt.title("Agent Defection and Sanction Evolution", fontsize=20)
    # plt.title("Agent Sanctioned Evolution Over Game For Up To 5 Random Agents")
    plt.ylabel("Sanctioned: 0=False, 1=True, Defector: 2=False, 3=True", fontsize=15)
    # plt.ylabel("Sanctioned (1 = Sanctioned, 2 = Not Sanctioned)")
    plt.xlabel("Round", fontsize=15)
    plt.legend()

    plt.savefig(filename)
    plt.show()


def spiderweb(data: Any, filename: str, title: str) -> None:
    """
    plot a spiderweb graph for the prediction/training data
    ---------------------------
    @args:
        data : input data in a pd.DataFrame
        filename : name of file to save
        title : title name
    """
    # Each attribute we'll plot in the radar chart.
    labels = ['New Selfish', 'New Selfless', 'New Collective', 'Survived Selfish', 'Survived Selfless', 'Servived Collective']

    values = data.iloc[:,[0,1,2,3,4,5]].to_numpy()
    progress = data.iloc[:,[6]].to_numpy()
    # values = values[0:20]
    # progress = progress[0:20]

    # Number of variables we're plotting.
    num_vars = len(labels)
    maxlim = np.amax(values)

    # Split the circle into even parts and save the angles
    # so we know where to put each axis.
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
    angles += angles[:1]

    # ax = plt.subplot(polar=True)
    # fig, ax = plt.subplots(figsize=(10, 6), subplot_kw=dict(polar=True))
    fig, ax = plt.subplots(figsize=(10, 6), subplot_kw=dict(polar=True))
    cmap = cm.get_cmap('viridis', 40)
    sm = cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(vmin=min(progress), vmax=max(progress)))
    sm.set_array([])

    for values, color_idx in zip(values, progress):
        color = cmap(color_idx)
        values = np.concatenate((values, [values[0]]))  # Close the shape
        ax.plot(angles, values, marker='o', label='Data', color=color)

    # Fix axis to go in the right order and start at 12 o'clock.
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)

    # Draw axis lines for each angle and label.
    ax.set_thetagrids(np.degrees(angles[:-1]), labels)

    for label, angle in zip(ax.get_xticklabels(), angles):
        if angle in (0, np.pi):
            label.set_horizontalalignment('center')
        elif 0 < angle < np.pi:
            label.set_horizontalalignment('left')
        else:
            label.set_horizontalalignment('right')

    # Ensure radar goes from 0 to 100.
    ax.set_ylim(0, maxlim+10)
    ax.set_rlabel_position(180 / num_vars)
    ax.tick_params(colors='#222222')
    ax.tick_params(axis='y', labelsize=8)
    ax.grid(color='#AAAAAA')
    ax.spines['polar'].set_color('#222222')
    ax.set_facecolor('#FAFAFA')
    cbar = plt.colorbar(sm, ax=ax, pad=0.15, label = "Progress")
    # ax.legend(["Progress"])
    ax.set_title(title, y=1.08)

    # plt.savefig(filename)
    plt.show()

def plot_game() -> None:
    """
    Plot the construct of each play during the game
    """
    # data = pd.read_csv("../Tracking Visualisations/final/Predicted (model1) 10 Rounds/gameOutput.csv")
    data = pd.read_csv("./output/gameOutput.csv")
    newSelfish = data.iloc[:,[0]].to_numpy()
    newSelfless = data.iloc[:,[1]].to_numpy()
    newCollective = data.iloc[:,[2]].to_numpy()
    survivedSelfish = data.iloc[:,[3]].to_numpy()
    survivedSelfless = data.iloc[:,[4]].to_numpy()
    survivedCollective = data.iloc[:,[5]].to_numpy()
    progress = data.iloc[:,[6]].to_numpy()

    plt.figure(figsize=(13,10))
    plt.plot(range(0, len( newSelfish )), newSelfish, label="New Selfish")
    plt.plot(range(0, len( newSelfless )), newSelfless, label="New Selfless")
    plt.plot(range(0, len( newCollective )), newCollective, label="New Collective")
    plt.plot(range(0, len( survivedSelfish )), survivedSelfish, label="Survived Selfish")
    plt.plot(range(0, len( survivedSelfless )), survivedSelfless, label="Survived Selfless")
    plt.plot(range(0, len( survivedCollective )), survivedCollective, label="Survived Collective")
    plt.plot(range(0, len( progress )), progress, label="Progress", color="black", linewidth=3, linestyle="--")
    plt.legend() 

    plt.title("Actions and Survied Agents Constructs Over The Game", fontsize=20)
    plt.xlabel("Game", fontsize=15)
    plt.ylabel("Number of Agents", fontsize=15)

    plt.savefig("game.png")
    plt.show()

def plotAll(mode: bool = True) -> None:
    """
    Retrieve survivors tracking log data and plot all related graphs
    ---------------------------------------------------------------
    @args:
        mode : [default = True] boolean value to indicate whether to create or retrieve data
    """
    if mode:
        # extract the survivors from the track log
        with open("./output/survivorsTrack.json") as json_data:
            data = json.load(json_data)
            survivors = pd.DataFrame(data)
    else:
        survivors = logging.ExtractSurvivorsFromTrackLog()
    
    plot_track(survivors, "survivors.png")
    plot_sanctioned(survivors, "sanctioned.png")
    plot_game()
    print("PLOT SPIDERWEB") # plot this in colab as the color mapoing is not working on my machine



def plotRewards():
    """
    Plot all the rewards from the different models
    """
    
    df1 = pd.read_csv("../Tracking Visualisations/RL/RL_average_rewards_3.csv").columns.to_numpy()
    df2 = pd.read_csv("../Tracking Visualisations/RL/RL_average_rewards_4.csv").columns.to_numpy()
    df3 = pd.read_csv("../Tracking Visualisations/RL/RL_average_rewards_5.csv").columns.to_numpy()
    df4 = pd.read_csv("../Tracking Visualisations/RL/RL_average_rewards_6.csv").columns.to_numpy()
    df5 = pd.read_csv("../Tracking Visualisations/RL/RL_average_rewards_7.csv").columns.to_numpy()
    df6 = pd.read_csv("../Tracking Visualisations/RL/RL_average_rewards_8.csv").columns.to_numpy()
    df7 = pd.read_csv("../Tracking Visualisations/RL/RL_average_rewards_9.csv").columns.to_numpy()
    df8 = pd.read_csv("../Tracking Visualisations/RL/RL_average_rewards_10.csv").columns.to_numpy()

    data = [df1,df2,df3,df4,df5,df6,df7,df8]
    data = [np.array([float(x[:5]) for x in df]) for df in data]

    plt.figure(figsize = (10,8))
    plt.plot(data[0], color='black', label='Q-Learning - FAS')
    plt.plot(data[1], color='blue', label='Q-Learning - PAS')
    plt.plot(data[2], color='red', label='SARSA-V')
    plt.plot(data[3], color='orange', label='SARSA-VDNN-Drop')
    plt.plot(data[4], color='pink', label='Adam')
    plt.plot(data[5], color='cyan', label='SARSA-VDNN')
    plt.plot(data[6], color='green', label='SGD')
    plt.title("Average Rewards Over Pervious 50 Episodes Per Episode")
    plt.ylabel("Average Reward")
    plt.xlabel("Episode")
    plt.legend()
    plt.show()
