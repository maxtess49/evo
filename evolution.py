from selectionFunctions import *
from insertionFunctions import *
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
            parameters = json.loads(json_file)
            self.selection_method = parameters["selection_method"]
            self.crossover_method = parameters["crossover_method"]
            self.crossover_rate = parameters["crossover_rate"]
            self.mutation_method = parameters["mutation_method"]
            self.mutation_rate = parameters["mutation_rate"]
            self.insertion_method = parameters["insertion_method"]
            self.endCondition = (parameters["endCondition"][0], parameters["endCondition"][1])
            self.fitness_function = parameters["fitness_function"]
            self.seed = parameters["seed"]
        else:
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
    def _fitPop(self, individuals, f, dataFolderName=None):
        """
        Function calculating the fitness of an individual by applying a fitness function for each

        :param individuals: A list of individuals
        :param f: The function used to calculate the fitness
        :param dataFolderName: The path to the folder in which we write the population datas

        :return: A list with the individuals plus their fitness [(individual, fitness)]
        """

        if type(individuals[0]) == tuple:
            population_fitness = [(individual[0], f(individual[0])) for individual in individuals]
        else:
            population_fitness = [(individual, f(individual)) for individual in individuals]

        maxFit = max(population_fitness, key=lambda fitness: fitness[1])[1]

        if dataFolderName is not None:
            sum_fitness = 0
            for element in population_fitness:
                sum_fitness += element[1]

            # Calculate a bunch of sophisticated (or not) stats
            meanFit = mean([fit[1] for fit in population_fitness])
            std_dev = pstdev([fit[1] for fit in population_fitness], mu=meanFit)
            minFit = min(population_fitness, key=lambda fitness: fitness[1])[1]

            # Write to csv
            csv_file = open(dataFolderName+"/data.csv", "a", encoding="UTF8", newline="")
            writer = csv.writer(csv_file)
            writer.writerow([str(minFit), str(maxFit), str(meanFit), str(std_dev)])
            csv_file.close()

        return {"population_fitness": population_fitness, "max_fit": maxFit}

    # Selection
    def _select(self, selectionProcess, ind):  # 2 bests, tournament, 2 randoms
        """
        Function which select the parents of the next generation

        :param selectionProcess: How the parents are selected (tournament, best or random as a string)
        :param ind: A list of individuals with their fitness

        :return: The choosen ones
        """

        return selectionProcess(ind)

    # Crossover
    def _crossoverPop(self, method, parents):
        """
        Apply crossover between parents to create new children

        :param method: Crossover function to apply
        :param parents: The newlywed happy couple having a bunch of children

        :return: A list of children or an empty list
        """

        return method(parents)

    # Mutation
    def _mutatePop(self, method, ind):
        """
        Apply a mutation to a population

        :param method: Mutation function to apply
        :param ind: Individual population on which the mutation happens

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

        :return: the population
        """

        return method(population)+children

    def _createDataLog(self):
        """
        Create a folder in which we create a json file for the caracteristics of the ga and a csv with the data

        :return: nothing
        """

        characteristics = self.selection_method + "_" + self.crossover_method.__name__ + "_" + \
            self.mutation_method.__name__ + "_" + self.fitness_function.__name__

        root_data_files = './data/'+str(self.endCondition)+"/"
        this_data_folder = root_data_files + characteristics + "/"

        if not os.path.exists(this_data_folder):
            os.makedirs(this_data_folder)

        json_file = open(this_data_folder + '/parameters.json', "w")
        parameters = {
            "selection_method": self.selection_method,
            "crossover_method": self.crossover_method.__name__,
            "crossover_rate": self.crossover_rate,
            "mutation_method": self.mutation_method.__name__,
            "mutation_rate": self.mutation_rate,
            "endCondition": self.endCondition,
            "fitness_function": self.fitness_function.__name__
        }
        json_file.write(json.dumps(parameters))
        json_file.close()

        csv_file = open(this_data_folder + "/data.csv", "w", encoding="UTF8", newline="")
        writer = csv.writer(csv_file)
        # Write header
        writer.writerow(["min_fitness", "max_fitness", "mean", "standart_deviation"])
        csv_file.close()

        return this_data_folder

    # Main method of ga, Darwin would be proud
    def evolution(self, indGeneration, fit, crossoverMethod, mutationMethod, insertionMethod, popSize=200,
                  selectionMethod="tournament", endCondition=(None, 100)):
        """
        Main function, make the population evolve
        Generate a csv file with data about the population

        :param indGeneration: Function which generate an individual
        :param fit: Fitness function to get individual performance
        :param crossoverMethod: Crossover function to apply
        :param mutationMethod: Mutation function to apply
        :param insertionMethod: Insertion function to apply

        :param popSize: Size of the population
        :param selectionMethod: Selection function to apply (tournament, best or random as a string)
        :param endCondition: End condition of the simulation (As a tuple, (wantedFitness, nmbGeneration))

        :return: The bestest individual
        """

        random.seed(self.seed)

        population = self._generatePop(popSize, indGeneration)

        generation = 0

        # Create a folder to put the data
        data_folder = self._createDataLog()

        # fit
        result = self._fitPop(population, fit, data_folder)
        population = result["population_fitness"]
        maxFitness = result["max_fit"]

        # TODO check that it works the way it was intended, I might be dumb
        while ((endCondition[0] is not None and endCondition[0] < maxFitness) or (generation < endCondition[1])):
            # select
            parents = self._select(selectionMethod, population)
            # cross
            if random.random() < self.crossover_rate:
                children = self._crossoverPop(crossoverMethod, parents)

                # mutate
                if random.random() < self.mutation_rate:
                    children = self._mutatePop(mutationMethod, children)

                children = self._fitPop(children, fit)["population_fitness"]

                # insert
                population = self._insertion(population, children, insertionMethod)

            # fit
            result = self._fitPop(population, fit, data_folder)
            maxFitness = result["max_fit"]

            generation += 1

        return bestSelection(population, 1)


# Notes à moi même, ce que je peux faire pour compter les méthodes, c'est juste garder une variable que j'incrémente à chaque fois qu'un appel est passé
# Et pour la roulette, au lieu d'utiliser un int, j'utilise un tableau, et j'incrémente là où il faut, puis pour ajouter dans le csv
# Je mets juste dans le header le nom de la fonction utilisée, et je me débrouille pour que si c'est la roulette, je mets les méthodes de la roulettes séparées par des ;
# et pour mettre le nombre d'utilisation des méthodes de la roulette, je mets chaque valeur du tableau séparées par des ; aussi

# Peut être que je dois garder la proba aussi pour les méthodes de la roulette ?

# Compter nombre de cross / de mutations et de fitness ?