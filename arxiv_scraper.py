from BeautifulSoup import BeautifulSoup
import cPickle
from datetime import datetime
import requests
import time


def getCategories(url):
    """gets all the categories for arxiv"""

    base_pg = requests.get(url)
    soup = BeautifulSoup(base_pg.text)
    categories = soup.findAll("ul")[:-1]
    sub_cat = []
    for c in categories:
        sub_c = [a.find("a")["href"] for a in c.findAll("li")]
        sub_cat.extend(sub_c)
    return sub_cat


def getYears(url, cat):
    """gets the years for a given category"""

    base_pg = requests.get(url + cat)
    soup = BeautifulSoup(base_pg.text)
    years = [a["href"] for a in soup.find("ul").findAll("li")[7].findAll("a")]
    return years


def getMonths(url, year):
    """gets all the months for a given year and returns the month along with
    the maximum number of articles"""

    base_pg = requests.get(url + year)
    soup = BeautifulSoup(base_pg.text)
    months = [a.find("a")["href"] for a in soup.find("ul").findAll("li")]
    num_1 = [a.find("b").text for a in soup.find("ul").findAll("li")]
    num_2 = [a.find("i").text for a in soup.find("ul").findAll("li")]
    num = [x + y for x, y in zip(num_1, num_2)]
    return months, num


def getArticleUrls(url, month, max_ind, t_sleep):
    """gets all the articles for a month"""

    articles = []
    for i in range(0, int(max_ind) / 2000 + 1, 2000):
        if i > 0:
            # only sleep if there is more than one page, otherwise the sleep
            # is external
            time.sleep(t_sleep)
        base_pg = requests.get(url + month, data={"show": (i + 1) * 2000,
                                                  "skip": i * 2000})
        soup = BeautifulSoup(base_pg.text)
        articles.extend([a["href"] for a in
                         soup.findAll("a", {"title": "Abstract"})])
    return articles


def getArticle(url, a_url):
    """gets the article info and downloads the paper"""

    article_dict = {}
    base_pg = requests.get(url + a_url)
    soup = BeautifulSoup(base_pg.text)
    article_dict["title"] = soup.find("h1", {"class": "title mathjax"}).text
    article_dict["authors"] = [a.text for a in
                               soup.find("div", {"class": "authors"}).findAll("a")]
    article_dict["date"] = soup.find("div", {"class": "dateline"}).text
    article_dict["sub_hist"] = [a.text for a in
                                soup.find("div", {"class": "submission-history"}).findAll("br")]
    # write the pdf to the correct file
    l_name = a_url.split("/")[-1]
    article_dict["link"] = l_name
    f_name = l_name + ".pdf"
    pdf = open(f_name, "wb")
    pdf_url = soup.find("div", {"class": "full-text"}).find("ul").find("li").find("a")["href"] 
    pdf.write(requests.get(url + pdf_url).content)
    pdf.close()
    # extract the text from the pdf
    input_ = open(f_name, "rb")
    doc = slate.PDF(input_)
    article_dict["text"] = doc
    return article_dict


def fullRun(url, t_sleep, url_f, output_f, start_ind, urls=True):
    """gets all the articles"""

    if urls:
        t_1 = datetime.now()
        article_urls = []
        articles = []
        categories = getCategories(url)
        time.sleep(t_sleep)
        for c in categories:
            years = getYears(url, c)
            time.sleep(t_sleep)
            for y in years:
                months, max_ind = getMonths(url, y)
                time.sleep(t_sleep)
                for m, m_i in zip(months, max_ind):
                    articles.extend(getArticleUrls(url, m, m_i, t_sleep))
                    time.sleep(t_sleep)
                    print c.split("/")[-1], y.split("/")[-1], m.split("/")[-1], datetime.now() - t_1
        cPickle.dump(article_urls, open(url_f, "wb"))
        print "got urls"
    else:
        article_urls = cPickle.load(open(url_f, "rb"))

    # now get articles
    t_1 = datetime.now()
    ln = len(article_urls)
    for i, a in enumerate(article_urls[start_ind:]):
        articles.append(getArticle(url, a))
        print start_ind + i, (start_ind + i) * 100. / ln, datetime.now() - t_1
        time.sleep(t_sleep)
    cPickle.dump(articles, open(output_f, "wb"))
