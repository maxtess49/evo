from evolution import *
import csv

# Main file, used to retrieve parameters from json file and launch the evolution

def main():
    results = []

    # A utiliser pour roulette
    listeMut = [oneFlip, threeFlip, fiveFlip, geneticDisease]

    ag = GeneticAlgorithm()
    ONE_MAX_SIZE = 100

    # with open('seeds.csv', 'r') as csvfile:
    #      seeds = csv.reader(csvfile, delimiter=';')
    #      for row in seeds:
    #          for seed in row:
    #
    #              # Settings of ag
    #              ag.setSeed(seed)
    #              ag.setIndividualBase(ind_zero_array(ONE_MAX_SIZE))
    #              ag.setFitness(fit)
    #              ag.setEndCond((ONE_MAX_SIZE, 1000))
    #              ag.setSelection(tournamentSelection)
    #              ag.setMutation(listeMut, 1)
    #              ag.setCrossover(monopoint, 0)
    #              ag.setInsertion(ageRemoval)
    #
    #              results += [ag.evolution(popSize=100, reinforcement="roulette")[0][1]]
    #
    #          print(results)
    #          results = []


    ag.setIndividualBase(ind_zero_array(ONE_MAX_SIZE))
    ag.setFitness(fit)
    ag.setEndCond((ONE_MAX_SIZE, 1000))
    ag.setSelection(tournamentSelection)
    ag.setMutation(listeMut, 1)
    ag.setCrossover(monopoint, 0)
    ag.setInsertion(ageRemoval)
    ag.setSeed(8)

    results += [ag.evolution(popSize=100, reinforcement="roulette")[0][1]]
    print(results)



if __name__ == '__main__':
    main()

