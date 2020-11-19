import os
import time
from evaluation.evaluation import create_string, create_string_repertoire, compute_ncd, \
    calculate_typicality_with_min_distance
from evaluation.sbc import compute_sbc_from_pop
from genetic_algorithm import deap_algorithm as deap_algorithm, constants, file_management
from genetic_algorithm.Parameters import Parameters


# repertoire index is the index of the corresponding repertoire file in paths list in constants
def init(number_of_generations, repertoire_index, evaluation_method_index, random_seed, dissim_threshold,
         fitness_threshold):

    # init params
    parameters = Parameters(number_of_generations=number_of_generations,
                            repertoire_path=constants.REPERTOIRE_PATH[repertoire_index],
                            evaluation_method_index=evaluation_method_index,
                            random_seed=random_seed,
                            dissim_threshold=dissim_threshold,
                            fitness_threshold=fitness_threshold)

    # set method string
    evaluation_method = "fitness"
    if evaluation_method_index == 1:
        evaluation_method = "novelty"
    elif evaluation_method_index == 2:
        evaluation_method = "fitness and novelty"

    # set full path name
    full_name = "data/results/" \
                + str(constants.NUMBER_OF_MOVES) + "_" \
                + str(constants.MAX_ARCH) + "_" \
                + str(constants.MUTPB) + "_" \
                + str(constants.T_MIN) + "_" \
                + str(constants.T_MAX) + "_" \
                + str(constants.MAX_NUMBER_OF_MUTATIONS) + "_" \
                + str(constants.POPULATION_SIZE) + "_" \
                + str(repertoire_index) + "_" \
                + str(number_of_generations) + "_" \
                + str(random_seed) + "_" \
                + str(parameters.fitness_threshold) + "_" \
                + str(parameters.dissim_threshold) \
                + "/" + evaluation_method + "/"  # + "/" + now.strftime("%Y%m%d-%H.%M.%S") + "/"

    # make results dir
    if not os.path.exists(full_name):
        try:
            os.makedirs(full_name)
            print "init path: " + full_name
        except Exception as e:
            print e
    else:
        print "existing path: " + full_name

    parameters.set_path(full_name)

    # execution
    start_time = time.time()
    pop, generations = deap_algorithm.create_choreography(parameters)
    time_elapsed = (time.time() - start_time)

    # compute metrics and stats
    print("--- %s seconds ---" % str(time_elapsed))

    # read results and repertoire
    repertoire = file_management.getRepertoireWithPath(parameters.repertoire_path)["repertoire"]
    results_string = create_string(pop)
    repertoire_string = create_string_repertoire(repertoire)

    # metrics
    ncd = compute_ncd(results_string, repertoire_string)  # ncd
    sbc_t = compute_sbc_from_pop(pop)  # sbc of results
    sbc_rep = compute_sbc_from_pop(repertoire)  # sbc of repertoire

    # stats
    length = len(pop)
    # gather all the fitness values in one list
    fits = [ind.fitness.values[0] for ind in pop]
    novs = [ind.fitness.values[1] for ind in pop]
    mean_f = sum(fits) / length
    mean_n = sum(novs) / length
    sum2f = sum(x * x for x in fits)
    sum2n = sum(x * x for x in novs)
    std_f = abs(sum2f / length - mean_f ** 2) ** 0.5
    std_n = abs(sum2n / length - mean_n ** 2) ** 0.5
    statistics = {
        "min ": (min(fits),min(novs)),
        "max": (max(fits),max(novs)),
        "mean": (mean_f,mean_n),
        "std ": (std_f,std_n),
    }

    # save results
    results = []
    # open file streams
    results_file = open(full_name + "results_serialized", "w")
    repertoire_file = open(full_name + "repertoire_serialized", "w")
    gens_file = open(full_name + "generations_serialized", "w")

    for ind in pop:
        results.append({"ind": "".join(ind), "value": ind.fitness.values})
        print >>results_file, "".join(ind)
    for element in repertoire:
        print >>repertoire_file, "".join(element["choreo"])
    for element in generations:
        print >>gens_file, "".join(element)

    # close file streams
    results_file.close()
    repertoire_file.close()
    gens_file.close()

    sbc_arch = 0
    archive = []
    # save archive (if method was not only fitness)
    if evaluation_method != "fitness":
        archive_file = open(full_name + "archive_serialized", "w")
        archive = parameters.archive
        for element in archive:
            print >> archive_file, element
        archive_file.close()
        sbc_arch = compute_sbc_from_pop(archive)  # sbc of archive

    params = {
        "generations": number_of_generations,
        "fitness_threshold": parameters.fitness_threshold,
        "dissim_threshold": parameters.dissim_threshold,
        "number_of_moves": constants.NUMBER_OF_MOVES,
        "t_min ": constants.T_MIN,
        "t_max": constants.T_MAX,
        "max_arch": constants.MAX_ARCH,
        "max_number_of_mutations": constants.MAX_NUMBER_OF_MUTATIONS,
        "population_size": constants.POPULATION_SIZE,
        # "CXPB": constants.CXPB,
        "mutpb": constants.MUTPB
    }

    file_management.saveResultsToPath({
        "evaluation_method": evaluation_method,
        "time elapsed": time_elapsed,
        "statistics": statistics,
        "ncd": ncd,
        "sbc_res":sbc_t,
        "sbc_rep": sbc_rep,
        "sbc_arch":sbc_arch,
        "archive": archive,
        "repertoire": repertoire,
        "min_distance": calculate_typicality_with_min_distance(parameters.repertoire_path, pop),
        "list_of_moves": constants.LIST_OF_MOVES,
        "parameters": params,
        "results": results,
        # "strings": [results_string, repertoire_string]
    }, full_name + "results")

    # end
    print "end reached"
