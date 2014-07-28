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
        # t = data[data["word"] == w].groupby("monthyear")["count"].sum().plot()
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
