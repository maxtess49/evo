# Generation of individuals
def ind_zero_array(n):
    """
    Generate an individual as an array of int with size n, populated with zeros

    :param n: The size of the array

    :return: The individual
    """

    return ([0]*n)

##TODO add a function to create random zeros and ones individuals

# Function to calculate the fitness of an individual
def fit(individual):
    """
    Calculate a score for the individual (the more ones the better)

    :param individual: An individual to test

    :return: The score of the individual
    """

    return individual.count(1)

# Crossover functions
def monopoint(parents, nbChildren):
    """
    Use monopoint crossover on parents to make children

    :param parents: A list of parents
    :param nbChildren: The number of children to make

    :return: A list of children
    """

    pass

def uniform(parents, nbChildren):
    """
    Use uniform crossover on parents to make children

    :param parents: A list of parents
    :param nbChildren: The number of children to make

    :return: A list of children
    """

    pass

# Mutation functions
def bitFlip(ind):
    """


    :param ind:
    :return:
    """
    pass

def oneFlip(ind):
    pass

def threeFlip(ind):
    pass

def fiveFlip(ind):
    pass