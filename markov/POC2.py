import time
from datetime import datetime
import json
import pprint
import markov
import os
import form_class as fc
from shutil import copyfile
import utils

# init, input, output
pp = pprint.PrettyPrinter(indent=2)
file_in = "markov/input/input.txt"
sep = ""
dir_out = "markov/results_POC2_" + datetime.now().strftime("%Y%m%d-%H.%M.%S") + "/"
os.mkdir(dir_out)
copyfile(file_in, dir_out + "input.txt")
###########################################################################

# read
sequences = utils.read_from_file(file_in, sep)

start_time = time.time()

# create model for generation
mdl = markov.create_generation_model(sequences)
# compute transitions frequencies
tf = markov.markov_trans_freq(sequences)
# count ngrams occurrences
ngrams = markov.ngram_occurrences(sequences)
# rewrite seqs with tf
tf_seqs = markov.detect_transitions(sequences, tf)
# tokenize seqs
chunks = markov.chunk_sequences(sequences, tf_seqs)
vocab = markov.dict_to_vocab(chunks)
detected = markov.chunks_detection(sequences, chunks)
#########################################################################
# form class
segmented = markov.chunks_detection(sequences, chunks, write_fun=markov.chunk_segmentation)
fc_seqs = segmented[3]
dc = fc.distributional_context(fc_seqs,3)
# print("---- dc ---- ")
# pp.pprint(dc)
classes = fc.form_classes(dc)
class_patt = fc.classes_patterns(classes,fc_seqs)


weights = [1,1,1,1,1]

gen = markov.generate_with_weights(mdl, weights)

evaluations = markov.evaluate(gen, class_patt)
