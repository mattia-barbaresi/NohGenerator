from genetic_algorithm import constants, file_management
from genetic_algorithm.string_operations import string_dissimilarity


def archive_dissim(individual, parameters):
    archive = parameters.archive
    len_a = len(archive)
    # if no entries in archive then add the individual
    if len_a == 0:
        return "-"
    else:
        values = []
        for x in archive:
            values.append(string_dissimilarity("".join(x), "".join(individual)))
        # select the most similar images (min dissimilarity)
        values.sort()
        max_len = min(constants.MAX_ARCH, len_a)
        dissimilarity = 0
        for i in range(0, max_len):
            dissimilarity = dissimilarity + values[i]
        return dissimilarity / max_len
