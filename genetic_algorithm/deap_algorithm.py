import random

import bcolors
from deap import base, creator, tools

import json_editor
from evaluation.evaluation import compute_ncd
from evaluation.ritchie_criteria import compute_criterion_1, compute_criterion_2
from evaluation.sbc import SBC
from genetic_algorithm import fitness_novelty as Operations, constants, file_management
from plots.plot2d import plot2d, plot2d_2_series, plot2d_no_lim


def calculate_fitnesses(ind, pop, toolbox, parameters):
    try:
        return toolbox.evaluate(ind, parameters)
    except Exception as e:
        print "fitness"
        print e


def calculate_novelty(ind, pop, toolbox, parameters):
    try:
        return toolbox.evaluate_hybrid(ind, pop, parameters)
    except Exception as e:
        print "novelty"
        print e


def print_pop(pop):
    for x in pop:
        print "".join(x), x.fitness.values


# evaluation_method: 0 fitness, 1 novelty, 2 both
# def create_choreography(number_of_generations):
# def create_choreography(parameters, number_of_generations, evaluation_method, repertoirePath):
def create_choreography(parameters):
    # initialization
    fitness_function = calculate_fitnesses
    if parameters.evaluation_method_index == 1:
        fitness_function = calculate_novelty

    random.seed(parameters.random_seed)
    file_management.clearArchive()
    file_management.initres(parameters.full_name)

    # init DEAP fitness and individual for tournament in novelty search
    if hasattr(creator, "FitnessMaxTN"):
        delattr(creator, "FitnessMaxTN")
        delattr(creator, "IndividualTN")
    creator.create("FitnessMaxTN", base.Fitness, weights=(1.0,))
    creator.create("IndividualTN", list, fitness=creator.FitnessMaxTN)

    # init DEAP fitness and individual
    if hasattr(creator, "FitnessMax"):
        delattr(creator, "FitnessMax")
        delattr(creator, "Individual")
    creator.create("FitnessMax", base.Fitness, weights=(1.0, 1.0))
    creator.create("Individual", list, fitness=creator.FitnessMax)

    # DEAP toolbox and registration
    toolbox = base.Toolbox()
    toolbox.register("individual", tools.initIterate, creator.Individual, Operations.init_individual)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    toolbox.register("evaluate", Operations.calculate_fitness)
    toolbox.register("evaluate_hybrid", Operations.calculate_fitness_and_novelty)
    toolbox.register("mutate", Operations.mutation)
    toolbox.register("mate", tools.cxTwoPoint)
    toolbox.register("selectspea2", tools.selSPEA2, k=constants.POPULATION_SIZE / 10)
    toolbox.register("selectTournament", tools.selTournament, k=constants.POPULATION_SIZE / 10, tournsize=5)

    # init the counter of individuals with fitness over threshold over to 0
    count_individuals = 0
    repertoire_string = ""
    for x in file_management.getRepertoireWithPath(parameters.repertoire_path)["repertoire"]:
        repertoire_string = repertoire_string + "".join(x["choreo"])

    full_ncd_results = {}
    full_sbc_results = {}
    criterion_1 = {}
    criterion_2 = {}
    fitnesses_avg = {}
    novelty_avg = {}
    archive_size = {}

    # create the population
    pop = toolbox.population(n=constants.POPULATION_SIZE)
    print "population done"

    # Begin the evolution
    g = 0
    # print(bcolors.BLUE + "initialization" + bcolors.ENDC)
    print "initialization"
    generations = []
    for g in range(parameters.number_of_generations):
        # while g < parameters.number_of_generations or
        # (fitness_function == calculate_fitnesses and not parameters.evaluation_method_index == 0):
        # A new generation
        g = g + 1
        # print "generation", g

        # switch function for evaluation
        if parameters.evaluation_method_index == 2:
            if count_individuals >= constants.T_MAX and fitness_function == calculate_fitnesses:
                fitness_function = calculate_novelty
            elif count_individuals <= constants.T_MIN and fitness_function == calculate_novelty:
                fitness_function = calculate_fitnesses
        if fitness_function == calculate_novelty:
            # print "novelty"
            print bcolors.OKMSG + "novelty" + bcolors.ENDC
            generations.append("novelty")
        else:
            # print "fitness"
            print bcolors.ERRMSG + "fitness" + bcolors.ENDC
            generations.append("fitness")

        # evaluate the offspring
        count_individuals = 0
        for ind in pop:
            ind.fitness.values = fitness_function(ind, pop, toolbox, parameters)
            if ind.fitness.values[0] > parameters.fitness_threshold:
                count_individuals = count_individuals + 1
        archive_size[g] = len(file_management.getArchive()["archive"])

        # selection
        if parameters.evaluation_method_index == 2:
            if fitness_function == calculate_fitnesses:
                parents = toolbox.selectTournament(pop)
            else:
                parents = toolbox.selectspea2(pop)
        elif parameters.evaluation_method_index == 1:
            parents = toolbox.selectspea2(pop)
        else:
            parents = toolbox.selectTournament(pop)

        # stats
        results_full = ""
        avg_nov_local = 0
        avg_fit_local = 0
        for x in parents:
            results_full = results_full + "".join(x)
            if fitness_function == calculate_novelty:
                avg_nov_local = avg_nov_local + x.fitness.values[1]
            avg_fit_local = avg_fit_local + x.fitness.values[0]
        avg_fit_local = avg_fit_local / 10
        avg_nov_local = avg_nov_local / 10
        if fitness_function == calculate_novelty:
            novelty_avg[g] = avg_nov_local
        fitnesses_avg[g] = avg_fit_local

        # evaluate metrics

        # sbc
        res_list = []
        for x in parents:
            res_list.append("".join(x))
        sbc = SBC("bz2", "9", res_list)
        full_sbc_results[g] = sbc.compute()  # sbc of generation

        # ncd
        full_ncd_results[g] = compute_ncd(results_full, repertoire_string)
        criterion_1[g] = compute_criterion_1(list(map(toolbox.clone, parents)), repertoire_string)
        criterion_2[g] = compute_criterion_2(list(map(toolbox.clone, parents)), repertoire_string, 0.5)

        # Clone the selected individuals
        offspring = list(map(toolbox.clone, parents))
        # new individuals of the population
        new = []

        # crossover
        i = 0
        for child1 in offspring:
            for child2 in offspring:
                if i < constants.POPULATION_SIZE * 9 / 10:
                    child1_copy = toolbox.clone(child1)
                    child2_copy = toolbox.clone(child2)
                    a, b = toolbox.mate(child1_copy, child2_copy)
                    new.append(a)
                    new.append(b)
                    i = i + 2

        # mutation
        for mutant in new:
            if random.random() < constants.MUTPB:
                toolbox.mutate(mutant)
                del mutant.fitness.values

        # create the new offspring with old population and new individuals
        pop = parents + new

    # last evaluation
    for ind in pop:
        ind.fitness.values = fitness_function(ind, pop, toolbox, parameters)

    # last selection
    if parameters.evaluation_method_index == 2:
        if fitness_function == calculate_fitnesses:
            final = toolbox.selectTournament(pop)
        else:
            final = toolbox.selectspea2(pop)
    elif parameters.evaluation_method_index == 1:
        final = toolbox.selectspea2(pop)
    else:
        final = toolbox.selectTournament(pop)
    results_full = ""

    # plots results
    avg_nov_local = 0
    avg_fit_local = 0
    for x in final:
        results_full = results_full + "".join(x)
        if fitness_function == calculate_novelty:
            avg_nov_local = avg_nov_local + x.fitness.values[1]
        avg_fit_local = avg_fit_local + x.fitness.values[0]
    avg_fit_local = avg_fit_local / 10
    avg_nov_local = avg_nov_local / 10
    if fitness_function == calculate_novelty:
        novelty_avg[g] = avg_nov_local
    fitnesses_avg[g] = avg_fit_local
    if fitness_function == calculate_novelty:
        plot2d_2_series(data=fitnesses_avg, data2=novelty_avg, x_label="generation", y_label="fitness and novelty",
                        path=parameters.full_name + "values")
    else:
        plot2d(data=fitnesses_avg, x_label="generation", y_label="fitness", path=parameters.full_name + "values")
    archive_size[g] = len(file_management.getArchive()["archive"])
    plot2d_no_lim(data=archive_size, x_label="generation", y_label="archive size",
                  path=parameters.full_name + "archivesize")

    # last metrics

    res_list = []
    # sbc of last gen
    for x in final:
        res_list.append("".join(x))
    sbc = SBC("bz2", "9", res_list)
    full_sbc_results[g] = sbc.compute()  # sbc of generation
    full_ncd_results[g] = compute_ncd(results_full, repertoire_string)
    criterion_1[g] = compute_criterion_1(list(map(toolbox.clone, final)), repertoire_string)
    criterion_2[g] = compute_criterion_2(list(map(toolbox.clone, final)), repertoire_string, 0.5)

    # plots
    plot2d(data=full_sbc_results, x_label="generation", y_label="sbc", path=parameters.full_name + "sbc")
    plot2d(data=full_ncd_results, x_label="generation", y_label="ncd_full", path=parameters.full_name + "ncd_full")
    plot2d(data=criterion_1, x_label="generation", y_label="criterion_1", path=parameters.full_name + "criterion_1")
    plot2d(data=criterion_2, x_label="generation", y_label="criterion_2", path=parameters.full_name + "criterion_2")
    plot2d_2_series(data=full_sbc_results, data2=full_ncd_results, x_label="generation", y_label="sbc_ncd",
                    path=parameters.full_name + "sbc_ncd")
    # plot2d_fit_nov(pop,final, parameters.full_name)

    # save results
    json_editor.dump_dict(filename=parameters.full_name + "sbc", dictionary=full_sbc_results)
    json_editor.dump_dict(filename=parameters.full_name + "ncd_full", dictionary=full_ncd_results)
    json_editor.dump_dict(filename=parameters.full_name + "criterion_1", dictionary=criterion_1)
    json_editor.dump_dict(filename=parameters.full_name + "criterion_2", dictionary=criterion_2)
    json_editor.dump_dict(filename=parameters.full_name + "criterion_2", dictionary=criterion_2)
    json_editor.dump_dict(filename=parameters.full_name + "archivesize", dictionary=archive_size)
    json_editor.dump_dict(filename=parameters.full_name + "values",
                          dictionary={"fitness": fitnesses_avg,
                                      "novelty": novelty_avg,
                                      "sbc": full_sbc_results,
                                      "ncd": full_ncd_results})

    return final, generations
