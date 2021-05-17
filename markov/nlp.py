# guide: https://realpython.com/python-nltk-sentiment-analysis/
import string
from pprint import pprint
import nltk
import form_class as fc
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
import matplotlib.pyplot as plt
from nltk.sentiment import SentimentIntensityAnalyzer

import utils

# read file
with open("input/aladdin.txt", 'r') as fp:
    text = fp.read()

# text = text.lower().translate(str.maketrans('', '', string.punctuation))
text = text.lower()

filtered_sent = []
tags = nltk.pos_tag(nltk.word_tokenize(text))
for word,pos in tags:
    # nouns, adjectives, verbs, adverbs
    if "NN" in pos or "JJ" in pos or "VB" in pos or "RB" in pos:
        filtered_sent.append(word)

ps = PorterStemmer()
stemmed_words = ""
for w in filtered_sent:
    stemmed_words += " " + ps.stem(w)

# words = nltk.word_tokenize(stemmed_words)
# fdist = nltk.FreqDist(words)
# fdist.plot(cumulative=False)
# plt.show()


# classes
seqs = utils.read_from_file("input/aladdin.txt", " ")
seqs_clean = []
for seq in seqs:
    seqs_clean.append(list(x.lower().translate(str.maketrans('', '', string.punctuation)) for x in seq))
dc = fc.distributional_context(seqs,5)
cls = fc.form_classes(dc)
cp = fc.classes_patterns(cls,seqs)
# print(cp)
