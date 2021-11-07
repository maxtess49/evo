from selectionFunctions import *
from insertionFunctions import *

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
    population = [individual]*n
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

    return [(individual, f(individual)) for individual in individuals]

# Selection
def select(selectionProcess, ind): # 2 bests, tournament, 2 randoms
    """
    Function which select the parents of the next generation

    :param selectionProcess: How the parents are selected (tournament, best or random as a string)
    :param ind: A list of individuals with their fitness

    :return: The choosen ones
    """

    if selectionProcess == "tournament":
        return tournamentSelection(ind)

    elif selectionProcess == "best":
        return bestSelection(ind)

    elif selectionProcess == "random":
        return randomSelection(ind)

    else:
        raise Exception("No valid selection process was choosen.")

# Crossover
def crossoverPop(method, p, parents, nbCildren=2):
    """
    Apply crossover between parents to create new children

    :param method: Crossover function to apply
    :param p: Probability of the crossover happening
    :param parents: The newlywed happy couple having a bunch of children

    :return: A list of children or an empty list
    """

    if random.random() < p:
        return method(parents, nbCildren)
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
        return method(ind)
    return []

# Insertion
def insertion(population, children, method):
    """
    Insert newly born children to the population

    :param children: Children to add to the population
    :param population: Population in which we add children as a list
    :param method: Method of removal

    :return: the population
    """

    return method(population)+children

# Function to generate individual, size of pop, fitness function, selection method, crossover method and rate of crossover,
# mutation methods and rate of mutation, insertion method, end condition,
# number of children to generate each crossover, number of individuals to remove on insertion (nbToRemove = none, if = none, = numberOfChildren)
def evolution():
    """
    Main function, make the population evolve

    :return: the best individual
    """
    pass