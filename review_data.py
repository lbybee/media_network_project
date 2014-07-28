from datetime import datetime
import matplotlib.pyplot as plt
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
    data[date_var] = data[date_var].apply(pd.to_datetime)
    data["month"] = data[date_var].apply(lambda x: x.month)
    data["day"] = data[date_var].apply(lambda x: x.day)
    data["year"] = data[date_var].apply(lambda x: x.year)
    data["monthyear"] = data[date_var].apply(lambda x: datetime(x.year, x.month, 1))
    data["count"] = data["count"].astype(int)
    return data


def buildData(csv_f, var_names, date_var):
    """builds the dataset"""

    reader = csv.reader(open(csv_f, "rb"))
    data = [r for r in reader]
    data = pd.DataFrame(data, columns=var_names)
    data[date_var] = data[date_var].apply(pd.to_datetime)
    data["month"] = data[date_var].apply(lambda x: x.month)
    data["day"] = data[date_var].apply(lambda x: x.day)
    data["year"] = data[date_var].apply(lambda x: x.year)
    data["monthyear"] = data[date_var].apply(lambda x: datetime(x.year, x.month, 1))
    data["count"] = data["count"].astype(int)
    return data


def monthlyWordCount(data):
    """generates the word count for each month"""

    return data.groupby("monthyear")["count"].sum()


def monthlyUniqueWordC(data):
    """generates the unique word count monthly"""

    return data.groupby("monthyear")["count"].size()


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
        data[data["word"] == w].groupby("monthyear")["count"].sum().plot(label=w)
    plt.legend()
    plt.savefig(fig_name)


def plotMonthlyWordC(m_word_count, fig_name):
    """plots the monthly word count"""

    m_word_count.plot(title="Word Count")
    plt.savefig(fig_name)


def plotMonthlyUniqueWordC(um_word_count, fig_name):
    """plots the unique monthly word count"""

    um_word_count.plot(title="Unique Word Count")
    plt.savefig(fig_name)


def plotWordC(word_count, fig_name):
    """plots the total word count, density"""

    plt.hist(word_count, bins=100, title="Word Count Density")


# The remainder of this code will only work with the network data

def nodeWordCount(data):
    """gets the word count for each node"""

    return data.groupby("node")["count"].sum()


def docWordCount(data):
    """gets the mean word count for each period"""

    subset = data
    subset["sum"] = subset.groupby(["node", "monthyear"])["count"].transform(sum)
    return subset.groupby("monthyear").mean()


def topNodes(data, n_limit):
    """get the top nodes"""

    sort_data = data.groupby("node")["count"].sum()
    sort_data.sort()
    return sort_data[-n_limit:]


def plotMonthlyTopNodes(data, t_nodes, fig_name):
    """plots the top nodes"""

    plt.figure()
    for n in t_nodes.index:
        data[data["node"] == n].groupby("monthyear")["count"].sum().plot(label=n)
    plt.legend()
    plt.savefig(fig_name)


def plotDocWordC(d_word_count, fig_name):
    """plots the document word count"""

    d_word_count.plot(title="Node Month Average Word Count")
    plt.savefig(fig_name)


def plotNodeWordC(n_word_count, fig_name):
    """plots the word count for each node"""

    plt.hist(n_word_count, bins=100, title="Node Word Count Density")
    plt.savefig(fig_name)
