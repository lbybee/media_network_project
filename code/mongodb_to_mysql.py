from pymongo import MongoClient
from datetime import datetime
from mysql_load_fns import *
import MySQLdb
import sys
import os

client = MongoClient()
db = client["StreamingDb"]
collection = db["StreamingCollection"]

t_ln = collection.count()
t_1 = datetime.now()

i = 0

host = sys.argv[1]
user = sys.argv[2]
passwd = sys.argv[3]
db = sys.argv[4]
tweet_tab = sys.argv[5]
user_tab = sys.argv[6]

#initTwitterTables(host, user, passwd, db, tweet_tab, user_tab)

rdb = MySQLdb.connect(host=host, user=user, passwd=passwd, db=db)
#rdb.set_character_set('utf8')
cursor = rdb.cursor()
#cursor.execute('SET NAMES utf8;')
#cursor.execute('SET CHARACTER SET utf8;')
#cursor.execute('SET character_set_connection=utf8;')
cursor.execute('SET character_set_server=utf8mb4')

for obs in collection.find():
    insertTweet(cursor, obs, tweet_tab, rdb)
    insertUser(cursor, obs, user_tab, rdb)
    collection.remove({"_id": obs["_id"]})
    print (i * 100.) / t_ln, i, datetime.now() - t_1, obs["_id"]
    i += 1
    if i % 100000 == 0:
        rdb.commit()

rdb.close()   
