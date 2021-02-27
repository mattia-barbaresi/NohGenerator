import json
import markov
import complexity

# input
# a = [[0, 1, 2, 3, 0, 1, 2, 4, 0, 1, 2, 4, 0, 1, 2, 4, ],
#      [7, 5],
#      [2, 1, 2, 1, 2, 1, 2]]
file_in = "markov/input.txt"
a = markov.read_from_file(file_in, "")


# markov trans_matrix(a)
res = markov.markov_trans_freq(a)
res2 = markov.detect_trans_probs(a,res)
markov.write_tp_seq(res2)
# print" ----------------"
# print "complexity: "
# print complexity.ngram_entropy(a[0],3)

# print" ----------------"
# print "result:"
# print json.dumps(res, indent=4, sort_keys=True)

# write
# with open("markov/markov.json", "w") as fp:
#     json.dump(res, fp)
