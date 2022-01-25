    # sum_fitness = 0
    # for element in population_fitness:
    #     sum_fitness += element[1]
    #
    # #Calculate first quartile
    # firstQuart = (len(population_fitness)+3)/4
    # if firstQuart.is_integer():
    #     firstQuart = population_fitness[int(firstQuart) - 1][1]
    # else:
    #     firstQuart = (population_fitness[int(firstQuart) - 1][1] + population_fitness[int(firstQuart)][1] * 3) / 4
    #
    # # Calculate median
    # median = (len(population_fitness) + 1) / 2
    # if median.is_integer():
    #     median = population_fitness[int(median) - 1][1]
    # else:
    #     median = (population_fitness[int(median) - 1][1] + population_fitness[int(median)][1]) / 2
    #
    # # Calculate third quartile
    # thirdQuart = (len(population_fitness) * 3 + 1) / 4
    # if thirdQuart.is_integer():
    #     thirdQuart = population_fitness[int(thirdQuart)-1][1]
    # else:
    #     thirdQuart = (population_fitness[int(thirdQuart) - 1][1] * 3 + population_fitness[int(thirdQuart)][1]) / 4
    #
    # meanFit = sum_fitness/len(population_fitness)


import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv('data/tournoi 24/tournament_uniformWeek_0.5_tabuSearch_0.8_2_2_(0, 100)_fit/data.csv')

generation = df.index
minF = df["min_fitness"]
maxF = df["max_fitness"]
mean = df['mean']
std = df['standart_deviation']

fig = plt.figure()
ax = plt.axes()
ax.plot(generation, mean)
ax.plot(generation, minF)
ax.plot(generation, maxF)
ax.set(xlim=(-len(df.index)/10, len(df.index) +len(df.index)/10),
       ylim=(min(df["min_fitness"]) -max(df["max_fitness"])/10, max(df["max_fitness"]) +max(df["max_fitness"])/10),
       xlabel="Generation", ylabel="fitness",
       title='mean fitness per generation')

plt.fill_between(generation, mean+std, mean -std, color="gray")

plt.grid()

plt.show()
#Vincent henaux