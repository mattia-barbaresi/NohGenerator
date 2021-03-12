import json
import pprint
import markov
import complexity


#
# According to the EPAM theory, when information is received by the sensory organs it initially undergoes an encoding
# process usually referred to as (i) feature extraction.
# (ii) The stimulus is then recognized on the basis of the features encoded by the feature extraction process,
# (iii) and a symbol is stored in short-term memory that “points to” or accesses the relevant information
# in semantic long-term memory.
#
#           sensory-perceptual front-end
#       ------------------------------------
#                     EPAM
#       ------------------------------------
#               semantic back-end
#


# read/init
file_in = "markov/input.txt"
separator = ""
sequences = markov.read_from_file(file_in, separator)
# init pp
pp = pprint.PrettyPrinter(indent=2)

# -----------------------------------------------------------
# compute transitions frequencies and extract tokens
tf = markov.markov_trans_freq(sequences)
# rewrite sequences with tf
tf_seqs = markov.detect_transitions(sequences,tf)
# tokenize sequences
tokens = markov.chunk_sequences(sequences,tf_seqs,6,separator)
# pp.pprint(tokens)
# -----------------------------------------------------------
# encoding sequences using tokens to calculate patterns
t_d = markov.dict_to_array(tokens)
tokenized = markov.chunks_detection(sequences,tokens, separator)
print("tokenized:")
pp.pprint(tokenized)
# convert dictionary levels in array
arr = []
for pat in tokenized.items():
    for sq in pat[1]:
        if sq:
            arr.append(list(str(x) for x in sq))

tf_tok = markov.markov_trans_freq(arr)
tf_tok_seq = markov.detect_transitions(arr,tf_tok)
patterns = markov.chunk_sequences(arr,tf_tok_seq,6)
t_p = markov.dict_to_array(patterns)
patternized = markov.chunks_detection(arr,patterns, separator)
print("patternized:")
pp.pprint(patternized)


# output  and to console
# markov.write_tp_file("tokens.txt",tf_seqs,sequences)
print(" ----------------")
# markov.write_tp_file("tokenized.txt",tf_tok_seq,arr)

# print (" ----------------")
# print ("results:")
# print (json.dumps(res, indent=4, sort_keys=True))

# write
# with open("markov/markov.json", "w") as fp:
#     json.dump(tf_seqs, fp)
