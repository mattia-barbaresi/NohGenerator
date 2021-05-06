# count pre- and post- occurrences for each word to find form classes
from collections import OrderedDict

import numpy as np
import pprint

pp = pprint.PrettyPrinter(indent=2)


# records pre- and post- lists of words (and the number of occurrences of each of them) that come
# before and after each word in sequences
def distributional_context(sequences, order=1):
    res = dict()
    for seq in sequences:
        for el in seq:
            if el not in res:
                res[el] = dict()
                for i in range(1, order + 1):
                    res[el][-i] = dict()
                    res[el][+i] = dict()
                    for search_seq in sequences:
                        values = np.array(search_seq)
                        for index in np.where(values == el)[0]:
                            # sx occurrence
                            if index >= i:
                                if values[index - i] in res[el][-i]:
                                    res[el][-i][values[index - i]] += 1
                                else:
                                    res[el][-i][values[index - i]] = 1
                            # dx occurrence
                            if index < len(values) - i:
                                if values[index + i] in res[el][+i]:
                                    res[el][+i][values[index + i]] += 1
                                else:
                                    res[el][+i][values[index + i]] = 1
                    # order results
                    res[el][+i] = OrderedDict(sorted(res[el][+i].items(), key=lambda x: x[1], reverse=True))
                    res[el][-i] = OrderedDict(sorted(res[el][-i].items(), key=lambda x: x[1], reverse=True))
    return res


# evaluates form classes
def form_classes(dist_ctx):
    # print initial and ending classes
    first_set = []
    last_set = []
    pp.pprint(dist_ctx)
    for word in dist_ctx.items():
        if not word[1][-1]:
            first_set.append(word[0])
        if not word[1][1]:
            last_set.append(word[0])
    print("first: ", first_set)
    print("last: ", last_set)
