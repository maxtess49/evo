from evolution import *
from onemaxFunctions import *

# Main file, used to retrieve parameters from json file and launch the evolution

def main():
    pop = generatePop(10, ind_zero_array(10))
    print(pop)
    print([x[1] for x in fitPop(pop, fit)])
    print(tournamentSelection([([0],1),([1],1),([2],0),([3],1),([4],2),([5],2),([6],2)]))
    print(insertion([0,0,0,0],[1,1,1,1],lambda x: x))

    print(fitnessRemoval([([0], 1), ([1], 1), ([2], 0), ([3], 1), ([4], 2), ([5], 2), ([6], 2)]))

if __name__ == '__main__':
    main()