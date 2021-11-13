import random

# Generation of individuals
def ind_zero_array(n):
    """
    Generate an individual as an array of int with size n, populated with zeros

    :param n: The size of the array

    :return: The individual
    """

    return lambda : ([0]*n)

##TODO add a function to create random zeros and ones individuals

# Function to calculate the fitness of an individual
def fit(individual):
    """
    Calculate a score for the individual (the more ones the better)

    :param individual: An individual to test (A list of int either 1 or 0)

    :return: The score of the individual
    """

    return individual.count(1)

# Crossover functions
def monopoint(parents, nbChildren=2):
    """
    Use monopoint crossover on parents to make children
    (Cut the pool of genes from parents in a point and create child by taking a part from each parent)

    :param parents: A list of two parents
    :param nbChildren: The number of children to make

    :return: A list of children
    """

    children = []

    while len(children) < nbChildren:
        cut = random.randint(1, len(parents[0])-1)
        children += [parents[0][cut:]+parents[1][:cut]]
        children += [parents[1][cut:]+parents[0][:cut]]
    if len(children) > nbChildren:
        random.shuffle(children)
        children = children[:nbChildren]

    return children

def uniform(parents, nbChildren=2, p=0.5):
    """
    Use uniform crossover on parents to make children
    (Each gene as a probability to come from either parent)

    :param parents: A list of two parents
    :param nbChildren: The number of children to make
    :param p: Probability to take first parent genes rather than second parent ones

    :return: A list of children
    """

    children = []
    while len(children) < nbChildren:
        child = [0]*len(parents[0])
        for i in range(len(child)):
            if random.random() < p:
                child[i] = parents[0][i]
            else:
                child[i] = parents[1][i]
        children += [child]

    return children

# Mutation functions
def bitFlip(ind):
    """
    Mutate the individual by flipping a gene (each gene has 1/length of individual chance to be mutated)

    :param ind: The individual to mutate

    :return: The mutated individual
    """

    for i in range(len(ind)):
        if random.random() < 1/len(ind):
            if ind[i] == 1:
                ind[i] = 0
            else:
                ind[i] = 1

    return ind

def numBitFlip(ind, numGenesFlip):
    """
    Mutate the individual by flipping random genes

    :param ind: The individual to mutate
    :param numGenesFlip: Number of genes to flip (1, 3, 5 flip)

    :return: The mutated individual
    """

    bitsToFlip = random.sample(range(len(ind)), numGenesFlip)
    for i in bitsToFlip:
        if ind[i] == 1:
            ind[i] = 0
        else:
            ind[i] = 1

    return ind

def oneFlip(ind):
    """
    Mutate the individual by flipping a random genes

    :param ind: The individual to mutate

    :return: The mutated individual
    """

    return numBitFlip(ind, 1)

def threeFlip(ind):
    """
    Mutate the individual by flipping three random genes

    :param ind: The individual to mutate

    :return: The mutated individual
    """

    return numBitFlip(ind, 3)

def fiveFlip(ind):
    """
    Mutate the individual by flipping five random genes

    :param ind: The individual to mutate

    :return: The mutated individual
    """

    return numBitFlip(ind, 5)