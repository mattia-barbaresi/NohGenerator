from genetic_algorithm import constants, file_management
from genetic_algorithm.string_operations import string_dissimilarity


def dissim(individual):
    archive = file_management.getArchive()["archive"]
    values = []
    for x in archive:
        values.append(string_dissimilarity("".join(x), "".join(individual)))
    # here I need to select the most similar images (min dissimilarity)
    values.sort()
    max_len = min(constants.MAX_ARCH, len(archive))
    dissimilarity = 0
    for i in range(0, max_len):
        dissimilarity = dissimilarity + values[i]
    if max_len > 0:
        dissimilarity = dissimilarity / max_len
    return dissimilarity
