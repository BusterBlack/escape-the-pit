# script for creating a normalised graph of different sanctioning mechansims
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


def normal_plot():
    FixedLengthDataP = [46.5,52.46666666666667,57.233333333333334,56.666666666666664,57.233333333333334,
                    54.733333333333334,50.06666666666667,50.93333333333333,44.4,38.03333333333333,38.4]
    FixedLengthData = [43.233333333333334,55.56666666666667,58.4,53.666666666666664,54.4,55.93333333333333,
                    54.766666666666666,53.86666666666667,51.733333333333334,46.03333333333333,50.53333333333333]
    GraduatedDataP = [44.43333333333333,50.833333333333336,56.03333333333333,56.06666666666667,52.8,57.766666666666666,
                    54.86666666666667,53.266666666666666,55.96666666666667,56.63333333333333,53.266666666666666]
    GraduatedData = [45.3,56.43333333333333,56.766666666666666,54.13333333333333,53.63333333333333,57.96666666666667,
                    56.9,57.0,56.5,54.7,57.63333333333333]
    DynamicDataP = [50.06666666666667,54.666666666666664,57.06666666666667,55.833333333333336,57.96666666666667,
                    56.63333333333333,53.1,51.733333333333334,47.53333333333333,41.13333333333333,36.833333333333336]
    DynamicData = [47.7,58.5,56.4,55.46666666666667,57.06666666666667,55.1,54.93333333333333,
                    52.333333333333336,48.56666666666667,47.3,49.733333333333334]
    
    sanctionLength = [0,1,2,3,4,5,6,7,8,9,10]


    xlabel = "Sanction Length (Turns)"
    ylabel = "Average Level Reached (n=30)"


    filename = "CombinationGraph"
    plt.figure()
    plt.plot(sanctionLength, FixedLengthDataP, "-ok", label="Fixed Sanctions")
    plt.plot(sanctionLength, FixedLengthData, "--ok", label="Fixed Sanctions")
    plt.plot(sanctionLength, GraduatedDataP, "-ob", label="Graduated Sanctions")
    plt.plot(sanctionLength, GraduatedData, "--ob", label="Graduated Sanctions")
    plt.plot(sanctionLength, DynamicDataP, "-o", label="Dynamic Sanctions", color="orange")
    plt.plot(sanctionLength, DynamicData, "--o", label="Dynamic Sanctions", color="orange")
    plt.xlabel(xlabel)
    plt.ylim([35,60])
    plt.ylabel(ylabel)
    # plt.title("Combination Graph For Fixed Length, Graduated and Dynamic Sanctions")
    patch1 = mpatches.Patch(color='black', label='Fixed Sanctions')
    patch2 = mpatches.Patch(color='blue', label='Graduated Sanctions')
    patch3 = mpatches.Patch(color='orange', label='Dynamic Sanctions')
    plt.legend(handles=[patch1,patch2,patch3])
    plt.savefig(f"../Test/FinalOutputs/{filename}.png")
    plt.savefig(f"../Test/FinalOutputs/{filename}.pdf")

    filename = "FixedSanction"
    xlabel = "Maximum Sanction Length (Turns)"
    plt.figure()
    plt.plot(sanctionLength, FixedLengthDataP, "-ok", label="Persistent")
    plt.plot(sanctionLength, FixedLengthData, "--ok", label="Non-Persistent")
    plt.xlabel(xlabel)
    plt.ylim([35,60])
    plt.ylabel(ylabel)
    # plt.title("Fixed Length Sanctions")
    plt.legend()
    plt.savefig(f"../Test/FinalOutputs/{filename}.png")
    plt.savefig(f"../Test/FinalOutputs/{filename}.pdf")

    filename = "GraduatedSanction"
    plt.figure()
    plt.plot(sanctionLength, GraduatedDataP, "-ob", label="Persistent")
    plt.plot(sanctionLength, GraduatedData, "--ob", label="Non-Persistent")
    plt.xlabel(xlabel)
    plt.ylim([35,60])
    plt.ylabel(ylabel)
    # plt.title("Graduated Length Sanctions")
    plt.legend()
    plt.savefig(f"../Test/FinalOutputs/{filename}.png")
    plt.savefig(f"../Test/FinalOutputs/{filename}.pdf")

    filename = "DynamicSanction"
    xlabel = "Initial Sanction Length (Turns)"
    plt.figure()
    plt.plot(sanctionLength, DynamicDataP, "-o", label="Persistent", color="orange")
    plt.plot(sanctionLength, DynamicData, "--o", label="Non-Persistent", color="orange")
    plt.xlabel(xlabel)
    plt.ylim([35,60])
    plt.ylabel(ylabel)
    # plt.title("Dynamic Length Sanctions")
    plt.legend()
    plt.savefig(f"../Test/FinalOutputs/{filename}.png")
    plt.savefig(f"../Test/FinalOutputs/{filename}.pdf")

    return 
    

if __name__ == "__main__":
    # fixed_dict_to_plot_both()
    # dynamic()
    normal_plot()