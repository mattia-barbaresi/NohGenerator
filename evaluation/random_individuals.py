import random


def init_individual(n, lst):
    # ind_class will receive a class inheriting from MyContainer
    moves_list = []
    # for _ in range(random.randint(Constants.min_number_of_moves, Constants.max_number_of_moves)):
    for _ in range(n):
        move = random.choice(lst)
        moves_list.append(move)
    return moves_list

    # save in file
    # for x in range(100):
    #     with open("data/archive/random", "a") as myfile:
    #         myfile.write("\n"  + str("".join(init_individual())))
