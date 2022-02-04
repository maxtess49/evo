import copy

from selectionFunctions import *
from insertionFunctions import *
from onemaxFunctions import *
from reinforcmentLearning import *
import os
import csv
import json
from statistics import pstdev, mean


#
# Author: Maxence Marot
#
# last update 25/01/22
#


class GeneticAlgorithm:

    def __init__(self, json_file=None):
        if json_file is not None:
            file = open(json_file)
            parameters = json.load(file)
            self.ind_generation = globals()[parameters["ind_generation"]]
            self.selection_method = globals()[parameters["selection_method"]]
            self.crossover_method = globals()[parameters["crossover_method"]]
            self.crossover_rate = parameters["crossover_rate"]
            self.mutation_method = globals()[parameters["mutation_method"]]
            self.mutation_rate = parameters["mutation_rate"]
            self.insertion_method = globals()[parameters["insertion_method"]]
            self.endCondition = (parameters["endCondition"][0], parameters["endCondition"][1])
            self.fitness_function = globals()[parameters["fitness_function"]]
            self.seed = parameters["seed"]
            file.close()
        else:
            self.ind_generation = None
            self.selection_method = None
            self.crossover_method = None
            self.crossover_rate = None
            self.mutation_method = None
            self.mutation_rate = None
            self.insertion_method = None
            self.endCondition = None
            self.fitness_function = None
            self.seed = None

    # Setters
    def setIndividualBase(self, ind_generation):
        self.ind_generation = ind_generation

    def setSelection(self, method):
        self.selection_method = method

    def setCrossover(self, method, prob=None):
        self.crossover_method = method
        if prob is not None:
            self.crossover_rate = prob

    def setMutation(self, method, prob=None):
        self.mutation_method = method
        if prob is not None:
            self.mutation_rate = prob

    def setInsertion(self, method):
        self.insertion_method = method

    def setFitness(self, method):
        self.fitness_function = method

    def setEndCond(self, endCond):
        self.endCondition = endCond

    def setSeed(self, seed):
        self.seed = seed
        random.seed(seed)

    def _generatePop(self, n, individual):
        """
        Generate the population

        :param n: The size of the population
        :param individual: A function representing an individual

        :rtype: list
        :return: A list of individuals
        """

        # We randomize the list in case we use age to remove individuals, as it won't be always the same
        # to be removed (if we use the same list)
        population = []
        for i in range(n):
            population += [individual()]

        random.shuffle(population)
        return population

    # Fitness
    def _fitPop(self, individuals, f):
        """
        Function calculating the fitness of an individual by applying a fitness function for each

        :param individuals: A list of individuals
        :param f: The function used to calculate the fitness

        :rtype: dict
        :return: A dict with a list of the individuals plus their fitness, and the highest fit of the population
        """

        if type(individuals[0]) == tuple:
            population_fitness = [(individual[0], f(individual[0])) for individual in individuals]
        else:
            population_fitness = [(individual, f(individual)) for individual in individuals]

        return population_fitness

    # Selection
    def _select(self, selectionProcess, ind):  # 2 bests, tournament, 2 randoms
        """
        Function which select the parents of the next generation

        :param selectionProcess: How the parents are selected (tournament, best or random as a string)
        :param ind: A list of individuals with their fitness

        :rtype: list
        :return: The choosen ones
        """

        return selectionProcess(ind)

    # Crossover
    def _crossoverPop(self, method, parents):
        """
        Apply crossover between parents to create new children

        :param method: Crossover function to apply
        :param parents: The newlywed happy couple having a bunch of children

        :rtype: list
        :return: A list of children or an empty list
        """

        return method([parents[0][0], parents[1][0]])

    # Mutation
    def _mutatePop(self, method, ind):
        """
        Apply a mutation to a population

        :param method: Mutation function to apply
        :param ind: Individual population on which the mutation happens

        :rtype: list
        :return: A list of mutated individuals or an empty list
        """

        return [method(individual) for individual in ind]

    # Insertion
    def _insertion(self, population, children, method):
        """
        Insert newly born children to the population

        :param children: Children to add to the population
        :param population: Population in which we add children as a list
        :param method: Method of removal

        :rtype: list
        :return: the population
        """

        return method(population) + children

    def _createDataLog(self):
        """
        Create a folder in which we create a json file for the caracteristics of the ga and a csv with the data

        :rtype: str
        :return: The name of the created folder (might remove and make it an attribute)
        """

        mutName = ""
        if type(self.mutation_method) == list:
            mutName += "roulette_["
            for name in self.mutation_method:
                mutName += name.__name__ + "_"
            mutName = mutName[:-1] + "]"
        else:
            mutName = self.mutation_method.__name__

        characteristics = self.selection_method.__name__ + "_" + self.crossover_method.__name__ + "_" + \
                           mutName + self.fitness_function.__name__

        root_data_files = './data/' + str(self.endCondition) + "/" + "seed_" + str(self.seed) + "/"
        data_folder = root_data_files + characteristics + "/"

        if not os.path.exists(data_folder):
            os.makedirs(data_folder)

        json_file = open(data_folder + 'parameters.json', "w")
        parameters = {
            "selection_method": self.selection_method.__name__,
            "crossover_method": self.crossover_method.__name__,
            "crossover_rate": self.crossover_rate,
            "mutation_method": mutName,
            "mutation_rate": self.mutation_rate,
            "endCondition": self.endCondition,
            "fitness_function": self.fitness_function.__name__,
            "seed": self.seed
        }
        json_file.write(json.dumps(parameters))
        json_file.close()

        csv_file = open(data_folder + "/data.csv", "w", encoding="UTF8", newline="")
        writer = csv.writer(csv_file)
        # Write header
        writer.writerow(["generation", "min_fitness", "max_fitness", "mean", "standard_deviation",
                         "methodsHistory", "probOpe", "improvement"])
        csv_file.close()

        return data_folder

    def _writeToDataLog(self, population, dataFolder, generation, opHistory=None, probaList=None, imp=None):
        """
        Write data to log for stats & graphs

        :param population: The current population of the AG
        :param dataFolder: The folder in which we write
        :param generation: Current generation
        :param opHistory: Number of time each method was called
        :param probaList: Evolution of the probability of use of each method
        """
        sum_fitness = 0
        for element in population:
            sum_fitness += element[1]

        # Calculate a bunch of sophisticated (or not) stats
        meanFit = mean([fitness[1] for fitness in population])
        std_dev = pstdev([fitness[1] for fitness in population], mu=meanFit)
        minFit = min(population, key=lambda fitness: fitness[1])[1]
        maxFit = max(population, key=lambda fitness: fitness[1])[1]

        # Write to csv
        csv_file = open(dataFolder + "/data.csv", "a", encoding="UTF8", newline="")
        writer = csv.writer(csv_file)
        writer.writerow([str(generation), str(minFit), str(maxFit), str(meanFit), str(std_dev),
                         str(opHistory), str(probaList), str(imp)])
        csv_file.close()

    # Main method of ga, Darwin would be proud
    def evolution(self, popSize=200, reinforcement=None, historySize=10, pmin=0.05, keepImproved=True):
        """
        Main function, make the population evolve
        Generate a csv file with data about the population and
        a json file with the parameters of the model in a "data" folder

        :param popSize: Size of the population
        :param reinforcement: Method of reinforcement to use, None if there is none
        :param historySize: Size of history used for the reinforcement
        :param pmin: Min probability of a method for reinforcement wheel
        :param keepImproved: True if we keep only the improved mutants, False otherwise

        :rtype: list
        :return: The bestest individual
        """
        random.seed(self.seed)

        population = self._generatePop(popSize, self.ind_generation)

        generation = 0

        # Create a folder to put the data
        data_folder = self._createDataLog()

        # Stats
        taille = 0
        if type(self.mutation_method) == list and reinforcement is not None:
            taille = len(self.mutation_method)
        rewardList = [0 for i in range(taille)]
        rewardHistory = [[0] for i in range(taille)]
        probaList = [1 / taille for i in range(taille)]
        opHistory = [0 for i in range(taille)]
        nbrMut = []

        # fit
        population = self._fitPop(population, self.fitness_function)
        maxFitness = max(population, key=lambda fitness: fitness[1])[1]

        while (self.endCondition[0] is not None and self.endCondition[0] > maxFitness) \
                and (generation < self.endCondition[1]):

            generation += 1

            # Reinforcment
            currentOpe = -1
            if reinforcement is not None:
                currentOpe = select_op(probaList)
                if currentOpe != -1:
                    nbrMut.append(self.mutation_method[currentOpe])

            # select
            parents = self._select(self.selection_method, population)
            children = None
            # cross
            if random.random() < self.crossover_rate:
                children = self._crossoverPop(self.crossover_method, parents)
            else:
                children = (copy.deepcopy(parents[0][0]), copy.deepcopy(parents[1][0]))

            # Fitness for utility
            initialFitnessP1 = parents[0][1]
            initialFitnessP2 = parents[1][1]
            newFitnessC1 = 0
            newFitnessC2 = 0

            # mutate
            if random.random() < self.mutation_rate:
                mutation_m = self.mutation_method
                if reinforcement is not None:
                    mutation_m = self.mutation_method[currentOpe]

                children = self._mutatePop(mutation_m, children)

            # Fitness calculus
            children = self._fitPop(children, self.fitness_function)
            newFitnessC1 = children[0][1]
            newFitnessC2 = children[1][1]

            # MAJ des utilités
            # For the improvement, we use the mean of the fitness
            imp = improvement((initialFitnessP1 + initialFitnessP2) / 2, (newFitnessC1 + newFitnessC2) / 2)
            update_reward_sliding(rewardList, rewardHistory, historySize, currentOpe, imp)


            # MAJ roulette
            update_roulette_wheel(rewardList, probaList, pmin)

            # insert
            if keepImproved:
                if imp > 0:
                    population = self._insertion(population, children, self.insertion_method)
            else:
                population = self._insertion(population, children, self.insertion_method)

            maxFitness = max(population, key=lambda fitness: fitness[1])[1]

            for o in range(len(self.mutation_method)):
                if o == currentOpe:
                    opHistory[o] += 1

            print(generation)
            print(rewardList)
            print(rewardHistory)
            print(probaList)
            print("------------")
            self._writeToDataLog(population, data_folder, generation, opHistory, probaList, imp)

        return bestSelection(population, 1)
