from nltk.tokenize import word_tokenize


def cleanData(csv_f, output_f):
    """cleans the csv file"""

    t_1 = datetime.now()

    node_dict = {}

    reader = csv.reader(open(csv_f, "rb"))
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
            node_dict[node][date] = []
        text = text.lower()
        text = re.sub("[^a-z ]", "", text)
        for w in word_tokenize(text):
            if w not in stopwords.words("english") and "http" not in w:
                node_dict[node][date].append(w)
        print (i * 100.) / reader_ln, datetime.now() - t_1
    cPickle.dump(node_dict, open(output_f, "wb"))


def sortByDate(data):
    """returns the dates and values sorted by date"""

    dt_dates = []
    for d in data.keys():
        dt = datetime.strptime(d, "%Y-%m-%d %H")
        dt_dates.append(dt)
    dt_dates.sort()
    dates = [dt.strftime("%Y-%m-%d %H") for dt in dt_dates]
    values = [data[d] for d in dates]
    return dates, values


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


