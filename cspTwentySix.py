from evolution import *
import random

# Tournament model and functions for fitness, crossovers & mutations (local search)
# Each tournament is created to respect two constraints:
# - Each team has only one match per week
# - Each possible match is played once
#
# We only need to work on the periods

class Tournament:
    def __init__(self, numberOfTeams=6):
        self.nbrTeams = numberOfTeams
        self.nbrWeeks = numberOfTeams-1
        self.nbrPeriods = int(numberOfTeams/2)
        self.schedule = self.makeSchedule()

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
    Calculate a score for a tournament (

    :param individual: An individual to test (a tournament)

    :return: The score of an individual
    """

    pass

# Crossover
def monopoint():
    pass

def uniform():
    pass


# Mutations (local search so as to have a memetic algorithm)
def simulatedAnnealing():
    pass

def tabuSearch():
    pass

def descent():
    pass


# Main function to launch memetic algorithm
def main():

    t = Tournament()

    for i in generatePop(2, tournamentGeneration):
        print(i)

    #results = []

    #for i in range(20):
        #results += [evolution(tournamentGeneration, fit, monopoint, bitFlip, ageRemoval,
        #                      endCondition=(100, 1000), popSize=20, mutationRate=5, crossoverRate=1)[0][1]]
        #print(i)

    #print(results)



if __name__ == '__main__':
    main()