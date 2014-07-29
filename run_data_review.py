from datetime import datetime
from review_data import *
import sys
import cPickle
import os


os.chdir(sys.argv[1])

# data = buildSubsetData(sys.argv[1], ["word", "date", "count"], "date", 5000)
# print "got test data"

data = buildData(sys.argv[2], ["word", "date", "node", "count"], "date")
data = data[data["date"] > datetime(2014, 1, 1)]
print "got real data"

cPickle.dump(data, open(sys.argv[3], "wb"))

# monthly word count
m_word_count = monthlyWordCount(data)
plotMonthlyWordC(m_word_count, sys.argv[4])

# unique monthly word count
um_word_count = monthlyUniqueWordC(data)
plotMonthlyUniqueWordC(um_word_count, sys.argv[5])

# total word count
word_count = wordCount(data)
plotWordC(word_count, sys.argv[6])

# monthly top words
top_words = topWords(data, int(sys.argv[7]))
plotMonthlyTopWords(data, top_words, sys.argv[8])

# node word count
n_word_count = nodeWordCount(data)
plotNodeWordC(n_word_count, sys.argv[9])

# monthly top nodes
top_nodes = topNodes(data, int(sys.argv[10]))
plotMonthlyTopNodes(data, top_nodes, sys.argv[11])

# monthly average doc word count
d_word_count = docWordCount(data)
plotDocWordC(d_word_count, sys.argv[12])
