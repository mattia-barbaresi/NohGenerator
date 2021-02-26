#!/usr/bin/env python
import json

import numpy as np


# calculates frequency (occ./tot) of each ngram, as single set
def ngram_freq(mtx, order_limit=6):
    """This function computes overall frequencies for ngrams up to order-limit in mtx

        ...

        Parameters
        ----------
        mtx : matrix
            a 2D-array of integers
        order_limit : int
            the maximum ngram length calculated
    """

    dic = dict()
    for order in range(order_limit):
        _shape = (max(max(mtx)) + 1,) * (order + 1)
        m = np.zeros(_shape)
        dic[order] = {}
        for arr in mtx:
            for _ind in zip(*[arr[_x:] for _x in range(order + 1)]):
                m[_ind] += 1
        # divide all m by the sum
        m = np.divide(m, m.sum())
        for tt in zip(np.array(np.nonzero(m)).T):
            idx = "".join(str(e) for e in tt).strip('[]')
            dic[order][idx] = float(m[tuple(tt[0])])

    return dic


# calculates frequency (occ./tot) foreach ngram, foreach line
def ngram_freq_per_line(mtx, order_limit=6):
    """This function computes frequencies, for each line, for ngrams up to order-limit in mtx

        ...

        Parameters
        ----------
        mtx : matrix
            a 2D-array of integers
        order_limit : int
            the maximum ngram length calculated
    """

    dic = dict()
    for order in range(order_limit):
        dic[order] = dict()
        for arr in mtx:
            if len(arr) > order:
                _shape = (max(arr) + 1,) * (order + 1)
                m = np.zeros(_shape)
                for _ind in zip(*[arr[_x:] for _x in range(order + 1)]):
                    m[_ind] += 1
                # divide each cell with the row sum
                m = (m.T / m.sum()).T
                for tt in zip(np.array(np.nonzero(m)).T):
                    idx = "".join(str(e) for e in tt).strip('[]')
                    dic[order][idx] = float(m[tuple(tt[0])])
    return dic


# calculates transitional occurrences for markov models
def markov_trans_occ(mtx, order_limit=6):
    """This function computes transition occurrences dict up to order-limit

        ...

        Parameters
        ----------
        mtx : matrix
            a 2D-array of string
        order_limit : int
            the maximum ngram length calculated
    """
    dic = dict()
    for order in range(order_limit):
        dic[order] = dict()
        for arr in mtx:
            m = dict()
            for _ind in zip(*[arr[_x:] for _x in range(order + 1)]):
                val = " ".join(str(e) for e in _ind)
                val = val.strip()
                if val in m:
                    m[val] = m[val] + 1
                else:
                    m[val] = 1
            for tt in m.items():
                if len(tt[0]) > 1:
                    i1 = tt[0][:-2]  # trim last space
                    i2 = tt[0][-1]
                    if i1 in dic[order]:
                        dic[order][i1][i2] = tt[1]
                    else:
                        dic[order][i1] = dict()
                        dic[order][i1][i2] = tt[1]
                else:
                    dic[order][tt[0]] = tt[1]
    return dic


# calculates markov
def markov_trans_freq(mtx, order_limit=6):
    """This function computes transition frequencies dict up to order-limit

            ...

            Parameters
            ----------
            mtx : matrix
                a 2D-array of string
            order_limit : int
                the maximum ngram length calculated
        """
    cto = markov_trans_occ(mtx, order_limit)
    m = dict()
    for itm in cto.items():
        order = list(itm)
        m[order[0]] = dict()
        if order[0] > 0:
            # higher orders
            for itm2 in order[1].items():
                tpo = list(itm2)
                m[order[0]][tpo[0]] = dict()
                tot = sum(tpo[1].values())
                for x in tpo[1].items():
                    m[order[0]][tpo[0]][x[0]] = float(x[1]) / int(tot)
        else:
            # 0th-order has no transitions
            tot = sum(order[1].values())
            for x in order[1].items():
                m[order[0]][x[0]] = float(x[1]) / int(tot)
    return m
