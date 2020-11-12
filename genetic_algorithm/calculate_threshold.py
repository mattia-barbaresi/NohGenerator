from genetic_algorithm import file_management
from string_operations import string_similarity


def calculate_fitness_threshold(repertoire_path):
    sim_min = 1
    if len(file_management.getRepertoireWithPath(repertoire_path)["repertoire"]) == 1:
        return 0.62
    for choreo1 in file_management.getRepertoireWithPath(repertoire_path)["repertoire"]:
        similarity = 0
        n = 0
        for choreo2 in file_management.getRepertoireWithPath(repertoire_path)["repertoire"]:
            if "".join(choreo1["choreo"]) != "".join(choreo2["choreo"]):
                similarity = similarity + string_similarity("".join(choreo1["choreo"]), "".join(choreo2["choreo"]))
                n = n + 1
        similarity = similarity / n
        sim_min = min(sim_min, similarity)
    return sim_min


def calculate_fitness_threshold_max(repertoire_path):
    sim_max = 0
    if len(file_management.getRepertoireWithPath(repertoire_path)["repertoire"]) == 1:
        return 0.75
    for choreo1 in file_management.getRepertoireWithPath(repertoire_path)["repertoire"]:
        similarity = 0
        n = 0
        for choreo2 in file_management.getRepertoireWithPath(repertoire_path)["repertoire"]:
            if "".join(choreo1["choreo"]) != "".join(choreo2["choreo"]):
                similarity = similarity + string_similarity("".join(choreo1["choreo"]), "".join(choreo2["choreo"]))
                n = n + 1
        similarity = similarity / n
        sim_max = max(sim_max, similarity)
    return sim_max
