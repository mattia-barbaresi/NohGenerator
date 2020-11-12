import random

from genetic_algorithm import constants


def init_individual():
    # ind_class will receive a class inheriting from MyContainer
    moves_list = []
    # for _ in range(random.randint(Constants.min_number_of_moves, Constants.max_number_of_moves)):
    for _ in range(constants.NUMBER_OF_MOVES):
        move = random.choice(constants.LIST_OF_MOVES.keys())
        moves_list.append(move)
    return moves_list

#
# for x in range(100):
#     with open(Constants.RANDOM_PATH, "a") as myfile:
#         myfile.write("\n"  + str("".join(init_individual())))
