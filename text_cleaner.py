from datetime import datetime
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk import PorterStemmer
import re
import csv


def addWordTDict(w, date, node, data_dict):
    """"""

    if date in data_dict:
        if node in data_dict[date]:
            if w in data_dict[date][node]:
                data_dict[date][node][w] += 1
            else:
                data_dict[date][node][w] = 1
        else:
            data_dict[date][node] = {}
            data_dict[date][node][w] = 1
    else:
        data_dict[date] = {}
        data_dict[date][node] = {}
        data_dict[date][node][w] = 1
    return data_dict


def extractData(csv_f, stemming, month_date):
    """extracts the data from the csv"""

    rx = re.compile("\W+")

    t_1 = datetime.now()
    data_dict = {}

    reader = csv.reader(open(csv_f, "rb"))
    reader_l = list(reader)
    reader_ln = len(reader_l)
    for i, row in enumerate(reader_l):
        text = row[2]
        node = row[1]
        if "-" not in row[0]:
            dateb = row[0].split(" ")
            if month_date:
                period = dateb[2] + " " + dateb[5]
                period = str(datetime.strptime(period, "%b %Y"))
            else:
                period = dateb[1] + " " + dateb[2] + " " + dateb[5]
                period = str(datetime.strptime(period, "%b %d %Y"))
        else:
            dateb = row[0].split(" ")[0].split("-")
            if month_date:
                period = dateb[1] + " " + dateb[0]
                period = str(datetime.strptime(period, "%m %Y"))
            else:
                period = dateb[1] + " " + dateb[2] + " " + dateb[0]
                period = str(datetime.strptime(period, "%m %d %Y"))
        text = text.lower()
        text = rx.sub(" ", text).strip()
        for w in word_tokenize(text):
            # remove urls
            if "http" not in w:
                # do any stemming
                if stemming == 1:
                    w = PorterStemmer().stem_word(w)
                if w not in stopwords.words("english"):
                    data_dict = addWordTDict(w, period, node, data_dict)
        print (i * 100.) / reader_ln, datetime.now() - t_1
    return data_dict


def getVocab(data_dict):
    """gets the vocab from a data_dict"""

    t_1 = datetime.now()
    vocab = []
    data_ln = len(data_dict)
    for i, d in enumerate(data_dict):
        for n in data_dict[d]:
            wrds = data_dict[d][n].keys()
            for w in wrds:
                if w not in vocab:
                    vocab.append(w)
        print (i * 100.) / data_ln, datetime.now() - t_1, "vocab"
    return vocab


def writeDictionary(data_dict, csv_f):
    """writes the dictionary to a csv file"""

    t_1 = datetime.now()
    data_ln = len(data_dict)
    writer = csv.writer(open(csv_f, "wb"))
    for i, d in enumerate(data_dict):
        for n in data_dict[d]:
            for w in data_dict[d][n]:
                writer.writerow([w, d, n, data_dict[d][n][w]])
        print (i * 100.) / data_ln, datetime.now() - t_1, "csv"


def fullRun(i_csv_f, o_csv_f, stemming=0, month_date=False):
    """does a full run"""

    data_dict = extractData(i_csv_f, stemming, month_date)
    writeDictionary(data_dict, o_csv_f)
