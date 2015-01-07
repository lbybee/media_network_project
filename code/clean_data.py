from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import re
from nltk import PorterStemmer
from datetime import datetime, timedelta
import csv
import cPickle


def cleanRData(i_csv_f, o_csv_f, hr):
    """writes the data to something better for R"""

    t_1 = datetime.now()

    node_dict = {}

    reader = csv.reader(open(i_csv_f, "rb"))
    reader_l = list(reader)
    reader_ln = len(reader_l)
    for i, r in enumerate(reader_l):
        text = r[2]
        node = r[1]
        date = datetime.strptime(r[0], "%a %b %d %H:%M:%S +0000 %Y")
        if date.hour >= hr:
            date = date.replace(hour = (date.hour - date.hour % hr))
        else:
            date = date.replace(hour = 0)
        date = date.strftime("%Y-%m-%d %H:00:00")
        if node not in node_dict:
            node_dict[node] = {}
        if date not in node_dict[node]:
            node_dict[node][date] = ""
        text = text.replace("@", "").replace("#", "").replace("'", "")
        text_l = text.split(" ")
        if "RT" in text_l:
            text_l.remove("RT")
        text_l = [w for w in text_l if "http" not in w]
        text = " ".join(text_l)
        node_dict[node][date] += " %s" % text
        print (i * 100.) / reader_ln, datetime.now() - t_1, "dict"
    writer = csv.writer(open(o_csv_f, "wb"))
    mx_date = 0
    for n in node_dict:
        for d in node_dict[n].keys():
            if len(node_dict[n][d]) < 10:
                del node_dict[n][d]
    for n in node_dict:
        t_date = len(node_dict[n])
        if t_date > mx_date:
            mx_date = t_date
    for n in node_dict.keys():
        if len(node_dict[n]) != mx_date:
            del node_dict[n]
    print len(node_dict)
    for n in node_dict:
        for d in node_dict[n]:
            writer.writerow([n, d, node_dict[n][d]])


