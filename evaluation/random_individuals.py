import random


def init_individual(n, lst):
    # ind_class will receive a class inheriting from MyContainer
    moves_list = []
    # for _ in range(random.randint(Constants.min_number_of_moves, Constants.max_number_of_moves)):
    for _ in range(n):
        move = random.choice(lst)
        moves_list.append(move)
    return moves_list

