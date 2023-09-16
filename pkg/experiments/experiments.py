import os
import json
import matplotlib.pyplot as plt
from tqdm import tqdm

OUTPUT_FILE_LOCATION = "./output/output.json"
RUN_COMMAND = "go run ./pkg/infra "
NUM_ITERATIONS = 30


def parseJSON(data):
    level_data = data["Levels"]
    return len(level_data)


# Fixed Length Sanctions

def fixedLength(is_persistent: bool = False):
    durations = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    duration_comp = {}
    for duration in tqdm(durations):
        avg_level_reached = 0
        for _ in range(NUM_ITERATIONS):
            full_run_command = RUN_COMMAND + \
                f"-fSanc={duration} -verbose=false"
            if is_persistent:
                full_run_command += " -pSanc=true"

            os.system(full_run_command)

            with open(OUTPUT_FILE_LOCATION) as OUTPUT_JSON:
                DATA = json.load(OUTPUT_JSON)
                lvl = parseJSON(DATA)
                avg_level_reached += lvl
        avg_level_reached /= NUM_ITERATIONS
        duration_comp[duration] = avg_level_reached
        print(
            f"Iteration For Duration: {duration} Has Finished - Average Score {avg_level_reached}")

    for duration, score in duration_comp.items():
        print(f"duration:{duration}, score:{score}")

    fixed_dict_to_plot(duration_comp, is_persistent)

    return duration_comp


def fixed_dict_to_plot_both():
    # title = "Level Reached Against Fixed Sanction Length"
    xlabel = "Fixed Sanction Length (Turns)"
    ylabel = f"Average Level Reached (n={NUM_ITERATIONS})"
    filename = "fixedBoth"

    d1 = fixedLength(is_persistent=True)
    d2 = fixedLength(is_persistent=False)

    names1, counts1 = zip(*d1.items())
    names2, counts2 = zip(*d2.items())

    plt.figure()
    plt.plot(names1, counts1, "-o", label="Persistent Sanctions")
    plt.plot(names2, counts2, "-o", label="Non-Persistent Sanctions")
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend()
    plt.savefig(f"./figures/{filename}.pdf")


def fixed_dict_to_plot(data: dict, is_persistent: bool):

    # title = "Level Reached Against Fixed Sanction Length"
    xlabel = "Fixed Sanction Length (Turns)"
    ylabel = f"Average Level Reached (n={NUM_ITERATIONS})"
    filename = "fixedNonPersist"
    if is_persistent:
        filename = "fixedPersist"

    names, counts = zip(*data.items())
    plt.figure()
    plt.plot(names, counts, "-o")
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.savefig(f"./figures/{filename}.pdf")


# Graduated Sanctions

def graduated(is_persistent: bool = False):
    durations = [0, 1, 2, 3, 4, 5,6, 7, 8, 9, 10]
    duration_comp = {}
    for duration in tqdm(durations):
        avg_level_reached = 0
        for _ in range(NUM_ITERATIONS):
            full_run_command = RUN_COMMAND + \
                f"-gSanc=true -gSancMax={duration} -verbose=false"
            if is_persistent:
                full_run_command += " -pSanc=true"

            os.system(full_run_command)

            with open(OUTPUT_FILE_LOCATION) as OUTPUT_JSON:
                DATA = json.load(OUTPUT_JSON)
                lvl = parseJSON(DATA)
                avg_level_reached += lvl
        avg_level_reached /= NUM_ITERATIONS
        duration_comp[duration] = avg_level_reached
        print(
            f"Iteration For Max Duration: {duration} Has Finished - Average Score {avg_level_reached}")

    for duration, score in duration_comp.items():
        print(f"Max duration:{duration}, score:{score}")

    graduated_dict_to_plot(duration_comp, is_persistent)

    return duration_comp

# dynamic


def dynamic(is_persistent: bool = False):
    durations = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    duration_comp = {}
    for duration in tqdm(durations):
        avg_level_reached = 0
        for _ in range(NUM_ITERATIONS):
            full_run_command = RUN_COMMAND + \
                f"-dSanc=true -fSanc={duration} -verbose=false"
            if is_persistent:
                full_run_command += " -pSanc=true"

            os.system(full_run_command)

            with open(OUTPUT_FILE_LOCATION) as OUTPUT_JSON:
                DATA = json.load(OUTPUT_JSON)
                lvl = parseJSON(DATA)
                avg_level_reached += lvl
        avg_level_reached /= NUM_ITERATIONS
        duration_comp[duration] = avg_level_reached
        print(
            f"Iteration For Initial Duration: {duration} Has Finished - Average Score {avg_level_reached}")

    for duration, score in duration_comp.items():
        print(f"Init duration:{duration}, score:{score}")

    graduated_dict_to_plot(duration_comp, is_persistent)

    return duration_comp


def graduated_dict_to_plot_both():
    # title = "Level Reached Against Fixed Sanction Length"
    xlabel = "Maximum Graduated Sanction Length (Turns)"
    ylabel = f"Average Level Reached (n={NUM_ITERATIONS})"
    filename = "graduatedBoth"

    d1 = graduated(is_persistent=True)
    d2 = graduated(is_persistent=False)

    names1, counts1 = zip(*d1.items())
    names2, counts2 = zip(*d2.items())

    plt.figure()
    plt.plot(names1, counts1, "-o", label="Persistent Sanctions")
    plt.plot(names2, counts2, "-o", label="Non-Persistent Sanctions")
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend()
    plt.savefig(f"./figures/{filename}.pdf")


def graduated_dict_to_plot(data: dict, is_persistent: bool):

    # title = "Level Reached Against Fixed Sanction Length"
    xlabel = "Maximum Graduated Sanction Length (Turns)"
    ylabel = f"Average Level Reached (n={NUM_ITERATIONS})"
    filename = "graduatedNonPersist"
    if is_persistent:
        filename = "graduatedPersist"

    names, counts = zip(*data.items())
    plt.figure()
    plt.plot(names, counts, "-o")
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.savefig(f"./figures/{filename}.pdf")


# Dynamic Length Sanctions

def dynamic_dict_to_plot(data: dict, is_persistent: bool):
    # title = "Level Reached Against Fixed Sanction Length"
    xlabel = "Initial Dynamic Sanction Length (Turns)"
    ylabel = f"Average Level Reached (n={NUM_ITERATIONS})"
    filename = "dynamicNonPersist"
    if is_persistent:
        filename = "dynamicPersist"

    names, counts = zip(*data.items())
    plt.figure()
    plt.plot(names, counts, "-o")
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.savefig(f"./figures/{filename}.pdf")

    return


def dynamic_dict_to_plot_both():
    # title = "Level Reached Against Fixed Sanction Length"
    xlabel = "Initial Dynamic Sanction Length (Turns)"
    ylabel = f"Average Level Reached (n={NUM_ITERATIONS})"
    filename = "dynamicBoth"

    d1 = dynamic(is_persistent=True)
    d2 = dynamic(is_persistent=False)

    names1, counts1 = zip(*d1.items())
    names2, counts2 = zip(*d2.items())

    plt.figure()
    plt.plot(names1, counts1, "-o", label="Persistent Sanctions")
    plt.plot(names2, counts2, "-o", label="Non-Persistent Sanctions")
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend()
    plt.savefig(f"./figures/{filename}.pdf")


if __name__ == "__main__":
    # fixed_dict_to_plot_both()
    # dynamic_dict_to_plot_both()
    graduated_dict_to_plot_both()
