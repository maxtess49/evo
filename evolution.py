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
def generatePop(n):
    """
    Generate the population

    :param n: The size of the population

    :return: ?
    """

    pass

def fit(ind, f):
    """
    Function calculating the fitness of an individual by applying a fitness function for each

    :param ind: The list of individuals
    :param f: The function used to calculate the fitness

    :return: the fitness of the individual (need to decide how it's represented)
    """

    pass

def select(selectionProcess, ind):
    """
    Function which select the parents of the next generation

    :param selectionProcess: How the parents are selected (tournament, best, random) (as a function ?)
    :param ind: The individuals

    :return:
    """
    pass

def crossover(method, p, parents):
    """
    Apply crossover between parents to create new child

    :param method: Crossover method to apply (monopoint, uniform) (as a function ?)
    :param p: Probability of the crossover happening
    :param parents: The newlywed happy couple having a bunch of children

    :return: ?
    """
    pass

def mutation(method, p, ind):
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


