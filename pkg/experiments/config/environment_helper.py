
# imports 
from typing import List, Any
# standards
import os, json, dotenv
import numpy as np


OUTPUT_FILE_LOCATION = "./output/output.json"


def parseJSON(data: dict) -> int:
    level_data = data["Levels"]
    return len(level_data)

def setenv(name: str, val: int, dotenv_file: Any) -> None:
    """
     function to change the value of a variable in the .env file
     -----------------------------
     @args:
         name : name of the variable to change
         val : value of the variable to be set
         dotenv_file : .env file to be edited
    """
    os.environ[name] = str(val)
    dotenv.set_key(dotenv_file, name, os.environ[name])

def setPopulation(action: List[int], dotenv_file) -> None:
    """
    set the environment file with the population values dictated by the action elements
    ----------------------------
    @args: 
        action : the population construction values
        dotenv_file : the .env file location
    """
    setenv("AGENT_SELFISH_QUANTITY", action[0], dotenv_file)
    setenv("AGENT_SELFLESS_QUANTITY", action[1], dotenv_file)
    setenv("AGENT_COLLECTIVE_QUANTITY", action[2], dotenv_file)

def getLvl() -> int:
    """
        function to return the final level of the game (progress)
        @args:
            lvl : level progress within the game (after finished game)
    """
    with open(OUTPUT_FILE_LOCATION) as OUTPUT_JSON:
        DATA = json.load(OUTPUT_JSON)
        lvl = parseJSON(DATA)

    return lvl

def listToArray(list: List) -> np.ndarray:
    """
        function to convert a list to a numpy array
        ---------------------------
        @args:
            list : a list
        @returns: 
            array : output array
    """
    return np.array(list)
