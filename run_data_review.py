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

# total word count
word_count = wordCount(data)
plotWordC(word_count, sys.argv[4])
