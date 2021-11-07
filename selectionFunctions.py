import random

# Definitions of functions used to select individuals

# Selection functions

def tournamentSelection(population, nbParticipant=5, nbWinners=2):
    """
    Returns the best individuals of a tournament

    :param population: A list of individuals with their fitness
    :param nbParticipant: The number of participant in a tournament
    :param nbWinners: The number of winners of a tournament

    :return: A list of the best participants in the tournament
    """

    participants = random.sample(population, nbParticipant)
    return bestSelection(participants, nbWinners)

def bestSelection(population, nbChosen=2):
    """
    Returns the best individuals

    :param population: A list of individuals with their fitness
    :param nbChosen: The number of individuals chosen

    :return: A list of the best participants
    """

    # Sort by best fitness and randomizes same value fitness
    # sort on fitness with individual[1], if fitness are equals, sort on random numbers
    population.sort(key=lambda individual: (individual[1], random.random()), reverse=True)
    return population[:nbChosen]

def randomSelection(population, nbChosen=2):
    """
    Returns random individuals

    :param population: A list of individuals with their fitness
    :param nbChosen: The number of individuals chosen

    :return: A list of random individuals
    """

    return random.sample([x for x in population], nbChosen)
