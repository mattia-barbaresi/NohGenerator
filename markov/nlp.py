# guide: https://realpython.com/python-nltk-sentiment-analysis/

from pprint import pprint
import nltk
import form_class as fc
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
import matplotlib.pyplot as plt
from nltk.sentiment import SentimentIntensityAnalyzer

import utils

seqs = utils.read_from_file("input/noh.txt", " ")
dc = fc.distributional_context(seqs)
cls = fc.form_classes(dc)
cp = fc.classes_patterns(cls,seqs)
# print(cp)

# read file
with open("input/noh.txt", 'r') as fp:
    text = fp.read()

sia = SentimentIntensityAnalyzer()
ps = sia.polarity_scores(text)
# print(ps)

stop_words = set(stopwords.words("english"))
tokenized_text = nltk.sent_tokenize(text)
filtered_sent = []
for w in tokenized_text:
    if w not in stop_words:
        filtered_sent.append(w)

ps = PorterStemmer()
stemmed_words = ""
for w in filtered_sent:
    stemmed_words += "" + ps.stem(w)

words = nltk.word_tokenize(stemmed_words)
fdist = nltk.FreqDist(words)
fdist.plot(cumulative=False)
plt.show()
