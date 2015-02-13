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
                   IN_REPLY_TO_SCREEN_NAME VARCHAR(15),
                   IN_REPLY_TO_STATUS_ID INT(25),
                   IN_REPLY_TO_USER_ID INT(25),
                   LANG VARCHAR(10),
                   POSSIBLY_SENSITVE INT(1),
                   RETWEET_COUNT INT(10),
                   RETWEETED INT(1),
                   SOURCE VARCHAR(100),
                   TEXT VARCHAR(140),
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
                  DESCRIPTION VARCHAR(160),
                  DEFAULT_PROFIlE_IMAGE INT(1),
                  FAVOURITES_COUNT INT(10),
                  FOLLOWERS_COUNT INT(10),
                  FRIEND_COUNT INT(10),
                  GEO_ENABLED INT(1),
                  LANG VARCHAR(10),
                  LISTED_COUNT INT(10),
                  LOCATION VARCHAR(50),
                  NAME VARCHAR(20),
                  PROTECTED INT(1),
                  SCREEN_NAME VARCHAR(15),
                  STATUSES_COUNT INT(10),
                  URL VARCHAR(100),
                  UTC_OFFSET INT(10),
                  VERIFIED INT(1) )""" % user_tab

    cursor.execute(tweet_str)
    cursor.execute(user_str)
    rdb.close()
