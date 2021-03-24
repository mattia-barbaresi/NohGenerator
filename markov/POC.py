import time
from datetime import datetime
import json
import pprint
import markov
import os
import complexity
from shutil import copyfile


# convert fun
def dict_to_arr(tkn_dict):
    res = []
    for pat in tkn_dict.items():
        # convert dictionary levels in array
        for sq in pat[1]:
            if sq:
                res.append(list(str(x) for x in sq))
    return res


# ----------------------------------------------------------
# init, input, output
pp = pprint.PrettyPrinter(indent=2)
file_in = "input/input.txt"
dir_out = "markov/results_" + datetime.now().strftime("%Y%m%d-%H.%M") + "/"
os.mkdir(dir_out)
copyfile(file_in, dir_out+"input.txt")
sequences = markov.read_from_file(file_in, " ")
new_seqs = sequences
start_time = time.time()
# compute tokens
tkn_tf, tkn_tf_seq, tokens, token_vocabulary, tokenized = markov.compute(sequences, dir_out, "tokens")
# convert tokenized to arr
arr = dict_to_arr(tokenized)
# compute patterns
pat_tf, pat_tf_seq, patterns, pattern_vocabulary, patternized = markov.compute(arr, dir_out, "patterns")
tf = pat_tf
vocabulary = token_vocabulary

# --------------------------------
# generate in a loop
# arr = sequences
# vocab = []
# for _i in range(2):
#     # compute tokens
#     vocabulary = vocab
#     tf, tf_seq, segments, vocab, seg_seqs = markov.compute(arr, dir_out, "gen_" + str(_i))
#     # convert tokenized to arr
#     arr = dict_to_arr(seg_seqs)
# --------------------------------

# generate new sequences
generated = markov.generate(tf, 10)
# translate to tokens
t2 = markov.translate(generated, vocabulary)

with open(dir_out + "generated.json", "w") as fp:
    json.dump(generated, fp, default=markov.serialize_sets)
with open(dir_out + "translated.json", "w") as fp:
    json.dump(t2, fp, default=markov.serialize_sets, ensure_ascii=False)

# output  and to console
# print (" ----------------")
# print ("results:")
print("time elapsed :", time.time() - start_time)
# print (json.dumps(res, indent=4, sort_keys=True))

# write
# markov.write_tp_file(dir_out + "blabla",tkn_tf_seq,sequences, False)
# markov.write_tp_file(dir_out + "blabla",pat_tf_seq,,arr, False)



