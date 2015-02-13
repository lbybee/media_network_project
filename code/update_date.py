from pymongo import MongoClient
from datetime import datetime
import sys


client = MongoClient()
db = client["StreamingDb"]
collection = db["StreamingCollection"]

ln = collection.count()
t_1 = datetime.now()

i = int(sys.argv[1])

while True:
    try:
        for obs in collection.find({"created_at": {"$type": 2}}):
            time = datetime.strptime(obs["created_at"], "%a %b %d %H:%M:%S +0000 %Y")
            collection.update({"_id": obs["_id"]}, {"$set":{"created_at": time}})
            print i * 100. / ln, datetime.now() - t_1, ln, i, obs["_id"]
            i += 1
    except Exception as e:
        print e
        input("It broke...")
