from evolution import *
from onemaxFunctions import *

def main():
    pop = generatePop(10, ind_zero_array(10))
    print([x[1] for x in fitPop(pop, fit)])
    print(tournamentSelection([([0],1),([1],1),([2],0),([3],1),([4],2),([5],2),([6],2)]))

if __name__ == '__main__':
    main()