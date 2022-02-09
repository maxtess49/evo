import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path
import numpy as np
import onemaxFunctions

# Pandas mean on a dataframe of the columns to mean

def makeGraf(folder, listOp):
       allcsvForSeeds = list(Path(folder).rglob("*.csv"))
       mean = pd.read_csv(allcsvForSeeds[0])
       if listOp is not None:
              historyMethodsMean = stringSeriesToList(mean["methodsHistory"])
              historyProbMean = stringSeriesToList(mean["probOpe"])

       maxGen = max(mean["generation"])

       for file in allcsvForSeeds[1:]:

              df = pd.read_csv(file)

              if max(df["generation"]) < maxGen:
                     maxGen = max(df["generation"])

              if listOp is not None:
                     historyMethodsMean = np.add(stringSeriesToList(df["methodsHistory"][:maxGen]), historyMethodsMean[:maxGen])
                     historyProbMean = np.add(stringSeriesToList(df["probOpe"][:maxGen]), historyProbMean[:maxGen])



              mean["min_fitness"] = mean["min_fitness"][:maxGen] + df["min_fitness"][:maxGen]
              mean["max_fitness"] = mean["max_fitness"][:maxGen] + df["max_fitness"][:maxGen]
              mean["mean"] = mean["mean"][:maxGen] + df["mean"][:maxGen]
              mean["standard_deviation"] = mean["standard_deviation"][:maxGen] + df["standard_deviation"][:maxGen]

       mean["min_fitness"] = mean["min_fitness"].div(len(allcsvForSeeds))
       mean["max_fitness"] = mean["max_fitness"].div(len(allcsvForSeeds))
       mean["mean"] = mean["mean"].div(len(allcsvForSeeds))
       mean["standard_deviation"] = mean["standard_deviation"].div(len(allcsvForSeeds))

       if listOp is not None:
              historyMethodsMean = np.divide(historyMethodsMean, len(allcsvForSeeds))
              historyProbMean = np.divide(historyProbMean, len(allcsvForSeeds))

       # fitness + use graf
       fig = plt.figure()
       ax = plt.axes()
       ax.plot(mean["generation"], mean["mean"], label="mean fitness")
       ax.plot(mean["generation"], mean["min_fitness"], label="min fitness")
       ax.plot(mean["generation"], mean["max_fitness"], label="max fitness")

       lengthGraf = 0
       if listOp is not None:
              listOfOp = [[t[o] for t in historyMethodsMean] for o in range(len(listOp))]
              for o in range(len(listOp)):
                     plt.plot(listOfOp[o], label=str(listOp[o].__name__))

              for o in range(len(listOp)):
                     maxOpe = historyMethodsMean[-1][o]
                     if lengthGraf < maxOpe:
                            lengthGraf = maxOpe

                     if lengthGraf < max(mean["max_fitness"]):
                            lengthGraf = max(mean["max_fitness"])
              ax.set(xlim=(-1, maxGen*1.1),
                     ylim=(-1, lengthGraf * 1.1),
                     xlabel="Generation", ylabel="fitness/Application of operations",
                     title='mean fitness and operation usage per generation')
       else:
              lengthGraf = max(mean["max_fitness"] * 1.1)
              if lengthGraf == 0:
                     lengthGraf = 1

              ax.set(xlim=(-1, maxGen*1.1),
                     ylim=(-1, lengthGraf * 1.1),
                     xlabel="Generation", ylabel="fitness",
                     title='mean fitness per generation')

       plt.legend()

       plt.fill_between(mean["generation"], mean["mean"] + mean["standard_deviation"],
                        mean["mean"] - mean["standard_deviation"], color="gray", label="standard deviation")

       plt.grid()
       #plt.savefig(folder + "/fig_use_and_fitness_per_gen.png")
       plt.show()

       if listOp is not None:
              # Percentage per fit graf
              fig = plt.figure()
              ax = plt.axes()

              listOfOp = [[t[o] for t in historyProbMean] for o in range(len(listOp))]
              for o in range(len(listOp)):
                     plt.plot(mean["max_fitness"][:maxGen], listOfOp[o], label=str(listOp[o].__name__))

              ax.set(xlim=(-1, max(mean["max_fitness"])*1.1),
                     ylim=(-0.1, 1.1),
                     xlabel="max fitness", ylabel="% of use",
                     title='Percentage of use of operation per fitness max of the population')
              plt.legend()
              plt.grid()
              #plt.savefig(folder + "/fig_percentage_per_fit.png")
              plt.show()

              # Percentage per gen graf
              fig = plt.figure()
              ax = plt.axes()

              listOfOp = [[t[o] for t in historyProbMean] for o in range(len(listOp))]
              for o in range(len(listOp)):
                     plt.plot(mean["generation"][:maxGen], listOfOp[o], label=str(listOp[o].__name__))

              ax.set(xlim=(-1, maxGen*1.1),
                     ylim=(-0.1, 1.1),
                     xlabel="generation", ylabel="% of use",
                     title='Percentage of use of operation per generation')
              plt.legend()
              plt.grid()
              #plt.savefig(folder + "/fig_percentage_per_gen.png")
              plt.show()


# Get list from pandas Series of strings
def stringSeriesToList(column):
       result = []
       for prob in column:
              tmp = prob.strip("[]").split(", ")
              for i in range(len(tmp)):
                     tmp[i] = float(tmp[i])
              result += [tmp]
       return result

makeGraf("/home/etud/PycharmProjects/evo/data/(1000, 40000)/tournamentSelection_monopoint_roulette_[oneFlip_threeFlip_fiveFlip_bitFlip]fit/",
         [onemaxFunctions.oneFlip, onemaxFunctions.threeFlip, onemaxFunctions.fiveFlip, onemaxFunctions.bitFlip])