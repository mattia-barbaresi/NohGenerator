import random

import constants
from dissimilarity import archive_dissim
from genetic_algorithm import tournament_novelty, file_management
from genetic_algorithm.string_operations import string_dissimilarity, string_similarity


# return novelty value of the individual
# calculated as the dissimilarity from the 4 most similar neighbours from (pop U archive)
def novelty(individual, population, parameters):
    if len(parameters.archive) == 0:
        print "- archive with 0 entries!"

    # select the neighbours
    pop_selected = tournament_novelty.select(population, individual, parameters.archive)
    value = 0
    # calculate individual dissimilarity (novelty)
    for x in pop_selected:
        value = value + string_dissimilarity("".join(individual), "".join(x))
    value = value / len(pop_selected)
    return value


def archive_assessment(individual, evaluation,  parameters):
    arch_len = len(parameters.archive)
    # conditions needed to add the individual to the archive
    if evaluation > parameters.fitness_threshold:
        # if the archive has no entries or if the dissimilarity between the
        # element and the choreographies in the archive is higher than a threshold
        arch_dissim = archive_dissim(individual, parameters)
        if arch_len == 0 or arch_dissim > parameters.dissim_threshold:
            ml = "".join(individual)
            parameters.archive.append(ml)
            file_management.addres(x={"choreo": ml,"method_index": parameters.evaluation_method_index, "fitness": evaluation, "dissim": arch_dissim},
                                   path=parameters.full_name + "res_arch", index=arch_len)


# return fitness value of the individual
# calculate as the similarity from the repertoire
def fitness(individual, parameters):
    evaluation = 0
    repertoire = file_management.getRepertoireWithPath(parameters.repertoire_path)["repertoire"]
    repertoire_size = len(repertoire)
    for x in repertoire:
        evaluation = evaluation + string_similarity("".join(x["choreo"]), "".join(individual))
    evaluation = evaluation / repertoire_size
    return evaluation


# used to return (novelty, 0) to the genetic
def calculate_novelty(individual, population, parameters):
    res = novelty(individual, population, parameters)
    archive_assessment(individual, res, parameters)
    return 0, res


# used to return (fitness, 0) to the genetic
def calculate_fitness(individual, parameters):
    return fitness(individual, parameters), 0


# used to return (fitness, novelty) to the genetic
def calculate_fitness_and_novelty(individual, population, parameters):
    fitness_value = fitness(individual, parameters)
    archive_assessment(individual, fitness_value, parameters)
    novelty_value = novelty(individual, population, parameters)
    return fitness_value, novelty_value


def mutation(move_list):
    for _ in range(random.randint(1, constants.MAX_NUMBER_OF_MUTATIONS)):
        move_list[random.randint(0, len(move_list) - 1)] = random.choice(constants.LIST_OF_MOVES.keys())
    return (move_list,)


def init_random():
    moves_list = []
    for _ in range(constants.NUMBER_OF_MOVES):
        move = random.choice(constants.LIST_OF_MOVES.keys())
        moves_list.append(move)
    return moves_list
