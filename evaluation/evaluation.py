import bz2

from genetic_algorithm import file_management
from genetic_algorithm.string_operations import string_similarity


def compute_ncd(a, b):
    ca = float(len(bz2.compress(a)))
    cb = float(len(bz2.compress(b)))
    cab = float(len(bz2.compress(a + b)))
    return 1 - (cab - min(ca, cb)) / max(ca, cb)


def create_string_repertoire(vector):
    result = ""
    for x in vector:
        result = result + "".join(x["choreo"])
    return result


def create_string(vector):
    result = ""
    for x in vector:
        result = result + "".join(x)
    return result


def calculate_typicality_with_min_distance_from_files(repertoire, results):
    values = []
    for choreo in results:
        sim_min = 1
        if choreo != "":
            for choreo_repertoire in repertoire:
                if choreo_repertoire != "":
                    sim_min = min(sim_min, string_similarity("".join(choreo), "".join(choreo_repertoire)))
            values.append(sim_min)
    return values


def calculate_typicality_with_min_distance(repertoire_path, results):
    values = []
    for choreo in results:
        sim_min = 1
        for choreo_repertoire in file_management.getRepertoireWithPath(repertoire_path)["repertoire"]:
            sim_min = min(sim_min, string_similarity("".join(choreo), "".join(choreo_repertoire["choreo"])))
        values.append(sim_min)
    return values
