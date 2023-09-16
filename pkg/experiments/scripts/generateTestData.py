########################################################
# Program for generating the training and test data 
# for ML tests
########################################################

import os, json, random, dotenv, csv
from tqdm import tqdm

OUTPUT_FILE_LOCATION = "../../../output/output.json"
RUN_COMMAND = "go run ../../../pkg/infra "
NUM_ITERATIONS = 600
dotenv_file = dotenv.find_dotenv()
dotenv.load_dotenv(dotenv_file)

def parseJSON(data):
    level_data = data["Levels"]
    return len(level_data)


def gen_training_data_dynamic():
    # set sanction length max (for use with graduated sanctions)
    max_sanc_duration = 10

    # build the command line prompt
    full_run_command = RUN_COMMAND + \
        f"-gSanc=true -gSancMax={max_sanc_duration} -verbose=false -pSanc=true"

    # start data fields
    output = [["selfish", "selfless", "collective", "level"]]

    # iteration for loop
    for _ in tqdm(range(NUM_ITERATIONS)):
        # generate the population numbers
        total_agents = 90
        state = random.randint(0,2)
        if state == 0:
            # start with selfish
            SELFISH = random.randint(0,total_agents)
            SELFLESS = random.randint(0,(total_agents-SELFISH))
            COLLECTIVE = total_agents-SELFISH-SELFLESS
        elif state == 1:
            # start with selfless
            SELFLESS = random.randint(0,total_agents)
            SELFISH = random.randint(0,(total_agents-SELFLESS))
            COLLECTIVE = total_agents-SELFISH-SELFLESS
        elif state == 2:
            # start with collective 
            COLLECTIVE = random.randint(0,total_agents)
            SELFLESS = random.randint(0,(total_agents-COLLECTIVE))
            SELFISH = total_agents-COLLECTIVE-SELFLESS

        # alter the .env file
        os.environ["AGENT_SELFISH_QUANTITY"] = str(SELFISH)
        dotenv.set_key(dotenv_file, "AGENT_SELFISH_QUANTITY", os.environ["AGENT_SELFISH_QUANTITY"])

        os.environ["AGENT_COLLECTIVE_QUANTITY"] = str(COLLECTIVE)
        dotenv.set_key(dotenv_file, "AGENT_COLLECTIVE_QUANTITY", os.environ["AGENT_COLLECTIVE_QUANTITY"])

        os.environ["AGENT_SELFLESS_QUANTITY"] = str(SELFLESS)
        dotenv.set_key(dotenv_file, "AGENT_SELFLESS_QUANTITY", os.environ["AGENT_SELFLESS_QUANTITY"])

        print(f"selfish: {SELFISH}, selfless: {SELFLESS}, collective: {COLLECTIVE}")
        # run command
        os.system(full_run_command)

        # calculate level reached
        with open(OUTPUT_FILE_LOCATION) as OUTPUT_JSON:
            DATA = json.load(OUTPUT_JSON)
            lvl = parseJSON(DATA)
            
        # append the outputs
        output.append([SELFISH, SELFLESS, COLLECTIVE, lvl])
    # save the data to a csv file
    with open('training_data_dynamic.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(output)


# repeat for dynamics turned off
def gen_training_data_non_dynamic():
    # set sanction length max (for use with graduated sanctions)
    max_sanc_duration = 10

    # build the command line prompt
    full_run_command = RUN_COMMAND + \
        f"-gSanc=true -gSancMax={max_sanc_duration} -verbose=false -pSanc=true"
    
    # start data fields
    output = [["selfish", "selfless", "collective", "level"]]

    # iteration for loop
    for _ in tqdm(range(NUM_ITERATIONS)):
        # generate the population numbers
        total_agents = 90
        state = random.randint(0,2)
        if state == 0:
            # start with selfish
            SELFISH = random.randint(0,total_agents)
            SELFLESS = random.randint(0,(total_agents-SELFISH))
            COLLECTIVE = total_agents-SELFISH-SELFLESS
        elif state == 1:
            # start with selfless
            SELFLESS = random.randint(0,total_agents)
            SELFISH = random.randint(0,(total_agents-SELFLESS))
            COLLECTIVE = total_agents-SELFISH-SELFLESS
        elif state == 2:
            # start with collective 
            COLLECTIVE = random.randint(0,total_agents)
            SELFLESS = random.randint(0,(total_agents-COLLECTIVE))
            SELFISH = total_agents-COLLECTIVE-SELFLESS

        # alter the .env file
        os.environ["AGENT_SELFISH_QUANTITY"] = str(SELFISH)
        dotenv.set_key(dotenv_file, "AGENT_SELFISH_QUANTITY", os.environ["AGENT_SELFISH_QUANTITY"])

        os.environ["AGENT_COLLECTIVE_QUANTITY"] = str(COLLECTIVE)
        dotenv.set_key(dotenv_file, "AGENT_COLLECTIVE_QUANTITY", os.environ["AGENT_COLLECTIVE_QUANTITY"])

        os.environ["AGENT_SELFLESS_QUANTITY"] = str(SELFLESS)
        dotenv.set_key(dotenv_file, "AGENT_SELFLESS_QUANTITY", os.environ["AGENT_SELFLESS_QUANTITY"])

        # run command
        os.system(full_run_command)
        
       # calculate level reached
        with open(OUTPUT_FILE_LOCATION) as OUTPUT_JSON:
            DATA = json.load(OUTPUT_JSON)
            lvl = parseJSON(DATA)
            
        # append the outputs
        output.append([SELFISH, SELFLESS, COLLECTIVE, lvl])
    # save the data to a csv file
    with open('training_data_non_dynamic.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(output)

# run file
if __name__ == "__main__":
    gen_training_data_dynamic()

    # turn off dynamic personality 
    os.environ["UPDATE_PERSONALITY"] = "false"
    dotenv.set_key(dotenv_file, "UPDATE_PERSONALITY", os.environ["UPDATE_PERSONALITY"])

    gen_training_data_non_dynamic()


