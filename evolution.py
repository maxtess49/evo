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
    def _fitPop(self, individuals, f, dataFolderName=None):
        """
        Function calculating the fitness of an individual by applying a fitness function for each

        :param individuals: A list of individuals
        :param f: The function used to calculate the fitness
        :param dataFolderName: The path to the folder in which we write the population datas

        :rtype: dict
        :return: A dict with a list of the individuals plus their fitness, and the highest fit of the population
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
            meanFit = mean([fitness[1] for fitness in population_fitness])
            std_dev = pstdev([fitness[1] for fitness in population_fitness], mu=meanFit)
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

        return method(population)+children

    def _createDataLog(self):
        """
        Create a folder in which we create a json file for the caracteristics of the ga and a csv with the data

        :rtype: str
        :return: The name of the created folder (might remove and make it an attribute)
        """

        characteristics = self.selection_method.__name__ + "_" + self.crossover_method.__name__ + "_" + \
            self.mutation_method.__name__ + "_" + self.fitness_function.__name__

        root_data_files = './data/' + str(self.endCondition) + "/" + "seed_" + str(self.seed) + "/"
        data_folder = root_data_files + characteristics + "/"

        if not os.path.exists(data_folder):
            os.makedirs(data_folder)

        json_file = open(data_folder + 'parameters.json', "w")
        parameters = {
            "selection_method": self.selection_method.__name__,
            "crossover_method": self.crossover_method.__name__,
            "crossover_rate": self.crossover_rate,
            "mutation_method": self.mutation_method.__name__,
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
        writer.writerow(["min_fitness", "max_fitness", "mean", "standard_deviation",
                         "nbrCrossovers", "nbrMutation", "probMutation"])
        csv_file.close()

        return data_folder

    # Main method of ga, Darwin would be proud
    def evolution(self, popSize=200):
        """
        Main function, make the population evolve
        Generate a csv file with data about the population and
        a json file with the parameters of the model in a "data" folder

        :param popSize: Size of the population

        :rtype: list
        :return: The bestest individual
        """
        random.seed(self.seed)

        population = self._generatePop(popSize, self.ind_generation)

        generation = 0

        # Create a folder to put the data
        data_folder = self._createDataLog()

        # Stats
        nbrMut = []
        nbrCross = []

        # fit
        result = self._fitPop(population, self.fitness_function, data_folder)
        population = result["population_fitness"]
        maxFitness = result["max_fit"]

        while (self.endCondition[0] is not None and self.endCondition[0] > maxFitness) and (generation < self.endCondition[1]):
            # select
            parents = self._select(self.selection_method, population)
            children = None
            # cross
            if random.random() < self.crossover_rate:
                children = self._crossoverPop(self.crossover_method, parents)

            # mutate
            # Rajouter un paramètre pour dire si on garde que améliorant ou pas (dans ce cas, créer un clone des enfants pour tester dessus, on jette si c'est inférieur)
            if random.random() < self.mutation_rate:
                if children is not None:
                    children = self._mutatePop(self.mutation_method, children)
                else:
                    parents = self._mutatePop(self.mutation_method, [parents[0][0], parents[1][0]])

            # insert
            if children is not None:
                children = self._fitPop(children, self.fitness_function)["population_fitness"]
                population = self._insertion(population, children, self.insertion_method)

            # fit
            result = self._fitPop(population, self.fitness_function, data_folder)
            maxFitness = result["max_fit"]

            generation += 1

        return bestSelection(population, 1)


# Notes à moi même, ce que je peux faire pour compter les méthodes, c'est juste garder une variable que j'incrémente à chaque fois qu'un appel est passé
# Et pour la roulette, au lieu d'utiliser un int, j'utilise un tableau, et j'incrémente là où il faut, puis pour ajouter dans le csv
# Je mets juste dans le header le nom de la fonction utilisée, et je me débrouille pour que si c'est la roulette, je mets les méthodes de la roulettes séparées par des ;
# et pour mettre le nombre d'utilisation des méthodes de la roulette, je mets chaque valeur du tableau séparées par des ; aussi

# Peut être que je dois garder la proba aussi pour les méthodes de la roulette ?

# Compter nombre de cross / de mutations et de fitness ?
