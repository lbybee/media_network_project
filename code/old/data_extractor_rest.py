from datetime import datetime
from pymongo import MongoClient
import cPickle
import sys
import csv
import os


client = MongoClient()
db = client["StreamingDb"]
collection = db["StreamingCollection"]

# prep for search
ln = collection.count()
t_1 = datetime.now()
i = 0

os.chdir(sys.argv[2])
for obs in collection.find():
    f_name = open(sys.argv[1], "ab")
    writer = csv.writer(f_name)
    text = obs["text"].encode("utf-8")
    agent = obs["user"]["screen_name"]
    date = obs["created_at"]
    writer.writerow([date, agent, text])
    f_name.close()
    print (i * 100.) / ln, datetime.now() - t_1, i, "db"
    i += 1

rest_timelines = cPickle.load(open(sys.argv[3], "rb"))
for link in rest_timelines:
    for tweet in rest_timelines[link]:
        f_name = open(sys.argv[1], "ab")
        writer = csv.writer(f_name)
        text = tweet.text.encode("utf-8")
        agent = tweet.user.screen_name
        date = tweet.created_at
        writer.writerow([date, agent, text])
        f_name.close()
