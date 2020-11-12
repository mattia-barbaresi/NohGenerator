import os
import time
from evaluation.evaluation import create_string_results, create_string_repertoire, compute_ncd, \
    calculate_typicality_with_min_distance
from evaluation.sbc import SBC
from genetic_algorithm import deap_algorithm as deap_algorithm, constants, file_management
from genetic_algorithm.Parameters import Parameters


# repertoire index is the index of the corresponding path in constants
def init(number_of_generations, repertoire_index, evaluation_method_index, random_seed, dissim_threshold,
         fitness_threshold):
    evaluation_method = "fitness"
    if evaluation_method_index == 1:
        evaluation_method = "novelty"
    elif evaluation_method_index == 2:
        evaluation_method = "fitness and novelty"

    parameters = Parameters(number_of_generations=number_of_generations,
                            repertoire_path=constants.REPERTOIRE_PATH[repertoire_index],
                            evaluation_method_index=evaluation_method_index,
                            random_seed=random_seed,
                            dissim_threshold=dissim_threshold,
                            fitness_threshold=fitness_threshold)
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

    if not os.path.exists(full_name):
        try:
            os.makedirs(full_name)
            print "init with path: " + full_name
        except Exception as e:
            print e
    else:
        print "Dir already exist: " + full_name

    parameters.set_path(full_name)
    start_time = time.time()
    pop, generations = deap_algorithm.create_choreography(parameters)
    # print "ending"
    # Gather all the fitness values in one list and print the stats
    fits = [ind.fitness.values[0] for ind in pop]
    time_elapsed = (time.time() - start_time)
    print("--- %s seconds ---" % str(time_elapsed))
    results_string = create_string_results(pop)
    repertoire_string = create_string_repertoire(
        file_management.getRepertoireWithPath(parameters.repertoire_path)["repertoire"])
    ncd = compute_ncd(results_string, repertoire_string)
    res_list = []
    for x in pop:
        res_list.append("".join(x))
    sbc = SBC("bz2", "9", res_list)
    sbc_t = sbc.compute()  # sbc of generation
    rep_list = []

    # calculate sbc for repertoire
    for x in file_management.getRepertoireWithPath(parameters.repertoire_path)["repertoire"]:
        rep_list.append(x["choreo"])
    sbc = SBC("bz2", "9", rep_list)
    sbc_rep = sbc.compute()  # sbc of repertoire

    length = len(pop)
    mean = sum(fits) / length
    sum2 = sum(x * x for x in fits)
    std = abs(sum2 / length - mean ** 2) ** 0.5
    statistics = {"min": min(fits), "max": max(fits), "mean": mean, "std": std}
    parameters_to_serialize = {
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
        "mutpb": constants.MUTPB,
        "evaluation_method": evaluation_method
    }

    print("  Min %s" % min(fits))
    print("  Max %s" % max(fits))
    print("  Avg %s" % mean)
    print("  Std %s" % std)
    print("  Ncd %s" % ncd)
    print("  Sbc %s" % sbc_t)

    results = []
    # open file streams
    results_file = open(full_name + "results_serialized", "w")
    archive_file = open(full_name + "archive_serialized", "w")
    repertoire_file = open(full_name + "repertoire_serialized", "w")
    gens_file = open(full_name + "generations_serialized", "w")

    for ind in pop:
        results.append({"ind": "".join(ind), "value": ind.fitness.values})
        print >>results_file, "".join(ind)
    for element in file_management.getArchive()["archive"]:
        print >>archive_file, "".join(element)
    for element in file_management.getRepertoireWithPath(parameters.repertoire_path)["repertoire"]:
        print >>repertoire_file, "".join(element["choreo"])
    for element in generations:
        print >>gens_file, "".join(element)

    # close file streams
    results_file.close()
    archive_file.close()
    repertoire_file.close()
    gens_file.close()

    file_management.saveResultsToPath({
        "time elapsed": time_elapsed,
        "statistics": statistics,
        "ncd": ncd,
        "sbc":sbc_t,
        "sbc_rep": sbc_rep,
        "min_distance": calculate_typicality_with_min_distance(parameters.repertoire_path, pop),
        "archive": file_management.getArchive()["archive"],
        "list_of_moves": constants.LIST_OF_MOVES,
        "repertoire": file_management.getRepertoireWithPath(parameters.repertoire_path)["repertoire"],
        "parameters": parameters_to_serialize,
        "results": results,
        # "strings" : [results_string, repertoire_string]
    }, full_name + "results")

    print "end reached"
