import random

# Definitions of functions used to select individuals

# Selection functions

def tournamentSelection(individualsFit, nbParticipant=5, nbWinners=2):
    """
    Returns the best individuals of a tournament

    :param individualsFit: A list of individuals with their fitness
    :param nbParticipant: The number of participant in a tournament
    :param nbWinners: The number of winners of a tournament

    :return: A list of the best participants in the tournament
    """

    participants = random.sample(individualsFit, nbParticipant)
    return bestSelection(participants, nbWinners)

def bestSelection(individualsFit, nbChosen=2):
    """
    Returns the best individuals

    :param individualsFit: A list of individuals with their fitness
    :param nbChosen: The number of individuals chosen

    :return: A list of the best participants
    """

    # Sort by best fitness and randomizes same value fitness
    # sort on fitness with individual[1], if fitness are equals, sort on random numbers
    individualsFit.sort(key=lambda individual: (individual[1], random.random()), reverse=True)
    return individualsFit[:nbChosen]

def randomSelection(individualsFit, nbChosen=2):
    """
    Returns random individuals

    :param individualsFit: A list of individuals with their fitness
    :param nbChosen: The number of individuals chosen

    :return: A list of random individuals
    """

    return random.sample([x[0] for x in individualsFit], nbChosen)
