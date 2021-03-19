from datetime import datetime
import json
import pprint
import markov
import os
import complexity


# --------------------------------------------------functions
# call fun
def compute(seqs, dir_name, filename):
    # compute transitions frequencies
    tf = markov.markov_trans_freq(seqs)
    # rewrite seqs with tf
    tf_seqs = markov.detect_transitions(seqs, tf)
    # tokenize seqs
    chunks = markov.chunk_sequences(seqs, tf_seqs)
    vocab = markov.dict_to_array(chunks)
    detected = markov.chunks_detection(seqs, chunks)
    # write
    with open(dir_name + filename + "_tf.json", "w") as fp:
        json.dump(tf, fp)
    with open(dir_name + filename + "_tf_seqs.json", "w") as fp:
        json.dump(tf_seqs, fp)
    with open(dir_name + filename + "_chunks.json", "w") as fp:
        json.dump(chunks, fp, default=serialize_sets)
    with open(dir_name + filename + "_vocab.json", "w") as fp:
        json.dump(vocab, fp)
    with open(dir_name + filename + "_detected.json", "w") as fp:
        json.dump(detected, fp)
    return tf, chunks, vocab, detected


# serialize sets
def serialize_sets(obj):
    if isinstance(obj, set):
        return list(obj)
    return obj


# init, input, output
pp = pprint.PrettyPrinter(indent=2)
file_in = "markov/input.txt"
dir_out = "markov/results_" + datetime.now().strftime("%Y%m%d-%H.%M") + "/"
os.mkdir(dir_out)
sequences = markov.read_from_file(file_in, "")
new_seqs = sequences

# compute tokens
tkn_tf, tokens, token_vocabulary, tokenized = compute(sequences, dir_out, "tokens")

# convert tokenized to arr
arr = []
for pat in tokenized.items():
    # convert dictionary levels in array
    for sq in pat[1]:
        if sq:
            arr.append(list(str(x) for x in sq))

# compute patterns
pat_tf, patterns, pattern_vocabulary, patternized = compute(arr, dir_out, "patterns")


# generation
markov.generate(token_vocabulary, pat_tf, pattern_vocabulary, 10)


# output  and to console
# markov.write_tp_file("tokens.txt",tf_seqs,sequences)
# print(" ----------------")
# markov.write_tp_file("tokenized.txt",tf_tok_seq,arr)

# print (" ----------------")
# print ("results:")
# print (json.dumps(res, indent=4, sort_keys=True))

# write
# markov.write_tp_file(dir_out + "blabla",tf_seqs,sequences, False)
# markov.write_tp_file(dir_out + "blabla",tf_tok_seq,arr, False)
