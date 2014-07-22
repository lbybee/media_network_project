from datetime import datetime
import cPickle
import csv
import sys
import os


def buildVocab(csv_f):
    """builds the vocab for the data"""
    
    t_1 = datetime.now()

    vocab = []
    reader = csv.reader(open(csv_f), "rb"))
    reader_l = list(reader)
    ln = len(reader_l)
    for i, row in enumerate(reader_l):
        text = row[2]
        text_l = text.split(" ")
        for word in text_l:
            if word not in vocab:
                vocab.append(word)
        print (i * 100.) / ln, datetime.now() - t_1, i
    return vocab


def buildData(csv_f, vocab):
    """builds the dataset"""

    t_1 = datetime.now()

    data = {}
    reader = csv.reader(open(csv_f), "rb"))
    reader_l = list(reader)
    ln = len(reader_l)
    for i, row in enumerate(reader_l):
        text = row[2].split(" ")
        node = row[1]
        dateb = row[0].split(" ")
        period = dateb[1] + " " + dateb[2] + " " + dateb[5]
        if node in data:
            if period in data[node]:
                doc = []
                for w in text:
                    doc.append(vocab.index(w))
                data[node][period].append(doc)
            else:
                data[node][period] = []
                doc = []
                for w in text:
                    doc.append(vocab.index(w))
                data[node][period].append(doc)
        else:
            data[node] = {}
            data[node][period] = []
            doc = []
            for w in text:
                doc.append(vocab.index(w))
            data[node][period].append(doc)
        print (i * 100.) / ln, datetime.now() - t_1, i
    return data


os.chdir(sys.argv[3])
csv_f = sys.argv[1]

vocab = buildVocab(csv_f)
data = buildData(csv_f, vocab)
cPickle.dump(data, open(sys.argv[2], "wb"))
