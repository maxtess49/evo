from evolution import *
from onemaxFunctions import *

# Main file, used to retrieve parameters from json file and launch the evolution

def main():
    #pop = generatePop(10, ind_zero_array(10))
    #print(pop)
    #print(fitPop(pop, fit))
    #print(tournamentSelection([([0],1),([1],1),([2],0),([3],1),([4],2),([5],2),([6],2)]))
    #print(insertion([0,0,0,0],[1,1,1,1],lambda x: x))
    #print(fitnessRemoval([([0], 1), ([1], 1), ([2], 0), ([3], 1), ([4], 2), ([5], 2), ([6], 2)]))
    #print(uniform([[0,0,0],[1,1,1]],3))

    # Ajouter de quoi calculer le temps pour obtenir un résultat
    # Ajouter la raison de l'arrêt de l'algo, fitness ou max génération ?

    results = []

    for i in range(20):
        results += [evolution(ind_zero_array(100), fit, monopoint, bitFlip, ageRemoval,
                              endCondition=(100, 1000), popSize=20, mutationRate=5, crossoverRate=1)[0][1]]
        print(i)

    print(results)

if __name__ == '__main__':
    main()