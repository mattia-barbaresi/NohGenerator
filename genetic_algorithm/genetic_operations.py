import random

import constants
from dissimilarity import dissim
from genetic_algorithm import tournament_novelty, file_management
from genetic_algorithm.string_operations import string_dissimilarity, string_similarity


# return novelty value of the individual
def novelty(individual, population):
    archive = file_management.getArchive()["archive"]
    if len(archive) == 0:
        print "- archive with 0 individuals!"
        print archive
    # here selects the novelty individuals
    pop_selected = tournament_novelty.select(population, individual, archive)
    value = 0
    for x in pop_selected:
        value = value + string_dissimilarity("".join(individual), "".join(x))
    value = value / len(pop_selected)
    return value


def fitness(individual, parameters):
    evaluation = 0
    repertoire = file_management.getRepertoireWithPath(parameters.repertoire_path)["repertoire"]
    repertoire_size = len(repertoire)
    for x in repertoire:
        evaluation = evaluation + string_similarity("".join(x["choreo"]), "".join(individual))
    evaluation = evaluation / repertoire_size
    return evaluation


# used to return (fitness, 0) to the genetic
def calculate_fitness(individual, parameters):
    return (fitness(individual, parameters), 0)


# used to return (fitness, novelty) to the genetic
def calculate_fitness_and_novelty(individual, population, parameters):
    fitness_value = fitness(individual, parameters)

    # conditions needed to add the choreography to the archive
    if fitness_value > parameters.fitness_threshold:
        archive = file_management.getArchive()["archive"]
        arch_len = len(archive)
        # if the archive has no entries or if the dissimilarity between the
        # element and the choreographies in the archive is higher than a threshold
        diss = dissim(individual)
        if arch_len == 0 or dissim(individual) > parameters.dissim_threshold:
            ml = "".join(individual)
            # add to archive
            print ("added to archive :" + ml)
            file_management.addToArchive(ml)
            file_management.addres(x={"choreo": ml, "fitness": fitness_value, "dissim": diss},
                                   path=parameters.full_name + "res_arch", index=arch_len)
    novelty_value = novelty(individual, population)
    print (fitness_value, novelty_value)
    return (fitness_value, novelty_value)


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
