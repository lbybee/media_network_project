from review_data import *
import sys
import cPickle
import os


os.chdir(sys.argv[1])

# data = buildSubsetData(sys.argv[1], ["word", "date", "count"], "date", 5000)
# print "got test data"

data = buildData(sys.argv[2], ["word", "date", "node", "count"], "date")
print "got real data"

# monthly word count
m_word_count = monthlyWordCount(data)
plotMonthlyWordC(m_word_count, sys.argv[3])

# unique monthly word count
um_word_count = monthlyUniqueWordC(data)
plotMonthlyUniqueWordC(um_word_count, sys.argv[4])

# total word count
word_count = wordCount(data)
plotWordC(word_count, sys.argv[5])

# monthly top words
top_words = topWords(data, int(sys.argv[6]))
plotMonthlyTopWords(data, top_words, sys.argv[7])

# node word count
n_word_count = nodeWordCount(data)
plotNodeWordC(n_word_count, sys.argv[8])

# monthly top nodes
top_nodes = topNodes(data, int(sys.argv[9]))
plotMonthlyTopNodes(data, top_nodes, sys.argv[10])
