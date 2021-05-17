#!/usr/bin/env python
import json
import random
import numpy as np
import pprint
import form_class as fc
from collections import OrderedDict

pp = pprint.PrettyPrinter(indent=2)


# for colored console out
class BColors:
    def __init__(self):
        pass

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
    def __init__(self):
        pass

    TSH = 0.7


# sort key selector function
def _key_selector(x):
    return len(x)


# calculates frequency (occ./tot) of each ngram, as single set
def ngram_occurrences(seqs, order_limit=6, sort=True):
    """
    This function computes overall frequencies for ngrams up to order-limit in seqs

    ...

    Parameters
    ----------
    seqs : matrix
        a list of sequences
    order_limit : int
        the maximum ngram length calculated
    sort: bool
        if True, sort results
    """

    dic = dict()
    for order in range(order_limit):
        dic[order] = {}
        for arr in seqs:
            for _ind in zip(*[arr[_x:] for _x in range(order + 1)]):
                val = "".join(_ind)
                if val in dic[order]:
                    dic[order][val] += 1
                else:
                    dic[order][val] = 1
    if sort:
        for k in dic.keys():
            dic[k] = OrderedDict(sorted(dic[k].items(), key=lambda item: int(item[1]), reverse=True))
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
                val = val.strip(" ")
                if val in m:
                    m[val] = m[val] + 1
                else:
                    m[val] = 1
            # count last-word transitions in n-grams
            for tt in m.items():
                # warning: double spaces give an error!
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
    """This function computes transition frequencies dict up to order-limit

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
    t_tot = 0
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
            t_tot = sum(order[1].values())
            for x in order[1].items():
                m[order[0]][x[0]] = float(x[1]) / int(t_tot)
    return m

    # calculates probabilities of markov transitions


# calculates chunk strength markov transitions
def markov_chunk_strength(seqs, order_limit=6):
    """This function computes chunk strengths dict up to order-limit

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
                    # chunk strength
                    m[order[0]][tpo[0]][x[0]] = float(x[1] - ((int(tot) - x[1]) * 0.5))
        else:
            # 0th-order has no transitions
            tot = sum(order[1].values())
            for x in order[1].items():
                # chunk strength
                m[order[0]][x[0]] = float(x[1] - ((int(tot) - x[1]) * 0.5))
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
                    m[order[0]][tpo[0]][x[0]] = (float(x[1]) / int(tot)) / float(tot / order_tot)
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
def chunk_sequences(seqs, mtp, orders=[2,3]):
    """
    Returns segments/chunks of seqs extracted using mtp transitions

    ...

    Parameters
    ----------
    seqs : matrix
        list of sequences to analyze
    mtp : dict
        the transitional probabilities dictionary
    orders : list
        orders in dict
    """
    cl = dict()
    # cl = set()
    for order in orders:  # ignore 0th-order
        cl[order] = set()
        i = 0
        for x in mtp[order]:
            cks = ""
            j = 0
            while j < len(x):
                if str(x[j]) == "-" or float(x[j]) >= Params.TSH:
                    cks = cks + " " + str(seqs[i][j])
                else:
                    if cks != "":
                        cks = cks.strip(" ")
                        cl[order].add(cks)
                        # cl.add(cks)
                        cks = str(seqs[i][j])
                j = j + 1
            cks = cks.strip(" ")
            if cks != "" and cks != " ".join(seqs[i]):  # not store the entire sequences
                cl[order].add(cks)
                # cl.add(cks)
            i = i + 1
    return cl


# chunking sequences
def chunk_sequences_only_sure(seqs, mtp, ord_max=6):
    """
    Returns segments/chunks of seqs extracted using mtp transitions

    ...

    Parameters
    ----------
    seqs : matrix
        list of sequences to analyze
    mtp : dict
        the transitional probabilities dictionary
    ord_max : int
        max level/order in dict
    """
    cl = dict()
    # cl = set()
    for order in range(1, ord_max):  # ignore 0th-order
        cl[order] = set()
        i = 0
        for x in mtp[order]:
            cks = ""
            j = 0
            while j < len(x):
                if str(x[j]) == "-" or float(x[j]) >= 0.98:
                    # concat new char
                    cks = cks + " " + str(seqs[i][j])
                else:
                    # add founded chunk, if any
                    if len(cks.strip(" ").split(" ")) > 1:
                        cks = cks.strip(" ")
                        if cks.strip(" ") == "f":
                            print("m")
                        cl[order].add(cks)
                        # cl.add(cks)
                    # start new chunk
                    cks = str(seqs[i][j])
                j = j + 1
            cks = cks.strip(" ")
            i = i + 1
    return cl


def chunk_recognition(bag, voc, sq):
    """
    Return the list of token (in bag) that match sq
    """
    arr = []
    # first char
    i = 0
    while i < len(sq):
        search_str = " ".join(sq[i:])
        # search search_str in words bag
        # actually select the longer chunk that match initial position in search_str
        ind = -1
        # order chunks by ascending length and pick the first match
        for w in sorted(bag, key=_key_selector):
            if search_str.find(w) == 0:
                ind = voc.index(w)
        if ind > -1:
            # match
            match = str(ind)
            arr.append(match)
            i = i + len(voc[ind].split(" "))
        else:
            i = i + 1
    return arr


def chunk_segmentation(bag, pos, sq):
    """
    Return the list of token (in bag) that match sq
    """
    arr = []
    # first char
    i = 0
    while i < len(sq):
        search_str = " ".join(sq[i:])
        # search search_str in words bag
        # actually select the longer chunk that match initial position in search_str
        ind = ""
        # order chunks by ascending length and pick the first match
        for w in sorted(bag, key=_key_selector):
            if search_str.find(w) == 0:
                ind = w
        if ind:
            # match
            arr.append(ind)
            i = i + len(ind.split(" "))
        else:
            i = i + 1
        # if search_str is not empty, detection has failed
    return arr


# rewrite sequences with chunks
def chunks_detection(seqs, chunks_dict, write_fun=chunk_recognition):
    """
    Return seqs converted using tokens/chunks
    """
    # results
    res = dict()
    vocab = dict_to_vocab(chunks_dict)
    for lvl in chunks_dict.items():
        res[lvl[0]] = []
        # foreach sequence
        for sq in seqs:
            arr = write_fun(lvl[1], vocab, sq)
            if len(arr) > 0:
                res[lvl[0]].append(arr)
    return res


def dict_to_vocab(chunks_dict):
    """
    Collect values in a set then convert the set in a (ordered) list
    """
    app_set = set()
    # create one array of words
    for lvl in chunks_dict.items():
        app_set = app_set | (lvl[1])
    sorted_dict = sorted(app_set, key=_key_selector)
    # print("sorted_dict: ", sorted_dict)
    return sorted_dict


# write tps instead of token in sequences
def write_tp_file(path, tps, seqs, console=True):
    """
    write transitional probabilities sequences for each order in file and console.

    ...

    Parameters
    ----------

    path : str
        the name of the file
    tps : dict
        the transitional probabilities dictionary
    seqs: list of str
        input sequences
    console : bool
        If True print (colored) tps in (Python) console too
    """
    with open(path, "w") as fp:
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


# return an index using MonteCarlo choice on arr
def mc_choice(arr):
    rnd = random.uniform(0, 1)
    sm = arr[0]
    j = 1
    ind = 0
    while sm < rnd:
        sm += float(arr[j])
        if sm >= rnd:
            ind = j
        j += 1
    return ind


# from transition probabilities, generates (occ) sequences
def generate(tps, n_seq, occ_per_seq=16):
    res = dict()
    for order in tps.keys():
        res[order] = list()
        if int(order) == 0:
            for _ns in range(0, n_seq):
                str_res = ""
                for _ops in range(0, occ_per_seq):
                    idx = mc_choice(list(tps[order].values()))
                    str_res += " " + list(tps[order].keys())[idx]
                res[order].append(str_res.strip(" "))
        else:
            for _ns in range(0, n_seq):
                # first choice
                str_res = random.choice(list(tps[order].keys()))
                sid = str_res
                # all other occs
                for _ops in range(0, occ_per_seq - order):
                    #  ending symbol, no further nth-order transition
                    # cut first symbol and search for the order-1 transition
                    i = 0
                    while i < order and (sid not in tps[order - i].keys()):
                        sid = " ".join(sid.split(" ")[1:])
                        i += 1
                    if sid:
                        val = tps[order - i][sid]
                        idx = mc_choice(list(val.values()))
                        str_res += " " + list(val.keys())[idx]
                    else:
                        # choose a symbol of the 0-th level
                        idx = mc_choice(list(tps[0].values()))
                        val = list(tps[0].keys())[idx]
                        str_res += " " + val

                    sid = " ".join(str_res.split(" ")[-order:])
                res[order].append(str_res)
    return res


def generate_with_weights(tps, weights, voc=[], n_seq=1, occ_per_seq=16, start_pool=[]):
    res = []
    # generate n_seq sequences
    for _ns in range(0, n_seq):
        # start symbol
        if start_pool:
            str_res = random.choice(list(start_pool))
        else:
            str_res = mc_choice_dict(tps[0])
        # all other symbols
        # generate occ_per_seq symbols (per sequence)
        trans = str_res
        if voc:
            trans = translate_sequence(str_res,voc)
        while len(trans.split(" ")) < occ_per_seq:
            # pick out the order
            order = mc_choice(weights)
            if order == 0:
                # if order = 0 pick out a random symbol
                str_res += " " + mc_choice_dict(tps[0])
            else:
                # no further transition
                # cut first symbol and search for the order-1 transition
                i = 0
                # pick out the right history (past length due to choosen order)
                sid = " ".join(str_res.split(" ")[-order:])
                while i < order and (sid not in tps[order - i].keys()):
                    sid = " ".join(sid.split(" ")[1:])
                    i += 1
                if sid and (order - i > 0):
                    val = tps[order - i][sid]
                    idx = mc_choice(list(val.values()))
                    str_res += " " + list(val.keys())[idx]
                else:
                    # choose a symbol of the 0-th level
                    idx = mc_choice(list(tps[0].values()))
                    val = list(tps[0].keys())[idx]
                    str_res += " " + val
            trans = str_res
            if voc:
                trans = translate_sequence(str_res, voc)
        res.append(str_res)
    return res


# convert symbols in sequences using vocabulary
def translate(sequences, vocabulary):
    res = dict()
    for itm in sequences.items():
        res[itm[0]] = list()
        for seq in itm[1]:
            tks = [int(x) for x in seq.split(" ")]
            sym = " ".join(np.array(vocabulary)[tks])
            res[itm[0]].append(sym)
    return res


def translate_sequence(sequence, vocabulary):
    res = ""
    tks = [int(x) for x in sequence.split(" ")]
    sym = " ".join(np.array(vocabulary)[tks])
    res += sym
    return res


# detect input seqs using token and patter vocabs
def detect(seqs, token_voc, pattern_voc, ):
    pass


# serialize sets as list
def serialize_sets(obj):
    if isinstance(obj, set):
        return list(obj)
    return obj


def create_generation_model(seqs):
    cto = markov_trans_occ(seqs)
    m = dict()
    t_tot = 0
    for itm1 in cto.items():
        if itm1[0] > 0:
            # higher orders
            for itm2 in itm1[1].items():
                vec = itm2[0].split(" ")
                curr = vec[-1]
                if curr not in m:
                    m[curr] = dict()
                past = ""
                if len(vec) > 1:
                    past = " ".join(vec[:-1])
                m[curr][past] = dict()
                tot = sum(itm2[1].values())
                for x in itm2[1].items():
                    m[curr][past][x[0]] = float(x[1]) / int(tot)
        else:
            m["0th"] = dict()
            # 0th-order has no transitions
            t_tot = sum(itm1[1].values())
            for x in itm1[1].items():
                m["0th"][x[0]] = float(x[1]) / int(t_tot)
    return m


def mc_choice_dict(a_dict):
    rnd = random.uniform(0, 1)
    ind = -1
    sm = 0
    for k,v in a_dict.items():
        sm += v
        if sm >= rnd:
            ind = k
            break
    return ind


# def reweight(pool, ws):
#     res = []
#     np.multiply(a, w)
#     out2 = [x / ss for x in out]
#
#     return re

#
# def mdl_generate_with_weights(mdl, weights, noccs, init_pool):
#     res = []
#     seq = ""
#     if init_pool:
#         seq = random.choice(init_pool)
#     else:
#         seq = mc_choice_dict(mdl["0th"])
#     res.append(seq)
#     # next trans
#     pool = reweight(mdl[seq], weights)
#     for n in range(0,noccs):
#         res.append()
#
#
# def mdl_generate_with_weights_iter(mdl, weights, ll, init_pool=[]):
#     n = 100
#     results = []
#     for i in range(0,100):
#         results.append(mdl_generate_with_weights(mdl, weights, ll, init_pool))
#     return results


# -------------------------------------------------------------------------
# call fun
def compute(seqs, dir_name="noDir", filename="noName", write_to_file=True):
    # create model for generation
    # mdl = create_generation_model(seqs)
    # compute transitions frequencies
    tf = markov_trans_freq(seqs)
    # count ngrams occurrences
    ngrams = ngram_occurrences(seqs)
    # ...or chunk strength
    # tf = markov_chunk_strength(seqs)
    # rewrite seqs with tf
    tf_seqs = detect_transitions(seqs, tf)
    # tokenize seqs
    chunks = chunk_sequences(seqs, tf_seqs)
    # chunks_sure = chunk_sequences_only_sure(seqs, tf_seqs)
    vocab = dict_to_vocab(chunks)
    detected = chunks_detection(seqs, chunks)
    #########################################################################
    # form class
    segmented = chunks_detection(seqs, chunks, write_fun=chunk_segmentation)
    fc_seqs = segmented[3]
    dc = fc.distributional_context(fc_seqs,3)
    # print("---- dc ---- ")
    # pp.pprint(dc)
    classes = fc.form_classes(dc)
    class_patt = fc.classes_patterns(classes,fc_seqs)

    #########################################################################
    # write
    if write_to_file:
        # with open(dir_name + filename + "_mdl.json", "w") as fp:
        #     json.dump(mdl, fp, default=serialize_sets)
        with open(dir_name + filename + "_tf.json", "w") as fp:
            json.dump(tf, fp)
        with open(dir_name + filename + "_tf_seqs.json", "w") as fp:
            json.dump(tf_seqs, fp)
        with open(dir_name + filename + "_chunks.json", "w") as fp:
            json.dump(chunks, fp, default=serialize_sets)
        # with open(dir_name + filename + "_chunks_sure.json", "w") as fp:
        #     json.dump(chunks_sure, fp, default=serialize_sets)
        with open(dir_name + filename + "_vocab.json", "w") as fp:
            json.dump(vocab, fp)
        with open(dir_name + filename + "_detected.json", "w") as fp:
            json.dump(detected, fp)
        with open(dir_name + filename + "_segmented.json", "w") as fp:
            json.dump(segmented, fp)
        with open(dir_name + filename + "_ngrams.json", "w") as fp:
            json.dump(ngrams, fp, )
        with open(dir_name + filename + "_contexts.json", "w") as fp:
            json.dump(dc, fp, default=serialize_sets)
        with open(dir_name + filename + "_form_classes.json", "w") as fp:
            json.dump(classes, fp, default=serialize_sets)
        with open(dir_name + filename + "_class_patterns.json", "w") as fp:
            json.dump(class_patt, fp, default=serialize_sets)
    return tf, tf_seqs, chunks, vocab, detected, classes, class_patt
