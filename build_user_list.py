import ConfigParser
from datetime import datetime
import os
import cPickle
import tweepy
import time
import sys



def authorize(consumer_key, consumer_secret,
              access_token, access_token_secret,
              timeout=60):
    """authorizes the Twitter API"""

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
user_dict = {}
missing = []
t_1 = datetime.now()

for i, k in enumerate(twitter_dict.keys()):
    screen_name = twitter_dict[k][0].split("/")[-1]
    try:
        user_object = api.get_user(screen_name)
        twitter_dict[k].append(user_object.id)
        user_dict[k] = user_object
    except Exception as e:
        print e
        time.sleep(60)
        try:
            user_object = api.get_user(screen_name)
            twitter_dict[k].append(user_object.id)
            user_dict[k] = user_object
        except Exception as e:
            print e
            missing_append(screen_name)
    time.sleep(5)
    print i, datetime.now() - t_1


cPickle.dump(user_dict, open("user_dict.pkl", "wb"))
cPickle.dump(twitter_dict, open("twitter_links.pkl", "wb"))
cPickle.dump(missing, open("missing.pkl", "wb"))
