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