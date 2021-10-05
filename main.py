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


# Generate the population
# n - The size of the population
def generatePop(n):
    pass

# Function calculating the fitness of an individual by applying a fitness function for each
# ind - The list of individuals
# f - The function used to calculate the fitness
# return the fitness of the individual (need to decide how it's represented)
def fit(ind, f):
    pass

# Function which select the parents of the next generation
# selectionProcess - How the parents are selected (tournament, best, random) (as a function ?)
# ind - The individuals
def select(selectionProcess, ind):
    pass

# Apply crossover between parents to create new child
# method - Crossover method to apply (monopoint, uniform) (as a function ?)
# p - Probability of the crossover happening
# parents - The newlywed happy couple having a bunch of children
def crossover(method, p, parents):
    pass

# Apply a mutation to an individual
# method - Mutation method to apply (bitflip / 1 flip / 3 flip / 5 flip) (as a function ?)
# p - Probability of the mutation happening
# ind - Individual on which the mutation happens
def mutation(method, p, ind):
    pass

# Create a new generation by selecting 2 parents and creating children whith crossover & mutation
# Attributes ?
def createNewGen():
    pass


#
#
def main():
    pass

if __name__ == "__main__":
    main()
