from distance import jaccard
from pyjarowinkler import distance as jw


# similar is 1
# dissimilar is 0
def string_similarity(a, b):
    a = "".join(a)
    b = "".join(b)
    return (jw.get_jaro_distance(a, b) + 1 - jaccard(a, b)) / 2


# similar is 0
# dissimilar is 1
def string_dissimilarity(a, b):
    a = "".join(a)
    b = "".join(b)
    return 1 - ((jw.get_jaro_distance(a, b) + 1 - jaccard(a, b)) / 2)
