#!/usr/bin/env python

import os
import sys

import numpy as np


# for colored console out
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    RED = '\033[31m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


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
                t1 = (tt[0].split(" "))
                if len(t1) > 1:
                    i1 = ' '.join(t1[:-1])  # trim last char
                    i2 = str(t1[-1])
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


# switch tokens in sequences with their transitional probabilities
def detect_trans_probs(sequences, mtp):
    """
    Read a list of sequences and switch each occurrence with its transitional probability.

    ...

    Parameters
    ----------
    sequences : matrix
    list of sequences to analyze
    mtp : dict
    the transitional probabilities dictionary
    """
    res = dict()
    for order in mtp.items():
        res[order[0]] = list()
        for seq in sequences:
            if len(seq) > int(order[0]):
                sq = list()
                # fill in initial n (#order)empty chars
                for i in range(order[0]):
                    sq.append("-")
                for _ind in zip(*[seq[_x:] for _x in range(order[0] + 1)]):
                    i1 = " ".join(_ind[:-1])  # trim last space
                    i2 = str(_ind[-1])
                    if not i1:
                        # order 1 ..then takes each tokens
                        ns = order[1][i2]
                    else:
                        # high order ..is a dict
                        ns = order[1][i1][i2]
                    sq.append(ns)
                res[order[0]].append(sq)
            else:
                # sequence too short
                res[order[0]].append([])
    return res


# write tps instead of token in sequences
def write_tp_seq(tps):
    """
        write transitional probabilities sequences for each order in file and console.

        ...

        Parameters
        ----------
        tps : dict
        the transitional probabilities dictionary
        """
    with open(os.path.join(sys.path[0], "out_tps.txt"), "w") as fp:
        for ind in tps.keys():
            fp.write(str(ind) + ":\n")
            print (str(ind) + ":\n")
            for item in tps[ind]:
                # vl to write
                vl = ""
                # vl2 to print
                vl2 = ""
                for x in item:
                    if x != "-":
                        rs = round(x, 2)
                        clr = bcolors.OKGREEN
                        if rs < 0.3:
                            clr = bcolors.OKCYAN
                        elif rs > 0.7:
                            clr = bcolors.RED
                        vl2 += clr + '(' + str(rs) + ')' + bcolors.ENDC + '\t'
                        vl += '(' + str(round(x, 2)) + ')\t'
                    else:
                        vl2 += ' (' + x + ') \t'
                        vl += ' (' + x + ') \t'
                print(vl2)
                fp.write(vl + "\n")


# reads list of sequences from file
def read_from_file(file_name, separator=""):
    """
    Read a list of strings and split into tokens using separator.

    ...

    Parameters
    ----------
    separator : str
        separator between tokens, used to split sequences
    file_name : str
        the name of the file to read
    """
    lst = []
    with open(file_name) as fp:
        for line in fp:
            if separator == "":
                a = list(line.strip())
            else:
                a = line.strip().split(separator)
            lst.append(a)
    return lst
