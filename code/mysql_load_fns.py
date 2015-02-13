from datetime import datetime
import MySQLdb


def initTwitterTables(host, user, passwd, db, tweet_tab, user_tab):
    """initalizes tweet and user tables in the specified db to fill with
    data"""

    rdb = MySQLdb.connect(host=host, user=user, passwd=passwd, db=db)
    cursor = rdb.cursor()

    tweet_str = """CREATE TABLE %s (
                   TID INT(25),
                   YEAR INT(4),
                   MONTH INT(2),
                   DAY INT(2),
                   HOUR INT(2),
                   MINUTE INT(2),
                   SECOND INT(2),
                   IN_REPLY_TO_SCREEN_NAME NVARCHAR(15),
                   IN_REPLY_TO_STATUS_ID INT(25),
                   IN_REPLY_TO_USER_ID INT(25),
                   LANG NVARCHAR(10),
                   POSSIBLY_SENSITVE INT(1),
                   RETWEET_COUNT INT(10),
                   RETWEETED INT(1),
                   TEXT NVARCHAR(140),
                   UID INT(25) )""" % tweet_tab

    user_str = """CREATE TABLE %s (
                  UID INT(25),
                  YEAR INT(4),
                  MONTH INT(2),
                  DAY INT(2),
                  HOUR INT(2),
                  MINUTE INT(2),
                  SECOND INT(2),
                  DEFAULT_PROFILE INT(1),
                  DESCRIPTION NVARCHAR(160),
                  DEFAULT_PROFIlE_IMAGE INT(1),
                  FAVOURITES_COUNT INT(10),
                  FOLLOWERS_COUNT INT(10),
                  FRIENDS_COUNT INT(10),
                  GEO_ENABLED INT(1),
                  LANG NVARCHAR(10),
                  LISTED_COUNT INT(10),
                  LOCATION NVARCHAR(50),
                  NAME NVARCHAR(20),
                  PROTECTED INT(1),
                  SCREEN_NAME NVARCHAR(15),
                  STATUSES_COUNT INT(10),
                  UTC_OFFSET INT(10),
                  VERIFIED INT(1) )""" % user_tab

    cursor.execute(tweet_str)
    cursor.execute(user_str)
    rdb.close()


def insertTweet(cursor, tweet, tweet_tab):
    """takes a tweet object and inserts the tweet element
    into the tweet table"""

    var_list = []
    
    # generate id
    var_list.append(tweet["id"])
    
    # now generate the data variable
    if type(tweet["created_at"]) != datetime:
        created_at =  datetime.strptime(tweet["created_at"], "%a %b %d %H:%M:%S +0000 %Y")
    else:
        created_at = tweet["created_at"]
    var_list.append(created_at.year)
    var_list.append(created_at.month)
    var_list.append(created_at.day)
    var_list.append(created_at.hour)
    var_list.append(created_at.minute)
    var_list.append(created_at.second)

    var_list.append(tweet["in_reply_to_screen_name"])
    var_list.append(tweet["in_reply_to_status_id"])
    var_list.append(tweet["in_reply_to_user_id"])
    
    var_list.append(tweet["lang"])
    
    var_list.append(tweet["retweet_count"])
    var_list.append(int(tweet["retweeted"]))
    
    var_list.append('%s' % tweet["text"])

    var_list.append(tweet["user"]["id"])

    insert_str = """INSERT INTO %s (TID, YEAR, MONTH, DAY, HOUR, MINUTE, SECOND, IN_REPLY_TO_SCREEN_NAME, IN_REPLY_TO_STATUS_ID, IN_REPLY_TO_USER_ID, LANG, POSSIBLY_SENSITIVE, RETWEET_COUNT, RETWEETED, TEXT, UID) VALUES(%d, %d, %d, %d, %d, %d, %d, %s, %d, %d, %s, %d, %d, %s, %d)""" % tuple([tweet_tab] + var_list)
    cursor.execute(insert_str)  


def insertUser(cursor, tweet, user_tab):
    """this function takes a tweet object, extracts the user and
    inserts the user into the user table specified"""

    var_list = []
    
    # gen user
    user = tweet["user"]

    var_list.append(user["id"])

    # now generate the date variable
    if type(user["created_at"]) != datetime:
        created_at =  datetime.strptime(user["created_at"], "%a %b %d %H:%M:%S +0000 %Y")
    else:
        created_at = user["created_at"]
    var_list.append(created_at.year)
    var_list.append(created_at.month)
    var_list.append(created_at.day)
    var_list.append(created_at.hour)
    var_list.append(created_at.minute)
    var_list.append(created_at.second) 

    var_list.append(int(user["default_profile"]))
    if user["description"] is not None:
        var_list.append('%s' % user["description"])
    else:
        var_list.append("''")
    var_list.append(int(user["default_profile_image"]))
    var_list.append(user["favourites_count"])
    var_list.append(user["followers_count"])
    var_list.append(user["friends_count"])
    var_list.append(int(user["geo_enabled"]))
    var_list.append(user["lang"])
    var_list.append(user["listed_count"])
    var_list.append('%s' % user["location"])
    var_list.append(user["name"])
    var_list.append(int(user["protected"]))
    var_list.append(user["screen_name"])
    var_list.append(user["statuses_count"])
    if user["utc_offset"] is not None:
        var_list.append(user["utc_offset"])
    else:
        var_list.append(0)
    var_list.append(int(user["verified"]))

    insert_str = "INSERT INTO %s (UID, YEAR, MONTH, DAY, HOUR, MINUTE, SECOND, DEFAULT_PROFILE, DEFAULT_PROFILE_IMAGE, FAVOURITES_COUNT, FOLLOWERS_COUNT, FRIENDS_COUNT, GEO_ENABLED, LANG, LISTED_COUNT, LOCATION, NAME, PROTECTED, SCREEN_NAME, STATUSES_COUNT, UTC_OFFSET, VERIFIED) VALUES(%d, %d, %d, %d, %d, %d, %d, %d, %s, %d, %d, %d, %d, %d, %s, %d, %s, %s, %d, %s, %d, %d, %d)" % tuple([user_tab] + var_list)
    cursor.execute(insert_str) 


def insertTweetList(host, user, passwd, db, tweet_tab, user_tab, tweets):
    """inserts a list of tweets into the specified db"""

    t_1 = datetime.now()
    t_ln = len(tweets)
    rdb = MySQLdb.connect(host=host, user=user, passwd=passwd, db=db)
    cursor = rdb.cursor()

    for i, t in enumerate(tweets):
        insertTweet(cursor, t, tweet_tab)
        insertUser(cursor, t, user_tab)
        print (i * 100.) / t_ln, i, t_1

    rdb.close()
