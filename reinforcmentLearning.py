import random


# Avec la roulette, renvoyer ptet un array de fois ou chaque opérateur est appelé ?
# Récupérer peu importe roulette ou pas le nombre de fois que l'opérateur a été appelé
# Voir comment faire pour que la roulette garde l'info -> renvoyer la méthode utilisée et faire un compteur là dessus ? voir deap
# Voir comment faire pour utiliser une méthode selon la proba de toutes celles proposées.

# Add a "fixed" wheel ?
def fixedRoulette(ind, methods):
    proba_list = [1 / len(methods) for i in range(len(methods))]

    # pmin+1-pmin ? -> si != 1 problème sur la roulette ?

    r = random.random()
    somme = 0
    i = 0
    while somme < r and i < len(proba_list):
        somme = somme + proba_list[i]
        if (somme < r):
            i = i + 1
    return i


def roulette(methods):
    proba_list = [1 / len(methods) for i in range(len(methods))]
    # pmin+1-pmin ? -> si != 1 problème sur la roulette ?

    r = random.random()
    somme = 0
    i = 0
    while somme < r and i < len(proba_list):
        somme = somme + proba_list[i]
        if (somme < r):
            i = i + 1
    return i


def update_roulette_wheel(reward_list, proba_list, p_min):
    somme_util = sum(reward_list)
    if somme_util > 0:
        for i in range(len(proba_list)):
            proba_list[i] = p_min + (1 - len(proba_list) * p_min) * (reward_list[i] / (somme_util))
    else:
        proba_list = [1 / len(proba_list) for i in range(len(proba_list))]


# initialisation des structures de stockage des utilités
def init_reward_list(taille):
    rewards = [0 for i in range(taille)]
    return rewards


def init_reward_history(taille):
    rewards = [[0] for i in range(taille)]
    return rewards


def init_op_history(l, taille):
    for o in range(taille):
        l.append([0])


FITNESS_OFFSET = 5


# calcul de l'amélioration/reward immédiate (plusieurs versions possibles)
def improvement(val_init, val_mut):
    return ((val_mut - val_init) + FITNESS_OFFSET)
    # return max(0,(val_mut-val_init))
    # return max(0,(val_mut-val_init)/ONE_MAX_LENGTH)
    # return (val_mut-val_init)/ONE_MAX_LENGTH


# calcul de moyenne simple
def update_reward(reward_list, iter, index, value):
    reward_list[index] = ((iter - 1) * reward_list[index] + value) / (iter)


# sliding window
def update_reward_sliding(reward_list, reward_history, history_size, index, value):
    if reward_history[index] == [0]:
        reward_history[index] = [value]
    else:
        reward_history[index].append(value)
    if (len(reward_history[index]) > history_size):
        reward_history[index] = reward_history[index][1:len(reward_history[index])]
    reward_list[index] = sum(reward_history[index]) / len(reward_history[index])
