import ConfigParser
import cPickle
import os
from datetime import datetime
import json
import tweepy
import sys

@classmethod
def parse(cls, api, raw):
	status = cls.first_parse(api, raw)
	setattr(status, 'json', json.dumps(raw))
	return status

tweepy.models.Status.first_parse = tweepy.models.Status.parse
tweepy.models.Status.parse = parse

class StreamWatcherListener(tweepy.StreamListener):

    def on_status(self, status):
        json_status = status.json
        output = open("statuses.txt", "ab")
        output.write(json.dumps(json_status, output))
        output.write("\n")
        return True

    def on_error(self, status_code):
        print 'An error has occured! Status code = %s' % status_code
        error = open("errors.txt", "ab")
        error.write(str(status_code))
        error.write("\n")
        return True  # keep stream alive

    def on_timeout(self):
        print 'Snoozing Zzzzzz'


def authorize(consumer_key, consumer_secret,
              access_token, access_token_secret,
              timeout=60):
    """authorizes the Twitter API"""

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.streaming.Stream(auth, StreamWatcherListener(), timeout=timeout)
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

#load user list

twitter_dict = cPickle.load(open("twitter_links.pkl"))
twitter_links = [twitter_dict[k][0].split("/")[-1] for k in twitter_dict]
# This is a very hacky solution to a problem that I keep running into, the streaming scraper keeps crashing with an IncompleteRead error, I am going to have to rewrite a lot of this at a lower level at somepoint but this makes the scraper work for now.
t_1 = datetime.now()
while True:
    try:
        api.filter(follow=twitter_links)
    except Exception as e:
        print e, datetime.now() - t_1
