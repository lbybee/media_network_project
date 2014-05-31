from BeautifulSoup import BeautifulSoup
from datetime import datetime
import requests


url = "http://usnpl.com"

source = requests.get(url)
soup = BeautifulSoup(source.text)
links = [a["href"] for a in soup.find("div", {"id": "data_box"}).find("table").findAll("a")]

twitter_links = []

t_1 = datetime.now()
ln = len(links)
for i, l in enumerate(links):
    pg = requests.get(l)
    pg_soup = BeautifulSoup(pg.text)
    pg_links = pg_soup.findAll("a")
    twitter_links.extend([a["href"] for a in pg_links if a.text == "T"])
    time.sleep(2)
    print datetime.now() - t_1, (i * 100.) / ln 


