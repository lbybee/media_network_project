from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import re
from nltk import PorterStemmer
from datetime import datetime
import csv
import cPickle


def cleanData(csv_f, output_f):
    """cleans the csv file"""

    t_1 = datetime.now()

    node_dict = {}

    reader = csv.reader(open(csv_f, "rb"))
    reader_l = list(reader)
    reader_ln = len(reader_l)
    for i, r in enumerate(reader_l):
        text = r[2]
        node = r[1]
        date = datetime.strptime(r[0], "%a %b %d %H:%M:%S +0000 %Y")
        date = date.strftime("%Y-%m-%d %H")
        if node not in node_dict:
            node_dict[node] = {}
        if date not in node_dict[node]:
            node_dict[node][date] = []
        text = text.lower()
        text = re.sub("[^a-z ]", "", text)
        for w in word_tokenize(text):
            if w not in stopwords.words("english") and "http" not in w:
                node_dict[node][date].append(w)
        print (i * 100.) / reader_ln, datetime.now() - t_1
    cPickle.dump(node_dict, open(output_f, "wb"))
    return node_dict


def cleanDateData(csv_f, output_f):
    """cleans the csv file"""

    t_1 = datetime.now()

    date_dict = {}

    reader = csv.reader(open(csv_f, "rb"))
    reader_l = list(reader)
    reader_ln = len(reader_l)
    for i, r in enumerate(reader_l):
        text = r[2]
        date = datetime.strptime(r[0], "%a %b %d %H:%M:%S +0000 %Y")
        date = date.strftime("%Y-%m-%d %H")
        if date not in date_dict:
            date_dict[date] = ""
        date_dict[date] += " %s" % text
        print (i * 100.) / reader_ln, datetime.now() - t_1
    writer = csv.writer(open(output_f, "wb"))
    for date in date_dict:
        writer.writerow([date, date_dict[date]])


def sortByDate(data):
    """returns the dates and values sorted by date, this drops
    the dictionary structure"""

    t_1 = datetime.now()

    sorted_values = []
    node_dates = []
    nodes = data.keys()
    ln_nodes = len(nodes)
    for i, n in enumerate(nodes):
        dt_dates = [datetime.strptime(d, "%Y-%m-%d %H") for d in data[n]]
        dt_dates.sort()
        dates = [dt.strftime("%Y-%m-%d %H") for dt in dt_dates]
        values = [data[n][d] for d in dates]
        sorted_values.append(values)
        node_dates.append(dates)
        print (i * 100.) / ln_nodes, datetime.now() - t_1
    return nodes, node_dates, sorted_values


def buildVocab(text):
    """builds the vocab from text"""
    
    vocab = []
    t_1 = datetime.now()
    ln_text = len(text)
    for i, n in enumerate(text):
        for d in n:
            for w in d:
                if w not in vocab:
                    vocab.append(w)
        print (i * 100.) / ln_text, datetime.now() - t_1
    return vocab


def convertToVector(text, vocab):
    """converts text to vectors"""
    
    n_text = []
    t_1 = datetime.now()
    ln_text = len(text)
    for j, n in enumerate(text):
        n_node = []
        for d in n:
            n_date = []
            for w in d:
                n_date.append(vocab.index(w))
            n_node.append(n_date)
        n_text.append(n_node)
        print (j * 100.) / ln_text, datetime.now() - t_1
    return n_text


def cleanRData(i_csv_f, o_csv_f):
    """writes the data to something better for R"""

    t_1 = datetime.now()

    node_dict = {}

    reader = csv.reader(open(o_csv_f, "rb"))
    reader_l = list(reader)
    reader_ln = len(reader_l)
    for i, r in enumerate(reader_l):
        text = row[2]
        node = row[1]
        date = datetime.strptime(row[0], "%a %b %d %H:%M:%S +0000 %Y")
        date = date.strftime("%Y-%m-%d %H")
        if node not in node_dict:
            node_dict[node] = {}
        if date not in node_dict[node]:
            node_dict[node][date] = ""
        node_dict[node][date] += " %s" % text
        print (i * 100.) / reader_ln, datetime.now() - t_1, "dict"
    writer = csv.writer(open(o_csv_f, "wb"))
    for n in node_dict:
        for d in node_dict[n]:
            writer.writerow([n, d, node_dict[n][d]])


