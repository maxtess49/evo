from evolution import *
import csv

# Main file, used to retrieve parameters from json file and launch the evolution

def main():
    results = []

    # A utiliser pour roulette
    listeMut = [bitFlip, oneFlip, threeFlip, fiveFlip]

    ag = GeneticAlgorithm()

    with open('seeds.csv', 'r') as csvfile:
        seeds = csv.reader(csvfile, delimiter=';')
        for row in seeds:
            for seed in row:
                print(seed)

    results += [ag.evolution(ind_zero_array(100), fit, monopoint, bitFlip, ageRemoval,
                          endCondition=(100, 1000), popSize=20, mutationRate=0.5, crossoverRate=0.5)[0][1]]

    print(results)

if __name__ == '__main__':
    main()

