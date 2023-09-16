
#imports
from typing import Any
# Standards
import json
import pandas as pd
import numpy as np



def ExtractSurvivorsFromTrackLog() -> Any:
    """
    function to extract the survivors from the track log json file using the survivors log json file
    -----------------------------------
    @returns:
        survivors : (pd.DataFrame) dictionary containing the agent IDs as keys and the agent data as values
    """
    # import the tracking log
    with open("./output/track.json") as json_data:
        data = json.load(json_data)
        df = pd.DataFrame(data)

    # import the survivors log
    with open("./output/survivors.json") as json_data:
        data = json.load(json_data)
        df2 = pd.DataFrame(data)

    # get the suviving IDs
    agents = list(df2.columns)

    # create a dictionary with the agent Ids as keys and the values as the agent data from the tracking log
    survivors = {}
    for agent in agents:
        survivors[agent] = df["Agents"][agent]

    return pd.DataFrame(survivors)

# function to extract the survivors 
def createSurvivorsLog() -> None:
    """
        function to create a json file containing the survivors from the track log
        -----------------------------------
        @returns:
            None
    """
    # keep only suvivors from track log
    tracklog = ExtractSurvivorsFromTrackLog()
    # save tracklog as json
    tracklog.to_json("./output/survivorsTrack.json")
    print(f'************ Survivors log created with: {len(tracklog.columns)} remaining ************')

def updateSurvivorsLog() -> None:
    """
    Update the survivors log by removing any agents who have died
    -----------------------------------
    @returns:
        None
    """
    # import the tracking log
    with open("./output/survivorsTrack.json") as json_data:
        data = json.load(json_data)
        df = pd.DataFrame(data)

    # import the survivors log
    with open("./output/survivors.json") as json_data:
        data = json.load(json_data)
        df2 = pd.DataFrame(data)

    # import track log
    with open("./output/track.json") as json_data:
        data = json.load(json_data)
        df3 = pd.DataFrame(data)

    # get the suviving IDs
    agents = list(df2.columns)
    # get agent IDs from suvivorsTrack
    agents2 = list(df.columns)

    # compare the two lists and keep only the agents that are in both
    agentsSurvived = list(set(agents) & set(agents2))

    if len(agentsSurvived) != 0:
        # create a dictionary with the agent Ids as keys and the values as the agent data from the tracking log
        survivors = {}
        for agent in agentsSurvived:
            # new dictionary entery with agent values from both dataframes
            survivors[agent] = {
                "FightAction":  np.append(df[agent]["FightAction"], df3["Agents"][agent]["FightAction"]),
                "Hp":           np.append(df[agent]["Hp"], df3["Agents"][agent]["Hp"]),
                "Stamina":      np.append(df[agent]["Stamina"], df3["Agents"][agent]["Stamina"]),
                "Attack":       np.append(df[agent]["Attack"], df3["Agents"][agent]["Attack"]),
                "Defense":      np.append(df[agent]["Defense"], df3["Agents"][agent]["Defense"]),
                "LevelsAlive":  np.append(df[agent]["LevelsAlive"], df3["Agents"][agent]["LevelsAlive"]),
                "Personality":  np.append(df[agent]["Personality"], df3["Agents"][agent]["Personality"]),
                # it should be noted that the "Sanctioned" value here represents if an agent has defected, NOT if they are sanctioned
                "Defector":     np.append(df[agent]["Defector"], df3["Agents"][agent]["Defector"]),
                "Sanctioned":   np.append(df[agent]["Sanctioned"], df3["Agents"][agent]["Sanctioned"]),
                "TSNlength":    np.append(df[agent]["TSNlength"], df3["Agents"][agent]["TSNlength"]),
                }
            

            # survivors[agent] = df[agent]
        # save as json
        pd.DataFrame(survivors).to_json("./output/survivorsTrack.json")
        print(f'************ Survivors log updated with: {len(agentsSurvived)} remaining ************')
    else:
        df.to_json("./output/survivorsTrack.json")
        print("************ There are no survivors from the first level remaining ************")



