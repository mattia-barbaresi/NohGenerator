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
#
# in "An Information-Processing Theory of Some Effects of Similarity, Familiarization, and Meaningfulness in Verbal
# Learning" - (Herbert A. Simon and Edward A. Feigenbaum, 1964)


# -------------------------------------------------- init, read input
pp = pprint.PrettyPrinter(indent=2)
# read
file_in = "markov/input.txt"
sequences = markov.read_from_file(file_in, " ")
new_seqs = sequences

# -------------------------------------------------- tokens
# compute transitions frequencies
tf = markov.markov_trans_freq(sequences)
# rewrite sequences with tf
tf_seqs = markov.detect_transitions(sequences,tf)
# tokenize sequences
tokens = markov.chunk_sequences(sequences,tf_seqs,6)
token_vocabulary = markov.dict_to_array(tokens)
tokenized = markov.chunks_detection(sequences,tokens)

# -------------------------------------------------- patterns
arr = []
for pat in tokenized.items():
    # convert dictionary levels in array
    for sq in pat[1]:
        if sq:
            arr.append(list(str(x) for x in sq))

# encoding sequences using tokens to calculate patterns
tf_tok = markov.markov_trans_freq(arr)
tf_tok_seq = markov.detect_transitions(arr,tf_tok)
# patternize sequences
patterns = markov.chunk_sequences(arr,tf_tok_seq,6)
pattern_vocabulary = markov.dict_to_array(patterns)
patternized = markov.chunks_detection(arr,patterns)

# markov.generate(tf, token_vocabulary, tf_tok, pattern_vocabulary,10)
# markov.detect(new_seqs, token_vocabulary, pattern_vocabulary)

# -------------------------------------------------- output  and to console

# markov.write_tp_file("tokens.txt",tf_seqs,sequences)
# print(" ----------------")
# markov.write_tp_file("tokenized.txt",tf_tok_seq,arr)

# print (" ----------------")
# print ("results:")
# print (json.dumps(res, indent=4, sort_keys=True))

# write
# with open("markov/markov.json", "w") as fp:
#     json.dump(tf_seqs, fp)
# markov.write_tp_file("blabla",tf_seqs,sequences)
# markov.write_tp_file("blabla",tf_tok_seq,arr)
