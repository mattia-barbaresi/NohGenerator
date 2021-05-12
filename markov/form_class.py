# count pre- and post- occurrences for each word to find form classes
from collections import OrderedDict
import numpy as np
import pprint
import utils

pp = pprint.PrettyPrinter(indent=2)

# threshold for classes
THS = 2.0


# records pre- and post- lists of words (and the number of occurrences of each of them) that come
# before and after each word in sequences
def distributional_context(sequences, order=1):
    res = OrderedDict()
    for seq in sequences:
        for el in seq:
            if el not in res:
                res[el] = dict()
                res[el]["sx"] = dict()
                res[el]["dx"] = dict()
                for i in range(1, order + 1):
                    for search_seq in sequences:
                        values = np.array(search_seq)
                        for index in np.where(values == el)[0]:
                            # sx occurrence
                            if index >= i:
                                if values[index - i] in res[el]["sx"]:
                                    res[el]["sx"][values[index - i]] += 1
                                else:
                                    res[el]["sx"][values[index - i]] = 1
                            # dx occurrence
                            if index < len(values) - i:
                                if values[index + i] in res[el]["dx"]:
                                    res[el]["dx"][values[index + i]] += 1
                                else:
                                    res[el]["dx"][values[index + i]] = 1
                    # order results
                    res[el]["dx"] = OrderedDict(sorted(res[el]["dx"].items(), key=lambda x: x[1], reverse=True))
                    res[el]["sx"] = OrderedDict(sorted(res[el]["sx"].items(), key=lambda x: x[1], reverse=True))
    return res


# evaluates form classes
def first_last(dist_ctx):
    # print initial and ending classes
    first_set = []
    last_set = []
    pp.pprint(dist_ctx)
    for word in dist_ctx.items():
        if not word[1]["sx"]:
            first_set.append(word[0])
        if not word[1]["dx"]:
            last_set.append(word[0])
    print("first: ", first_set)
    print("last: ", last_set)


def search(k,arr):
    for s in arr.items():
        if k in s[1]:
            return True
    return False


def form_classes(dist_ctx):
    angles = dict()
    for itm1 in dist_ctx.items():
        if itm1[0] not in angles:
            angles[itm1[0]] = dict()
            for itm2 in dist_ctx.items():
                if (itm2[0] != itm1[0]) and (itm2[0] not in angles[itm1[0]]):
                    # calculates pre- and post- contexts similarity (angles)
                    v1 = utils.angle_from_dict(itm1[1]["sx"],itm2[1]["sx"])
                    v2 = utils.angle_from_dict(itm1[1]["dx"],itm2[1]["dx"])
                    angles[itm1[0]][itm2[0]] = (v1 + v2)/2
    # print("angles: ")
    # pp.pprint(angles)
    res = dict()
    idx = 1
    for k,values in angles.items():
        if not search(k,res):
            sim = set()
            sim.add(k)
            sim.update(x[0] for x in values.items() if float(x[1]) < THS)
            res[idx] = sim
            idx += 1

    print("res: ")
    pp.pprint(res)

    return res


def classes_index(classes, word):
    for cl in classes.items():
        if word in cl[1]:
            return cl[0]
    return -1


def classes_patterns(classes,sequences):
    res = set()
    for seq in sequences:
        pattern = ""
        for el in seq:
            val = classes_index(classes, el)
            if val != -1:
                pattern += " " + str(val)
            else:
                print("ERROR")
        pattern = pattern.strip(" ")
        res.add(pattern)
    print("class patterns: ")
    pp.pprint(res)
    return res

