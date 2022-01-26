from evolution import *
import csv

# Main file, used to retrieve parameters from json file and launch the evolution

def main():
    results = []

    # A utiliser pour roulette
    listeMut = [bitFlip, oneFlip, threeFlip, fiveFlip]

    ag = GeneticAlgorithm()

    # with open('seeds.csv', 'r') as csvfile:
    #     seeds = csv.reader(csvfile, delimiter=';')
    #     for row in seeds:
    #         for seed in row:
    #
    #             # Settings of ag
    #             ag.setSeed(seed)
    #             ag.setIndividualBase(ind_zero_array(100))
    #             ag.setFitness(fit)
    #             ag.setEndCond((100, 1000))
    #             ag.setSelection(tournamentSelection)
    #             ag.setMutation(bitFlip, 0.5)
    #             ag.setCrossover(monopoint, 0.5)
    #             ag.setInsertion(ageRemoval)
    #
    #             results += [ag.evolution(popSize=20)[0][1]]
    #             print(results)
    #         results = []



    ag.setIndividualBase(ind_zero_array(100))
    ag.setFitness(fit)
    ag.setEndCond((100, 1000))
    ag.setSelection(tournamentSelection)
    ag.setMutation(bitFlip, 0.5)
    ag.setCrossover(monopoint, 0.5)
    ag.setInsertion(ageRemoval)

    results += [ag.evolution(popSize=20)[0][1]]
    print(results)



if __name__ == '__main__':
    main()

