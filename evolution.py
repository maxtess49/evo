from selectionFunctions import *

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

    :return: ?
    """

    return ([individual]*n)

# Fitness
def fitPop(individuals, f):
    """
    Function calculating the fitness of an individual by applying a fitness function for each

    :param individuals: An array of individuals
    :param f: The function used to calculate the fitness

    :return: An array with the individuals plus their fitness [(individual, fitness)]
    """

    return [(individual, f(individual)) for individual in individuals]

def select(selectionProcess, ind): # 2 bests, tournament, 2 randoms
    """
    Function which select the parents of the next generation

    :param selectionProcess: How the parents are selected (tournament, best or random as a string)
    :param ind: An array of individuals with their fitness

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

def crossoverPop(method, p, parents):
    """
    Apply crossover between parents to create new child

    :param method: Crossover method to apply (monopoint, uniform) (as a function ?)
    :param p: Probability of the crossover happening
    :param parents: The newlywed happy couple having a bunch of children

    :return: ?
    """
    pass

def mutatePop(method, p, ind):
    """
    Apply a mutation to an individual

    :param method: Mutation method to apply (bitflip / 1 flip / 3 flip / 5 flip) (as a function ?)
    :param p: Probability of the mutation happening
    :param ind: Individual on which the mutation happens

    :return: ?
    """
    pass

# Attributes ?
def createNewGen():
    """
    Create a new generation by selecting 2 parents and creating children whith crossover & mutation

    :return: ?
    """
    pass

# Function to generate individual, size of pop, fitness function, selection method, crossover method or probabilities for crossover,
# mutation method or probabilities for mutation, insertion method
def evolution():
    """
    Main function, make the population evolve

    :return: the best individual
    """
    pass