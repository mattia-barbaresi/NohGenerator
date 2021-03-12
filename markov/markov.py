#!/usr/bin/env python
import math
import os
import sys
import numpy as np


# for colored console out
class BColors:

    CYAN = '\033[96m'
    PURPLE = '\033[95m'
    BLUE = '\033[94m'
    YELLOW = '\033[93m'
    GREEN = '\033[92m'
    RED = '\033[91m'
    END = '\033[0m'


# parameters
class Params:
    # in max-entropy sequences each symbol has 1/N freq.
    TSH = 0.51


# sort key selector function
def _key_selector(x):
    return len(x)


# calculates frequency (occ./tot) of each ngram, as single set
def ngram_freq(seqs, order_limit=6):
    """
    This function computes overall frequencies for ngrams up to order-limit in seqs

    ...

    Parameters
    ----------
    seqs : matrix
        a 2D-array of integers
    order_limit : int
        the maximum ngram length calculated
    """

    dic = dict()
    for order in range(order_limit):
        _shape = (max(max(seqs)) + 1,) * (order + 1)
        m = np.zeros(_shape)
        dic[order] = {}
        for arr in seqs:
            for _ind in zip(*[arr[_x:] for _x in range(order + 1)]):
                m[_ind] += 1
        # divide all m by the sum
        m = np.divide(m, m.sum())
        for tt in zip(np.array(np.nonzero(m)).T):
            idx = "".join(str(e) for e in tt).strip('[]')
            dic[order][idx] = float(m[tuple(tt[0])])

    return dic


# calculates frequency (occ./tot) foreach ngram, foreach line
def ngram_freq_per_line(seqs, order_limit=6):
    """
    This function computes frequencies, for each line, for ngrams up to order-limit in seqs

    ...

    Parameters
    ----------
    seqs : matrix
        a 2D-array of integers
    order_limit : int
        the maximum ngram length calculated
    """

    dic = dict()
    for order in range(order_limit):
        dic[order] = dict()
        for arr in seqs:
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


# calculates markov transitional occurrences
def markov_trans_occ(seqs, order_limit=6):
    """This function computes transition occurrences dict up to order-limit

    ...

    Parameters
    ----------
    seqs : matrix
        a 2D-array of string
    order_limit : int
        the maximum ngram length calculated
    """
    dic = dict()
    for order in range(order_limit):
        dic[order] = dict()
        # init new dict for counting
        m = dict()
        for arr in seqs:
            # read and count n-grams in sequences
            for _ind in zip(*[arr[_x:] for _x in range(order + 1)]):
                val = " ".join(str(e) for e in _ind)
                val = val.strip()
                if val in m:
                    m[val] = m[val] + 1
                else:
                    m[val] = 1
            # count last-word transitions in n-grams
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


# calculates probabilities of markov transitions
def markov_trans_freq(seqs, order_limit=6):
    """This function computes conditional entropy dict up to order-limit

    ...

    Parameters
    ----------
    seqs : matrix
        a 2D-array of string
    order_limit : int
        the maximum ngram length calculated
    """
    cto = markov_trans_occ(seqs, order_limit)
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


# calculates probabilities of markov transitions
def markov_trans_prob(seqs, order_limit=6):
    """This function computes conditional entropy dict up to order-limit

    ...

    Parameters
    ----------
    seqs : matrix
        a 2D-array of string
    order_limit : int
        the maximum ngram length calculated
    """
    cto = markov_trans_occ(seqs, order_limit)
    m = dict()
    count_tot = 0
    for itm in cto.items():
        order = list(itm)
        m[order[0]] = dict()
        if order[0] > 0:
            # tot count for order
            order_tot = count_tot - order[0]
            # higher orders
            for itm2 in order[1].items():
                tpo = list(itm2)
                m[order[0]][tpo[0]] = dict()
                # count all transitions
                tot = sum(tpo[1].values())
                for x in tpo[1].items():
                    m[order[0]][tpo[0]][x[0]] = (float(x[1]) / int(tot)) / float(tot/order_tot)
        else:
            # 0th-order has no transitions
            tot = sum(order[1].values())
            count_tot = tot
            for x in order[1].items():
                m[order[0]][x[0]] = float(x[1]) / int(tot)
    return m


# switch tokens with their transitional probabilities in the given sequences
def detect_transitions(sequences, mtp):
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


# chunking sequences
def chunk_sequences(seqs, mtp, ord_max, separator=""):
    cl = dict()
    # cl = set()
    for order in range(1, ord_max):  # ignore 0th-order
        cl[order] = set()
        i = 0
        for x in mtp[order]:
            cks = ""
            j = 0
            while j < len(x):
                if str(x[j]) == "-" or float(x[j]) >= Params.TSH:
                    cks = cks + separator + str(seqs[i][j])
                else:
                    if cks != "":
                        cks = cks.strip(separator)
                        cl[order].add(cks)
                        # cl.add(cks)
                        cks = str(seqs[i][j])
                j = j + 1
            cks = cks.strip(separator)
            if cks != "" and cks != separator.join(seqs[i]):  # not store the entire sequences
                cl[order].add(cks)
                # cl.add(cks)
            i = i + 1
    return cl


def chunk_recognition(bag, pos, sq, separator=""):
    arr = []
    # first char
    search_str = ""
    i = 0
    while i < len(sq):
        search_str = separator.join(sq[i:])
        # search search_str in words bag
        # actually select the longer chunk

        # -------------------------------------------------------
        ind = -1
        # order chunks by ascending length and pick the first match
        for w in sorted(bag, key=_key_selector):
            if search_str.find(w) == 0:
                ind = pos.index(w)
        if ind > -1:
            # match
            match = str(ind)
            arr.append(match)
            if separator == "":
                i = i + len(pos[ind].split())
            else:
                i = i + len(pos[ind].split(separator))
        else:
            i = i + 1
            # if search_str is not empty, detection has failed

        # -------------------------------------------------------
    return arr


# rewrite sequences with chunks
def chunks_detection(seqs, chunks_dict, separator):
    # results
    res = dict()
    sorted_dict = dict_to_array(chunks_dict)
    for lvl in chunks_dict.items():
        res[lvl[0]] = []
        # foreach sequence
        for sq in seqs:
            arr = chunk_recognition(lvl[1], sorted_dict, sq, separator)
            if len(arr) > 0:
                res[lvl[0]].append(arr)
    return res


def dict_to_array(chunks_dict):
    app_set = set()
    # create one array of words
    for lvl in chunks_dict.items():
        app_set = app_set | (lvl[1])
    sorted_dict = sorted(app_set, key=_key_selector)
    # print("sorted_dict: ", sorted_dict)
    return sorted_dict


# write tps instead of token in sequences
def write_tp_file(file_name, tps, seqs, console=True):
    """
    write transitional probabilities sequences for each order in file and console.

    ...

    Parameters
    ----------

    file_name : str
        the name of the file
    tps : dict
        the transitional probabilities dictionary
    seqs: list of str
        input sequences
    console : bool
        If True print (colored) tps in (Python) console too
    """
    with open(os.path.join(sys.path[0], file_name), "w") as fp:
        for ind in tps.keys():
            fp.write(str(ind) + ":\n")
            i = 0
            for item in tps[ind]:
                i += 1
                # vl to write
                vl = ""
                # vl2 to print
                vl2 = ""
                j = 0
                for x in item:
                    if x != "-":
                        rs = round(x, 2)
                        if rs < Params.TSH:
                            clr = BColors.RED
                        else:
                            clr = BColors.BLUE
                        # vl2 += clr + '(' + str(rs) + ')' + BColors.END + '\t'
                        vl2 += clr + str(seqs[i - 1][j]) + BColors.END + ' '
                        vl += '(' + str(round(x, 2)) + ')\t'
                    else:
                        # vl2 += ' (' + x + ') \t'
                        vl2 += x + ' '
                        vl += ' (' + x + ') \t'
                    j += 1
                if console:
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
    with open(file_name, encoding="utf8") as fp:
        for line in fp:
            if separator == "":
                a = list(line.strip())
            else:
                a = line.strip().split(separator)
            lst.append(a)
    return lst


# generate a sequence starting from initial symbol
# def generate(tps, init_symbol):
#     res = dict()
#     lvl = 0
#     past = ""
#     # num of symbols to generate
#     for o in range(5):
#         res[o] = set()
#         for n in tps[o]:
#             for v in n:
#                 res[o].update(n.split())
#     print(res)
