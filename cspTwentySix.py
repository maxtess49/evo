import random
from collections import Counter
import itertools
from copy import deepcopy

# Tournament model and functions for fitness, crossovers & mutations (local search)
# Each tournament is created to respect two constraints:
# - Each team has only one match per week
# - Each possible match is played once
#
# We only need to work on the periods
from evolution import generatePop, evolution


class Tournament:
    def __init__(self, numberOfTeams=6, schedule=[]):
        self.nbrTeams = numberOfTeams
        self.nbrWeeks = numberOfTeams-1
        self.nbrPeriods = int(numberOfTeams/2)
        if schedule == []:
            self.schedule = self.makeSchedule()
        else:
            self.schedule = schedule

    def __str__(self):
        #return str(self.schedule)
        length_list = [len(element) for row in self.schedule for element in row]
        column_width = max(length_list)
        stringTable = " "*10+"1"
        for i in range(2, int(self.nbrTeams/2+1)):
            stringTable += " "*(11-(len(str(i))-1))+str(i)
        stringTable+= "\n"
        week = 1
        for row in self.schedule:
            row = "".join(str(element).ljust(column_width + 7)+" | " for element in row)
            stringTable += str(week).ljust(column_width + 2) + " | " +row + "\n"
            week += 1

        return stringTable

    def makeSchedule(self):
        """
        Makes a schedule with all matches being different
        and with all teams playing only once per week

        For each match from (1,nbrTeams-1) to (nbrTeams-2,nbrTeams-1) we assign a week that way:
        Team y and team y+1 on week y
        Then for each team team y has to do a match against,
            we assign y+nbrTeams/2, and then y-nbrTeams/2-1 until all matches of y are assigned

        For the last team, we assign the remaining week of the first team to 1-lastTeam, and increment it for each match of lastTeam

        :return: The schedule for the tournament as list of lists
        """

        # Create all the different matches that can be played
        matchs = []
        for firstTeam in range(1, self.nbrTeams):
            for secondTeam in range(firstTeam+1, self.nbrTeams):
                matchs += [(firstTeam, secondTeam)]

        # Assign a week for each match
        baseOddWeek = 1
        baseEvenWeek = int(1 + self.nbrTeams/2)
        countOddWeek = baseOddWeek
        countEvenWeek = baseEvenWeek

        oddWeek = True

        team = 1

        weeks = []
        firstTeamWeek = -1

        for match in matchs:
            if team != match[0]:
                baseOddWeek += 1
                baseEvenWeek += 1
                countOddWeek = baseOddWeek
                countEvenWeek = baseEvenWeek

                team = match[0]
                oddWeek = True

            if oddWeek:
                weeks += [(countOddWeek, match)]

                # Keep last week added to team one to add all of last team weeks later
                if team == 1:
                    firstTeamWeek = countOddWeek

                countOddWeek += 1
                oddWeek = False

            else:
                weeks += [(countEvenWeek, match)]

                # Keep last week added to team one to add all of last team weeks later
                if team == 1:
                    firstTeamWeek = countEvenWeek

                countEvenWeek += 1
                oddWeek = True

            # If the week is not in schedule, back to the first
            if countOddWeek > self.nbrTeams - 1:
                countOddWeek -= self.nbrTeams - 1
            if countEvenWeek > self.nbrTeams - 1:
                countEvenWeek -= self.nbrTeams - 1


        # Add weeks of matches of the last team
        firstTeamWeek -= int(self.nbrTeams / 2 - 1)
        weeks += [(firstTeamWeek, (1, self.nbrTeams))]
        for team in range (2, self.nbrTeams):
            firstTeamWeek += 1
            if firstTeamWeek > self.nbrTeams -1:
                firstTeamWeek -= self.nbrTeams - 1
            weeks += [(firstTeamWeek, (team, self.nbrTeams))]

        schedule = []
        # Sort the matches by week and assign a random period
        for week in range(1, self.nbrTeams):
            matchsPerWeek = [match[1] for match in weeks if match[0] == week]
            # Shuffle to have different periods for match among every tournaments
            random.shuffle(matchsPerWeek)
            schedule += [(matchsPerWeek)]

        return schedule


# Generation of individuals
def tournamentGeneration():
    """
    Create random tournaments

    :return: a random tournament
    """

    return Tournament()

# Fitness
def fit(individual):
    """
    Calculate a score for a tournament (contrary of the sum of excess occurrence of each team per period (contrary to keep the best fit high))

    :param individual: An individual to test (a tournament)

    :return: The score of an individual
    """

    countFit = 0
    for j in range(individual.nbrPeriods):
        liste = list(itertools.chain.from_iterable([i[j] for i in individual.schedule]))

        for k in Counter(liste).items():
            if k[1] > 2:
                countFit += k[1] - 2

    return -countFit

# Crossover
def monopointWeek(parents, nbChildren=2):
    children = []

    while len(children) < nbChildren:
        cut = random.randint(1, parents[0].nbrWeeks-1)
        children += [Tournament(parents[0].nbrTeams, deepcopy([parents[0].schedule[i] for i in range(0, cut)] + [parents[1].schedule[i] for i in range(cut, parents[0].nbrWeeks)]))]
        children += [Tournament(parents[0].nbrTeams, deepcopy([parents[1].schedule[i] for i in range(0, cut)] + [parents[0].schedule[i] for i in range(cut, parents[0].nbrWeeks)]))]

    if len(children) > nbChildren:
        random.shuffle(children)
        children = children[:nbChildren]

    return children

def uniformWeek(parents, nbChildren=2, p=0.5):
    children = []
    while len(children) < nbChildren:
        newSchedule = []
        for i in range(parents[0].nbrWeeks):
            if random.random() < p:
                newSchedule += [parents[0].schedule[i]]
            else:
                newSchedule += [parents[1].schedule[i]]

        child = Tournament(parents[0].nbrTeams, newSchedule)
        children += [child]

    return children


# Mutations (local search so as to have a memetic algorithm)
def simulatedAnnealing():
    pass

def tabuSearch(individual, maxSize = 100, repetitions=1000):
    best = individual
    bestCandidate = ()
    tabuList = [individual.schedule]
    fitBest = fit(individual)
    nbrNotImproved = 0
    for i in range(repetitions):
        # Bestest
        if fitBest == 0:
            #return best
            return best

        neighborhood = generateNeighbors(best)
        bestCandidate = neighborhood[0]

        for candidate in neighborhood:
            if fit(bestCandidate) < fit(candidate) and candidate.schedule not in tabuList:
                bestCandidate = candidate

        newFit = fit(bestCandidate)
        if newFit > fitBest:
            best = bestCandidate
            fitBest = newFit

        tabuList += [bestCandidate.schedule]
        if len(tabuList) > maxSize:
            del tabuList[0]

        if nbrNotImproved > repetitions/20:
            tabuList = []   # Diversification
            bestCandidate = best    # Intensification
            nbrNotImproved = -1
        nbrNotImproved += 1

    return best

def generateNeighbors(individual):
    """
    Construct neighborhood of an individual for the tabu search

    :param individual: The individual which neighborhood we search
    :return: the neighborhood of the individual
    """
    neighborhood = []

    for period in range(individual.nbrPeriods):
        liste = list(itertools.chain.from_iterable([i[period] for i in individual.schedule]))

        counter = Counter(liste)
        conflicts = Counter({team: occurence-2 for team, occurence in counter.items() if occurence > 2}).items()

        for conflict in conflicts:
            weeksToSwap = []
            for week in range(individual.nbrWeeks):
                if conflict[0] in individual.schedule[week][period]: # Faire une liste de toutes les semaines où échanger 2 périodes ?
                    weeksToSwap += [week]

            choosenWeeks = random.sample(weeksToSwap, conflict[1])
            periodsToSwap = list(range(individual.nbrPeriods))
            periodsToSwap.remove(period)
            periodToSwap = random.choice(periodsToSwap)
            for week in choosenWeeks:
                neighbor = Tournament(individual.nbrTeams, deepcopy(individual.schedule))
                swap = neighbor.schedule[week][periodToSwap]
                neighbor.schedule[week][periodToSwap] = neighbor.schedule[week][period]
                neighbor.schedule[week][period] = swap
                neighborhood += [neighbor]

    return neighborhood

def descent():
    pass

def fitnessRemoval(pop, nbToRemove=2):
    """
    Remove the worst individuals

    :param pop: The list of the population
    :param nbToRemove: The number of individuals to remove

    :return: The population minus the worst individuals
    """

    pop.sort(key=lambda individual: (individual[1], random.random()))
    return pop[nbToRemove:]

def dummy(parents, nbChildren=2):
    return parents

def genTour(n):
    """
    Generate an individual as an array of int with size n, populated with zeros

    :param n: The size of the array

    :return: The individual
    """

    return lambda : Tournament(n)

# Main function to launch memetic algorithm
def main():

    #for i in generatePop(2, tournamentGeneration):
    #    print(i)
    #    print(fit(i))

    resultats = []

    fitRes = 1

    #while fitRes != 0:
    #for i in range(1):
    #    t = Tournament(14)

    #    fitT = fit(t)
    #    fitRes = fit(tabuSearch(t, 100, 10000))

    #    resultats += [(fitT, fitRes)]

    #print(resultats)
    #print(len(resultats))
    #for i in range(10):
    #    evolution(genTour(14), fit, uniformWeek, tabuSearch, fitnessRemoval,
    #          endCondition=(0, 100), popSize=50, mutationRate=0.8, crossoverRate=1, end=i)
    #print("base \n" + str(t))
    #print(fit(t))
    #res = tabuSearch(t)
    #print("\n résultat \n" + str(res))
    #print(fit(res))

    print("[(1,2) ... (n-1, n)]")
    print()
    print()

    print("\t|\t1\t|\t2\t|\t...\t|\tn-1")
    print("1   |")
    print("... |")
    print("n/2 |")

    #results = []

    #for i in range(20):
        #results += [evolution(tournamentGeneration, fit, monopoint, bitFlip, ageRemoval,
        #                      endCondition=(100, 1000), popSize=20, mutationRate=5, crossoverRate=1)[0][1]]
        #print(i)

    #print(results)



if __name__ == '__main__':
    main()
