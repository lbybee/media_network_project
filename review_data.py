from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
import csv
import pandas as pd
import random


def buildSubsetData(csv_f, var_names, date_var, rand_n):
    """takes a random subset of the data to test the code"""

    reader = csv.reader(open(csv_f, "rb"))
    data = [r for r in reader]
    random_mx = len(data)
    data = [data[random.randint(0, random_mx)] for i in range(rand_n)]
    data = pd.DataFrame(data, columns=var_names)
    data[date_var] = pd.to_datetime(data[date_var])
    # data["month"] = data[date_var].apply(lambda x: x.month)
    # data["day"] = data[date_var].apply(lambda x: x.day)
    # data["year"] = data[date_var].apply(lambda x: x.year)
    data["count"] = data["count"].astype(int)
    print "count"
    return data


def buildData(csv_f, var_names, date_var):
    """builds the dataset"""

    t_1 = datetime.now()
    reader = csv.reader(open(csv_f, "rb"))
    cols = [r for r in reader]
    ln_cols = len(cols)
    steps = ln_cols / 5000
    data = pd.DataFrame(columns=var_names)
    for i in range(steps):
        chk = cols[i * 5000: (i + 1) * 5000]
        chk = pd.DataFrame(chk, columns=var_names)
        chk[date_var] = pd.to_datetime(chk[date_var])
        chk["count"] = chk["count"].astype(int)
        data = data.append(chk)
        print (i * 100.) / steps, datetime.now() - t_1
    chk = cols[steps * 5000:]
    chk = pd.DataFrame(chk, columns=var_names)
    chk[date_var] = pd.to_datetime(chk[date_var])
    chk["count"] = chk["count"].astype(int)
    data = data.append(chk)
    return data


def monthlyWordCount(data):
    """generates the word count for each month"""

    return data.groupby("date")["count"].sum()


def monthlyUniqueWordC(data):
    """generates the unique word count monthly"""

    return data.groupby("date")["count"].size()


def wordCount(data):
    """generates the total count for each word"""

    return data.groupby("word")["count"].sum()


def topWords(data, t_limit):
    """gets the top words"""

    sort_data = data.groupby("word")["count"].sum()
    sort_data.sort()
    return sort_data[-t_limit:]


def plotMonthlyTopWords(data, t_words, fig_name):
    """plots the top words"""

    plt.figure()
    for w in t_words.index:
        data[data["word"] == w].groupby("date")["count"].sum().plot(label=w)
    plt.legend()
    plt.savefig(fig_name)
    plt.clf()


def plotMonthlyWordC(m_word_count, fig_name):
    """plots the monthly word count"""

    m_word_count.plot(title="Word Count")
    plt.savefig(fig_name)
    plt.clf()


def plotMonthlyUniqueWordC(um_word_count, fig_name):
    """plots the unique monthly word count"""

    um_word_count.plot(title="Unique Word Count")
    plt.savefig(fig_name)
    plt.clf()


def plotWordC(word_count, fig_name):
    """plots the total word count, density"""

    plt.hist(word_count, bins=100)
    plt.savefig(fig_name)
    plt.clf()


# The remainder of this code will only work with the network data

def nodeWordCount(data):
    """gets the word count for each node"""

    return data.groupby("node")["count"].sum()


def docWordCount(data):
    """gets the mean word count for each period"""

    g = data.groupby(["node", "date"]).sum()
    return g.mean(level="date")


def topNodes(data, n_limit):
    """get the top nodes"""

    sort_data = data.groupby("node")["count"].sum()
    sort_data.sort()
    return sort_data[-n_limit:]


def plotMonthlyTopNodes(data, t_nodes, fig_name):
    """plots the top nodes"""

    plt.figure()
    for n in t_nodes.index:
        data[data["node"] == n].groupby("date")["count"].sum().plot(label=n)
    plt.legend()
    plt.savefig(fig_name)
    plt.clf()


def plotDocWordC(d_word_count, fig_name):
    """plots the document word count"""

    d_word_count.plot(title="Node Month Average Word Count")
    plt.savefig(fig_name)
    plt.clf()


def plotNodeWordC(n_word_count, fig_name):
    """plots the word count for each node"""

    plt.hist(n_word_count, bins=100)
    plt.savefig(fig_name)
    plt.clf()
