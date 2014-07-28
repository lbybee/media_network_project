from review_data import *
import sys
import cPickle


# data = buildSubsetData(sys.argv[1], ["word", "date", "count"], "date", 5000)
# print "got test data"

data = buildData(sys.argv[1], ["word", "date", "node", "count"], "date")
print "got real data"

# monthly word count
word_count = monthlyWordCount(data)
plotMonthlyWordC(sys.argv[2])
