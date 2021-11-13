from selectionFunctions import *
from insertionFunctions import *
from math import floor

#
#   Ultimately the best would be to have a jupyter notebook to launch instances of the evo algo
#   and several files having all the functions I would need and that I could replace as I wish
#   And at first simply having a main python file that I could toy with until I'm sure my functions are written right
#   Or maybe it's not how it's meant to be
#
#   Ou ptet que ce que je dis c'est de la merde et faut pas faire ça lol

################################################################
# Maybe I should make a class out of this, and keep the population generated as an attribute
# If I decide to do so, I need to remove each "ind" of some functions


#TODO add the data structure of the individuals to generate automatically
def generatePop(n, individual):
    """
    Generate the population

    :param n: The size of the population
    :param individual: A function representing an individual

    :return: A list of individuals
    """

    # We randomize the list in case we use age to remove individuals, as it won't be always the same
    # to be removed (if we use the same list)
    population = []
    for i in range(n):
        population += [individual()]

    random.shuffle(population)
    return population

# Fitness
def fitPop(individuals, f):
    """
    Function calculating the fitness of an individual by applying a fitness function for each

    :param individuals: A list of individuals
    :param f: The function used to calculate the fitness

    :return: A list with the individuals plus their fitness [(individual, fitness)]
    """

    if type(individuals[0]) == tuple:
        population_fitness = [(individual[0], f(individual[0])) for individual in individuals]
    else:
        population_fitness = [(individual, f(individual)) for individual in individuals]

    sum_fitness = 0
    for element in population_fitness:
        sum_fitness += element[1]

    #Calculate first quartile
    firstQuart = (len(population_fitness)+3)/4
    if firstQuart.is_integer():
        firstQuart = population_fitness[int(firstQuart) - 1][1]
    else:
        firstQuart = (population_fitness[int(firstQuart) - 1][1] + population_fitness[int(firstQuart)][1] * 3) / 4

    # Calculate median
    median = (len(population_fitness) + 1) / 2
    if median.is_integer():
        median = population_fitness[int(median) - 1][1]
    else:
        median = (population_fitness[int(median) - 1][1] + population_fitness[int(median)][1]) / 2

    # Calculate third quartile
    thirdQuart = (len(population_fitness) * 3 + 1) / 4
    if thirdQuart.is_integer():
        thirdQuart = population_fitness[int(thirdQuart)-1][1]
    else:
        thirdQuart = (population_fitness[int(thirdQuart) - 1][1] * 3 + population_fitness[int(thirdQuart)][1]) / 4
    return {"population_fitness": population_fitness,
            "min_fit": min(population_fitness, key=lambda fitness:fitness[1])[1],
            "max_fit": max(population_fitness, key=lambda fitness:fitness[1])[1],
            "mean_fit": sum_fitness/len(population_fitness),
            "first_quartile": firstQuart,
            "median":median,
            "third_quartile":thirdQuart}

# Selection
def select(selectionProcess, ind): # 2 bests, tournament, 2 randoms
    """
    Function which select the parents of the next generation

    :param selectionProcess: How the parents are selected (tournament, best or random as a string)
    :param ind: A list of individuals with their fitness

    :return: The choosen ones
    """

    if selectionProcess == "tournament":
        selected = []
        for individual in tournamentSelection(ind):
            selected += [individual[0]]
        return selected

    elif selectionProcess == "best":
        selected = []
        for individual in bestSelection(ind):
            selected += [individual[0]]
        return selected

    elif selectionProcess == "random":
        selected = []
        for individual in randomSelection(ind):
            selected += [individual[0]]
        return selected



    else:
        raise Exception("No valid selection process was choosen.")

# Crossover
def crossoverPop(method, p, parents, nbChildren=2):
    """
    Apply crossover between parents to create new children

    :param method: Crossover function to apply
    :param p: Probability of the crossover happening
    :param parents: The newlywed happy couple having a bunch of children
    :param nbChildren: The number of children the happy couple shall have

    :return: A list of children or an empty list
    """

    if random.random() < p:
        return method(parents, nbChildren)
    return []

#Mutation
def mutatePop(method, p, ind):
    """
    Apply a mutation to a population

    :param method: Mutation function to apply
    :param p: Probability of the mutation happening
    :param ind: Individual population on which the mutation happens

    :return: A list of mutated individuals or an empty list
    """

    if random.random() < p:
        return [method(individual) for individual in ind]
    return []

# Insertion
def insertion(population, children, method, nbToRemove):
    """
    Insert newly born children to the population

    :param children: Children to add to the population
    :param population: Population in which we add children as a list
    :param method: Method of removal
    :param nbToRemove: Number of individuals to remove on insertion

    :return: the population
    """

    return method(population)+children

def evolution(indGeneration, fit, crossoverMethod, mutationMethod, insertionMethod, popSize=200, selectionMethod="tournament", crossoverRate=0.1,
        mutationRate=0.1, endCondition=(None, 100), childrenNbrOnCross = 2, removalNbrOnInsert=None):
    """
    Main function, make the population evolve

    :param indGeneration: Function which generate an individual
    :param fit: Fitness function to get individual performance
    :param crossoverMethod: Crossover function to apply
    :param mutationMethod: Mutation function to apply
    :param insertionMethod: Insertion function to apply

    :param popSize: Size of the population
    :param selectionMethod: Selection function to apply (tournament, best or random as a string)
    :param crossoverRate: Rate of crossovers happening
    :param mutationRate: Rate of mutation
    :param endCondition: End condition of the simulation (As a tuple, (wantedFitness, nmbGeneration))
    :param childrenNbrOnCross: Number of children added made on each crossover
    :param removalNbrOnInsert: Number of individuals to remove on insertion (Default: None, equals childrenNbrOnCross)

    :return: The bestest individual
    """

    population = generatePop(popSize, indGeneration)

    maxFitness = -1
    generation = 0

    # fit
    result = fitPop(population, fit)
    population = result["population_fitness"]
    maxFitness = result["max_fit"]

    while ((endCondition[0] != None and endCondition[0] < maxFitness) or generation < endCondition[1]):
        #select
        parents = select(selectionMethod, population)
        #cross
        children = crossoverPop(crossoverMethod, crossoverRate, parents, childrenNbrOnCross)

        if len(children) > 0:
            #mutate
            children = mutatePop(mutationMethod, mutationRate, children)

            if len(children) > 0:
                children = fitPop(children, fit)["population_fitness"]

                #insert
                if removalNbrOnInsert != None:
                    population = insertion(population, children, insertionMethod, removalNbrOnInsert)
                else:
                    population = insertion(population, children, insertionMethod, childrenNbrOnCross)

        # fit
        result = fitPop(population, fit)
        maxFitness = result["max_fit"]

        generation += 1

    return bestSelection(population, 1)
