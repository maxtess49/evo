def ind_zero_array(n):
    """
    Generate an individual as an array of int with size n, populated with zeros

    :param n: The size of the array

    :return: The individual
    """

    return ([0]*n)

##TODO add a function to create random zeros and ones individuals

def fit(individual):
    """
    Calculate a score for the individual (the more ones the better)

    :param individual: An individual to test

    :return: The score of the individual
    """

    return individual.count(1)

# Crossover functions
def cMonopoint():
    pass

def cUniform():
    pass

# Mutation functions
def mBitFlip():
    pass

def mOneFlip():
    pass

def mThreeFlip():
    pass

def mFiveFlip():
    pass