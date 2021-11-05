from evolution import *
from evolutionaryFunctions import *
from onemaxFunctions import *

def main():
    pop = generatePop(10, ind_zero_array(10))
    print(fitPop(pop, fit))

if __name__ == '__main__':
    main()