import MySQLdb


def initTwitterTables(host, user, passwd, db, tweet_tab, user_tab):
    """initalizes tweet and user tables in the specified db to fill with
    data"""

    rdb = MySQLdb.connect(host=host, user=user, passwd=passwd, db=db)
    cursor = rdb.cursor()

    tweet_str = """CREATE TABLE %s (
                   ID INT,
                   YEAR INT,
                   MONTH INT,
                   DAY INT,
                   HOUR INT,
                   MINUTE INT,
                   SECOND INT,
                   IN_REPLY_TO_SCREEN_NAME VARCHAR(15),
                   IN_REPLY_TO_STATUS_ID INT,
                   IN_REPLY_TO_USER_ID INT,
                   LANG VARCHAR(10),
                   POSSIBLY_SENSITVE INT,
                   RETWEET_COUNT INT,
                   RETWEETED INT,
                   SOURCE VARCHAR(100),
                   TEXT VARCHAR(140),
                   USER_ID INT )""" % tweet_tab

    user_str = """CREATE TABLE %s (
                  ID INT
                  YEAR INT,
                  MONTH INT,
                  DAY INT,
                  HOUR INT,
                  MINUTE INT,
                  SECOND INT,
                  DEFAULT_PROFILE INT,
                  DESCRIPTION VARCHAR(160),
                  DEFAULT_PROFIlE_IMAGE INT,
                  FAVOURITES_COUNT INT,
                  FOLLOWERS_COUNT INT,
                  FRIEND_COUNT INT,
                  GEO_ENABLED INT,
                  LANG VARCHAR(10),
                  LISTED_COUNT INT,
                  LOCATION VARCHAR(50),
                  NAME VARCHAR(20),
                  PROTECTED INT,
                  SCREEN_NAME VARCHAR(15),
                  STATUSES_COUNT INT,
                  URL VARCHAR(100),
                  UTC_OFFSET INT,
                  VERIFIED INT )""" % user_tab

    cursor.execute(tweet_str)
    cursor.execute(user_str)
    rdb.close()
