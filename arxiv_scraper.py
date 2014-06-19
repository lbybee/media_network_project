from BeautifulSoup import BeautifulSoup
import cPickle
import requests
import slat


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
    num_1 = [a.find("b") for a in soup.find("ul").findAll("li")]
    num_2 = [a.find("i") for a in soup.find("ul").findAll("li")]
    num = [x + y for x, y in zip(num_1, num_2)]
    return months, num


def getArticleUrls(url, month, max_ind, t_sleep):
    """gets all the articles for a month"""

    articles = []
    for i in range(max_ind / 2000 + 1):
        if i > 0:
            # only sleep if there is more than one page, otherwise the sleep
            # is external
            time.sleep(t_sleep)
        base_pg = requests.get(url + year, data={"show": (i + 1) * 2000,
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


def fullRun(url, t_sleep, url_f, output_f):
    """gets all the articles"""

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
                print c, y, m, datetime.now() - t_1
    cPickle.dump(article_urls, open(url_f, "wb"))

    # now get articles
    for a in article_urls:
        articles.append(getArticle(url, a))
        time.sleep(t_sleep)
    cPickle.dump(articles, open(output_f, "wb"))
