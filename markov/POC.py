import json
import markov
import complexity

file_in = "markov/input.txt"
# tokenize
a = markov.read_from_file(file_in, " ")
# calculate markov frequencies
res = markov.markov_trans_freq(a)
# rewrite sequences with tps
res2 = markov.detect_transitions(a,res)
# output
markov.write_tp_seq(res2)

print (" ----------------")
print ("complexity: ")
print (complexity.ngram_entropy(a[0],3))
print (" ----------------")
print ("results:")
print (json.dumps(res, indent=4, sort_keys=True))
print (json.dumps(res2, indent=4, sort_keys=True))

# write
with open("markov/markov.json", "w") as fp:
    json.dump(res, fp)
