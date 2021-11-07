import random

def ageRemoval(pop, nbToRemove=2):
    """
    Remove the older individuals

    :param pop: The list of the population
    :param nbToRemove: The number of individuals to remove

    :return: The population minus the older individuals
    """

    return pop[nbToRemove:]

def fitnessRemoval(pop, nbToRemove=2):
    """
    Remove the worst individuals

    :param pop: The list of the population
    :param nbToRemove: The number of individuals to remove

    :return: The population minus the worst individuals
    """

    pop.sort(key=lambda individual: (individual[1], random.random()))
    return pop[nbToRemove:]