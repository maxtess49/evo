import random
import numpy as np


# WHEEL
def select_op(proba_list):
    r = random.random()
    somme = 0
    i = 0
    while somme < r and i < len(proba_list):
        somme = somme + proba_list[i]
        if somme < r:
            i = i + 1
    return i


def update_roulette_wheel(reward_list, proba_list, p_min):
    somme_util = sum(reward_list)
    if somme_util > 0:
        for i in range(len(proba_list)):
            proba_list[i] = p_min + (1 - len(proba_list) * p_min) * (reward_list[i] / (somme_util))
    else:
        proba_list = [1 / len(proba_list) for i in range(len(proba_list))]


# UCB
# MAJ valeurs UCB
def update_UCB_val(UCB_val, C, op_history, reward_list, generationCounter):
    for o in range(len(op_history)):
        UCB_val[o] = reward_list[o] + C * np.sqrt(
            generationCounter / (2 * np.log(1 + op_history[o][generationCounter]) + 1))


# sélection operateur
def select_op_UCB(UCB_val):
    return UCB_val.index(max(UCB_val))


# Init for UCB
def init_proba_list_ucb(taille):
    return [0 for i in range(taille)]


FITNESS_OFFSET = 5


# calcul de l'amélioration/reward immédiate (plusieurs versions possibles)
def improvement(val_init, val_mut):
    return ((val_mut - val_init) + FITNESS_OFFSET)
    # return max(0,(val_mut-val_init))
    # return max(0,(val_mut-val_init)/ONE_MAX_LENGTH)
    # return (val_mut-val_init)/ONE_MAX_LENGTH


# calcul de moyenne simple
def update_reward(reward_list, iter, index, value):
    reward_list[index] = ((iter - 1) * reward_list[index] + value) / iter


# sliding window
def update_reward_sliding(reward_list, reward_history, history_size, index, value):
    if reward_history[index] == [0]:
        reward_history[index] = [value]
    else:
        reward_history[index].append(value)
    if len(reward_history[index]) > history_size:
        reward_history[index] = reward_history[index][1:len(reward_history[index])]
    reward_list[index] = sum(reward_history[index]) / len(reward_history[index])
