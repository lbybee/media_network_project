from BeautifulSoup import BeautifulSoup
from datetime import datetime
import requests
import time
import cPickle
import sys


url = "http://usnpl.com"

source = requests.get(url)
soup = BeautifulSoup(source.text)
links = [a["href"] for a in soup.find("div", {"id": "data_box"}).find("table").findAll("a")]

twitter_links_dict = {}

t_1 = datetime.now()
ln = len(links)
for i, l in enumerate(links):
    pg = requests.get(l)
    pg_soup = BeautifulSoup(pg.text)
    pg_links = pg_soup.findAll("a")
    for j in range(2,len(pg_links)):
        a = pg_links[j]
        prev = pg_links[j - 3:j]
        if a.text == "T":
            for q, k in enumerate(prev):
                if k.text == "A":
                    name = pg_links[j - 4 + q].text
                    twitter_links_dict[name] = [a["href"], k["href"]]
                    break
    time.sleep(2)
    print datetime.now() - t_1, (i * 100.) / ln 

cPickle.dump(twitter_links_dict, open(sys.argv[1], "wb"))
