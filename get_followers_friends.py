import tweepy


def authorize(consumer_key, consumer_secret,
              access_token, access_token_secret):
    """authorize the Twitter API"""

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    return api


def getFollowerIds(api, user):
    """gets the ids for all the followers for a given user"""

    follower_id_list = []
    for page in tweepy.Cursor(api.followers_ids, user).pages():
        time.sleep(60)
        follower_id_list.extend(page)
    return follower_id_list


def getFriendsIds(api, user):
    """gets the ids for all the friends for a given user"""

    friends_id_list = []
    for page in tweepy.Cursor(api.friends_ids, user).pages():
        time.sleep(60)
        friends_id_list.extend(page)
    return friends_id_list
