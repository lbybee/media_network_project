import MySQLdb
import ConfigParser
import mysql_load_fns as myfns
import os
from datetime import datetime
import json
import tweepy
import cPickle
import sys
from tweepy.utils import import_simplejson


@classmethod
def parse(cls, api, raw):
	status = cls.first_parse(api, raw)
	setattr(status, 'json', json.dumps(raw))
	return status

tweepy.models.Status.first_parse = tweepy.models.Status.parse
tweepy.models.Status.parse = parse

json = import_simplejson()

class StreamWatcherListener(tweepy.StreamListener, host, user, passwd, db, twitter_tab, user_tab):

    def __init__(self):
        self.localhost = host
        self.user = user
        self.passwd = passwd
        self.db = db
        self.twitter_tab = twitter_tab
        self.user_tab = user_tab
        self.rdb = MySQLdb.connect(host=host, user=user, passwd=passwd, db=db, use_unicode=True, charset="utf8")
        self.cursor = self.rdb.cursor()
        self.cursor.execute('SET NAMES utf8mb4')
        self.cursor.execute("SET CHARACTER SET utf8mb4")
        self.cursor.execute("SET character_set_connection=utf8mb4")
        self.cursor.execute("SET character_set_server=utf8mb4")

    def on_status(self, status):
        json_status = status.json
        print json_status
        json_data = json.loads(json_status)
        myfns.insertTweet(self.cursor, json_data, self.tweet_tab)
        myfns.insertUser(self.cursor, json_data, self.user_tab)
        if random.randint(1, 1000) == 500:
            self.rdb.commit()
        return True

    def on_error(self, status_code):
        print 'An error has occured! Status code = %s' % status_code
        error = open("errors.txt", "ab")
        error.write(str(status_code))
        error.write("\n")
        self.rdb.commit()
        return True  # keep stream alive

    def on_timeout(self):
        print 'Snoozing Zzzzzz'
        self.rdb.commit()


def authorize(consumer_key, consumer_secret, access_token, access_token_secret,
              host, user, passwd, db, tweetable, usertable,
              timeout=60):
    """authorizes the Twitter API"""

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.streaming.Stream(auth, StreamWatcherListener(host, user, passwd,
                                                              db, tweettable, usertable),
                                  timeout=timeout)
    return api


os.chdir(sys.argv[1])
Config = ConfigParser.ConfigParser()
Config.read(sys.argv[2])
consumer_key = Config.get("Twitter", "consumer_key")
consumer_secret = Config.get("Twitter", "consumer_secret")
access_token = Config.get("Twitter", "access_token")
access_token_secret = Config.get("Twitter", "access_token_secret")
host = Config.get("Twitter", "host")
user = Config.get("Twitter", "user")
passwd = Config.get("Twitter", "passwd")
db = Config.get("Twitter", "db")
tweettable = Config.get("Twitter", "tweettable")
usertable = Config.get("Twitter", "usertable")
api = authorize(consumer_key, consumer_secret, access_token, access_token_secret,
                host, user, passwd, db, tweettable, usertable)

#load user list

twitter_links = cPickle.load(open("user_ids.pkl"))
twitter_links = [str(i) for i in twitter_links]
# This is a very hacky solution to a problem that I keep running into, the streaming scraper keeps crashing with an IncompleteRead error, I am going to have to rewrite a lot of this at a lower level at somepoint but this makes the scraper work for now.
t_1 = datetime.now()
while True:
    try:
        api.filter(follow=twitter_links)
    except Exception as e:
        print e, datetime.now() - t_1

