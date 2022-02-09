from evolution import *
from statScript import makeGraf
import csv

# Main file, used to retrieve parameters from json file and launch the evolution

def main():
    results = []

    # A utiliser pour roulette
    listeMut = [oneFlip, threeFlip, fiveFlip, bitFlip]
    #listToApply = [[oneFlip, threeFlip, fiveFlip, bitFlip], [oneFlip, threeFlip, fiveFlip, bitFlip, dummyMutation], [oneFlip, threeFlip, fiveFlip, bitFlip, geneticDisease], [oneFlip, threeFlip, fiveFlip, bitFlip, dummyMutation, geneticDisease]]
    ag = GeneticAlgorithm()
    listToApply = [oneFlip, threeFlip, fiveFlip, bitFlip, dummyMutation, geneticDisease,
                   [oneFlip, threeFlip, fiveFlip], [oneFlip, threeFlip, fiveFlip, bitFlip],
                   [oneFlip, threeFlip, fiveFlip, bitFlip, dummyMutation],
                   [oneFlip, threeFlip, fiveFlip, bitFlip, dummyMutation, geneticDisease]]
    ONE_MAX_SIZE = 1000

    # Left fitness we want at least, right nbr of generations
    endCondition = (ONE_MAX_SIZE, ONE_MAX_SIZE * 40)

    # We study mutations, so those are statics
    ag.setIndividualBase(ind_zero_array(ONE_MAX_SIZE))
    ag.setFitness(fit)
    ag.setEndCond(endCondition)
    ag.setSelection(tournamentSelection)
    ag.setCrossover(monopoint, 0)
    ag.setInsertion(fitnessRemoval)




    for method in listToApply:
        dataFolder = './data/' + str(endCondition) + "/tournamentSelection_monopoint_"
        with open('seeds.csv', 'r') as csvfile:
            seeds = csv.reader(csvfile, delimiter=';')
            for row in seeds:
                for seed in row:
                    # Settings of ag
                    ag.setSeed(seed)
                    ag.setMutation(method, 1)

                    # Call to GA
                    if type(method) == list:
                        results += [ag.evolution(popSize=100, reinforcement="roulette")[0][1]]
                    else:
                        results += [ag.evolution(popSize=100)[0][1]]

                    mutName = ""

        # Grafs & stats
        if type(method) == list:
            mutName += "roulette_["
            for name in method:
                mutName += name.__name__ + "_"
            mutName = mutName[:-1] + "]"
        else:
            mutName = method.__name__

        dataFolder += mutName + "fit"

        if type(method) == list:
            makeGraf(dataFolder, method)
        else:
            makeGraf(dataFolder, None)

        print(results)
        results = []


    # ag.setIndividualBase(ind_zero_array(ONE_MAX_SIZE))
    # ag.setFitness(fit)
    # ag.setEndCond((ONE_MAX_SIZE, 10000))
    # ag.setSelection(tournamentSelection)
    # ag.setMutation(listeMut, 1)
    # ag.setCrossover(monopoint, 0)
    # ag.setInsertion(ageRemoval)
    #
    # results += [ag.evolution(popSize=100, reinforcement="roulette")[0][1]]
    # print(results)



if __name__ == '__main__':
    main()

