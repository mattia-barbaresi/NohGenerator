import random
import bcolors
from deap import base, creator, tools
from evaluation.evaluation import compute_ncd
from evaluation.ritchie_criteria import compute_criterion_1, compute_criterion_2
from evaluation.sbc import compute_sbc_from_pop
from genetic_algorithm import genetic_operations, constants, file_management, json_editor
from utils.plot2d import plot2d, plot2d_2_series, plot2d_no_lim


# alias for ga ops: only fitness
def calculate_fitness(ind, pop, toolbox, parameters):
    try:
        return toolbox.evaluate(ind, parameters)
    except Exception as e:
        print "fitness error"
        print e


# alias for ga ops: only novelty
def calculate_novelty(ind, pop, toolbox, parameters):
    try:
        return toolbox.evaluate_novelty(ind, pop, parameters)
    except Exception as e:
        print "novelty error"
        print e


# alias for ga ops: hybrid
def calculate_hybrid(ind, pop, toolbox, parameters):
    try:
        return toolbox.evaluate_hybrid(ind, pop, parameters)
    except Exception as e:
        print "hybrid error"
        print e


def create_choreography(parameters):

    # init
    fitness_function = calculate_fitness
    if parameters.evaluation_method_index == 1:
        fitness_function = calculate_novelty

    # init random
    random.seed(parameters.random_seed)

    # init archive
    if parameters.evaluation_method_index != 0:
        parameters.archive = []
        file_management.init_res_arch(parameters.full_name)

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
    toolbox.register("individual", tools.initIterate, creator.Individual, genetic_operations.init_random)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    toolbox.register("evaluate", genetic_operations.calculate_fitness)
    toolbox.register("evaluate_novelty", genetic_operations.calculate_novelty)
    toolbox.register("evaluate_hybrid", genetic_operations.calculate_fitness_and_novelty)
    toolbox.register("mutate", genetic_operations.mutation)
    toolbox.register("mate", tools.cxTwoPoint)
    toolbox.register("selectspea2", tools.selSPEA2, k=constants.POPULATION_SIZE / 10)
    # for novelty tournament
    toolbox.register("selectTournament", tools.selTournament, k=constants.POPULATION_SIZE / 10, tournsize=5)

    # string encoding of repertoire
    repertoire_string = ""
    for x in file_management.getRepertoireWithPath(parameters.repertoire_path)["repertoire"]:
        repertoire_string = repertoire_string + "".join(x["choreo"])

    # create the population
    pop = toolbox.population(n=constants.POPULATION_SIZE)
    print "init population done"

    # init stats variables
    generations = []
    archive_size = {}
    ncd_results = {}
    sbc_results = {}
    criterion_1 = {}
    criterion_2 = {}
    fitness_avg = {}
    novelty_avg = {}
    count_individuals = 0
    parents = []

    for g in range(parameters.number_of_generations):

        # switch function for hybrid evaluation
        if parameters.evaluation_method_index == 2:
            if count_individuals >= constants.T_MAX and fitness_function == calculate_fitness:
                fitness_function = calculate_hybrid
            elif count_individuals <= constants.T_MIN and fitness_function == calculate_hybrid:
                fitness_function = calculate_fitness

        # save used method
        if fitness_function == calculate_fitness:
            # print bcolors.PASS + "fitness" + bcolors.ENDC
            generations.append("fitness")
        elif fitness_function == calculate_novelty:
            # print bcolors.WARN + "novelty" + bcolors.ENDC
            generations.append("novelty")
        elif fitness_function == calculate_hybrid:
            # print bcolors.ERR + "hybrid" + bcolors.ENDC
            generations.append("hybrid")
        else:
            print "FATAL ERROR: NO METHOD FOUND"

        # evaluate the offspring
        # and count individuals above threshold
        count_individuals = 0
        for ind in pop:
            ind.fitness.values = fitness_function(ind, pop, toolbox, parameters)
            if ind.fitness.values[0] > parameters.fitness_threshold:
                count_individuals = count_individuals + 1

        # save archive size
        archive_size[g] = len(parameters.archive)

        # selection
        parents = toolbox.selectspea2(pop)

        # stats
        results_full = ""
        avg_nov_local = 0
        avg_fit_local = 0
        for x in parents:
            results_full = results_full + "".join(x)
            avg_fit_local = avg_fit_local + x.fitness.values[0]
            if parameters.evaluation_method_index != 0:
                avg_nov_local = avg_nov_local + x.fitness.values[1]

        fitness_avg[g] = avg_fit_local / 10
        if parameters.evaluation_method_index != 0:
            novelty_avg[g] = avg_nov_local / 10

        # evaluate metrics
        sbc_results[g] = compute_sbc_from_pop(parents)
        ncd_results[g] = compute_ncd(results_full, repertoire_string)
        criterion_1[g] = compute_criterion_1(list(map(toolbox.clone, parents)), repertoire_string)
        criterion_2[g] = compute_criterion_2(list(map(toolbox.clone, parents)), repertoire_string, 0.5)

        # Clone the selected individuals
        offspring = list(map(toolbox.clone, parents))

        # crossover
        # new individuals of the population
        new = []
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

        # create the new offspring with old population and new individuals (tot = 10 + 90)
        pop = parents + new
    # -----------------

    # plot fitness and novelty avgs
    if parameters.evaluation_method_index == 2:
        plot2d_2_series(data=fitness_avg, data2=novelty_avg, x_label="generation", y_label="fitness and novelty",
                        path=parameters.full_name + "values")
    elif parameters.evaluation_method_index == 1:
        plot2d(data=novelty_avg, x_label="generation", y_label="novelty", path=parameters.full_name + "values")
    else:
        plot2d(data=fitness_avg, x_label="generation", y_label="fitness", path=parameters.full_name + "values")

    # plot archive size
    if parameters.evaluation_method_index != 0:
        plot2d_no_lim(data=archive_size, x_label="generation", y_label="archive size",
                      path=parameters.full_name + "archive_size")

    # plots
    plot2d(data=sbc_results, x_label="generation", y_label="sbc", path=parameters.full_name + "sbc")
    plot2d(data=ncd_results, x_label="generation", y_label="ncd", path=parameters.full_name + "ncd")
    plot2d(data=criterion_1, x_label="generation", y_label="criterion_1", path=parameters.full_name + "criterion_1")
    plot2d(data=criterion_2, x_label="generation", y_label="criterion_2", path=parameters.full_name + "criterion_2")
    plot2d_2_series(data=sbc_results, data2=ncd_results, x_label="generation", y_label="sbc_ncd",
                    path=parameters.full_name + "sbc_ncd")
    # plot2d_fit_nov(pop,final, parameters.full_name)

    # save results
    json_editor.dump_dict(filename=parameters.full_name + "sbc", dictionary=sbc_results)
    json_editor.dump_dict(filename=parameters.full_name + "ncd", dictionary=ncd_results)
    json_editor.dump_dict(filename=parameters.full_name + "criterion_1", dictionary=criterion_1)
    json_editor.dump_dict(filename=parameters.full_name + "criterion_2", dictionary=criterion_2)

    # save archive
    if parameters.evaluation_method_index != 0:
        json_editor.dump_dict(filename=parameters.full_name + "archive_size", dictionary=archive_size)

    # save values
    json_editor.dump_dict(filename=parameters.full_name + "values",
                          dictionary={"fitness": fitness_avg,
                                      "novelty": novelty_avg,
                                      "sbc": sbc_results,
                                      "ncd": ncd_results})

    return parents, generations
