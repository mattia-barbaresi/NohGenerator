import random

import constants
from dissimilarity import dissim
from genetic_algorithm import tournament_novelty, file_management
from genetic_algorithm.string_operations import string_dissimilarity, string_similarity


def novelty(choreography, population):
    archive = file_management.getArchive()["archive"]
    # if len(archive) == 0:
    #     return 0
    # here selects the novelty individuals
    pop_selected = tournament_novelty.select(population, choreography, archive)
    value = 0
    for x in pop_selected:
        value = value + string_dissimilarity("".join(choreography), "".join(x))
    value = value / len(pop_selected)
    return value


# the return should be between parenthesis because needs to return a list
# correct
def fitness(movesList, parameters):
    evaluation = 0
    repertoire = file_management.getRepertoireWithPath(parameters.repertoire_path)["repertoire"]
    repertoire_size = len(repertoire)
    archive = file_management.getArchive()["archive"]
    arch_len = len(archive)
    for x in repertoire:
        evaluation = evaluation + string_similarity("".join(x["choreo"]), "".join(movesList))
    evaluation = evaluation / repertoire_size
    # conditions needed to add the choreography to the archive
    if evaluation > parameters.fitness_threshold:
        # if the archive has no entries or if the dissimilarity between the
        # element and the choreographies in the archive is higher than a threshold
        diss = dissim(movesList)
        if arch_len == 0 or dissim(movesList) > parameters.dissim_threshold:
            ml = "".join(movesList)
            file_management.addToArchive(ml)
            file_management.addres(x={"choreo": ml, "fitness": evaluation, "dissim": diss},
                                   path=parameters.full_name + "res_arch", index=arch_len)
    return evaluation


def calculate_fitness(movesList, parameters):
    return (fitness(movesList, parameters), 0)


def calculate_fitness_and_novelty(choreography, population, parameters):
    fitness_value = fitness(choreography, parameters)
    novelty_value = novelty(choreography, population)
    return (fitness_value, novelty_value)


def mutation(movesList):
    for _ in range(random.randint(1, constants.MAX_NUMBER_OF_MUTATIONS)):
        movesList[random.randint(0, len(movesList) - 1)] = random.choice(constants.LIST_OF_MOVES.keys())
    return (movesList,)


def init_individual():
    moves_list = []
    for _ in range(constants.NUMBER_OF_MOVES):
        move = random.choice(constants.LIST_OF_MOVES.keys())
        moves_list.append(move)
    return moves_list
