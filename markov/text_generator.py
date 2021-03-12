import pprint
import random

vocabulary = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u",
              "v", "w", "x", "y", "z"]

pp = pprint.PrettyPrinter(indent=2)


def matrix_generator(n):
    """"Generates a transition probability square matrix for n elements.
        For each row the sum of values is equal to 1.
        """
    # ok...but probability distribution is too uniform
    result = [[random.randint(0, n) for i in range(n)] for j in range(n)]
    for r in result:
        tot = sum(r)
        for j in range(0,n):
            r[j] = round(r[j]/tot,2)
    # chek summation is 1 for each row
    for j,r in enumerate(result):
        r[j] += round(1 - sum(r),2)
    return result


def generate(trans_mtx, n_occ, start_index=-1):
    """"Given a transition probability matrix generates text of given length n_occ,
    starting from the specified start_index, random otherwise.
    """
    random.seed()
    ind = start_index
    if start_index < 0:
        ind = random.randint(0, len(vocabulary))
    res = str(vocabulary[ind])
    for i in range(0, n_occ-1):
        rnd = random.uniform(0,1)
        sm = 0
        j = 0
        while sm < rnd:
            sm += trans_mtx[ind][j]
            if sm > rnd:
                res += vocabulary[j]
                ind = j
            j += 1
    print(res)


# generate a transition matrix for a grammar
mtx = matrix_generator(len(vocabulary))
pp.pprint(mtx)
for q in range(0,50):
    generate(mtx,16,3)
