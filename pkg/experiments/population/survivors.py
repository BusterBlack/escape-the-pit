# functions relating to the survivors

# imports
from typing import List, Tuple
# standards
import json
import pandas as pd
# packages
from operator import is_not
from functools import partial

OUTPUT_FILE_LOCATION = "./output/output.json"

def getSurvivorIDs() -> List:
    """
        function to get the agent IDs of the surviving agents and the number of them remaining. Also grab their stats 
        -------------------------------
        @returns:
            final_agents : the list of surviving agent IDs 
    """

    with open(OUTPUT_FILE_LOCATION) as json_data:
        data = json.load(json_data)
        df = pd.DataFrame(data['Levels'])

    # extract number of indexs
    size, _ = df.shape
    # extract the final fight stage of the game (it will be in a dictionary form)
    dict = df.at[size-1,"FightStage"]

    remaining = dict['Rounds'][-1]["AgentsRemaining"]
    if remaining == 0:
        return []
    else:
        # for each fight option, extract the agent IDs (these are the surviving agents)
        keys = ["AttackingAgents", "ShieldingAgents", "CoweringAgents"]
        # get all values from the fight option keys
        temp = [dict['Rounds'][-1].get(key) for key in keys]
        # filter any "None" elements (where there are no agents in that fight option)
        filtered_temp = list(filter(partial(is_not, None), temp))
        # join the list to form a single list
        final_agents = [el for nestedlist in filtered_temp for el in nestedlist]

    return final_agents

def getSurvivorConstuct() -> List[int]:
    """
        function to get the agent IDs of the surviving agents from the saved agentMap 
        -----------------------------------
        @returns:
            Survivors : List containing the numbers of each agent construct 
    """

    # get the suviving IDs
    # agents = getSurvivorIDs()

    # import the agentMap data
    with open("./output/survivors.json") as json_data:
        data = json.load(json_data)
        df = pd.DataFrame(data)
    # what is the format of the agent Map data?
    # initiate the output values
    SurvivorSELFISH, SurvivorSELFLESS, SurvivorCOLLECTIVE = 0,0,0

    # grab keys of dataframe (i.e - the surviving agent ids)
    agents = list(df.columns)

    # index agentMap and peak personality of each agent 
    if len(agents) == 0:
        pass
    else:
        for agent in agents:
            personality = df[agent].Personality
            if personality <= 25:
                SurvivorSELFISH += 1
            elif personality >= 75:
                SurvivorSELFLESS += 1
            else:
                SurvivorCOLLECTIVE += 1

    # returns
    return [SurvivorSELFISH, SurvivorSELFLESS, SurvivorCOLLECTIVE]
    

