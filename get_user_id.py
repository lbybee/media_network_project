import tweepy
import cPickle
import sys
import os
import time
import ConfigParser
from datetime import datetime


def authorize(consumer_key, consumer_secret,
              access_token, access_token_secret):
    """authorize the Twitter API"""

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    return api


os.chdir(sys.argv[1])
Config = ConfigParser.ConfigParser()
Config.read("twitter.config")
consumer_key = Config.get("Twitter", "consumer_key")
consumer_secret = Config.get("Twitter", "consumer_secret")
access_token = Config.get("Twitter", "access_token")
access_token_secret = Config.get("Twitter", "access_token_secret")
api = authorize(consumer_key, consumer_secret,
                access_token, access_token_secret)

twitter_dict = cPickle.load(open("twitter_links.pkl"))
twitter_links = [twitter_dict[k][0].split("/")[-1] for k in twitter_dict.keys()]

timelines = {}
user_ids = []
t_1 = datetime.now()
for i, link in enumerate(twitter_links):
    try:
        timeline = api.user_timeline(link)
        timelines[link] = timeline
        print timeline[0].user.id, i, datetime.now() - t_1
        user_ids.append(timeline[0].user.id)
        time.sleep(5)
    except:
        try:
            time.sleep(30)
            timeline = api.user_timeline(link)
            timeline[link] = timeline
            print timeline[0].user.id, i, datetime.now() - t_1
            user_ids.append(timeline[0].user.id)
            time.sleep(5)
        except:
            print "Error", link, i

cPickle.dump(user_ids, open("user_ids.pkl", "wb"))
cPickle.dump(timelines, open("timelines.pkl", "wb"))
