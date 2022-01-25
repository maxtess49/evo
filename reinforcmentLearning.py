import random

# Avec la roulette, renvoyer ptet un array de fois ou chaque opérateur est appelé ?
# Récupérer peu importe roulette ou pas le nombre de fois que l'opérateur a été appelé
# Voir comment faire pour que la roulette garde l'info -> renvoyer la méthode utilisée et faire un compteur là dessus ? voir deap
# Voir comment faire pour utiliser une méthode selon la proba de toutes celles proposées.

# Add a "fixed" wheel ?
def fixedRoulette(ind, methods):
    prob = [1/len(methods) for i in range(len(methods))]

    #pmin+1-pmin ? -> si != 1 problème sur la roulette ?

    methodChoice = random.random()

def roulette():
    #pmin+1-pmin ? -> si != 1 problème sur la roulette ?
    pass