from datetime import datetime
import MySQLdb


def initTwitterTables(host, user, passwd, db, tweet_tab, user_tab):
    """initalizes tweet and user tables in the specified db to fill with
    data"""

    rdb = MySQLdb.connect(host=host, user=user, passwd=passwd, db=db)
    cursor = rdb.cursor()

    cursor.execute('SET NAMES utf8mb4')
    cursor.execute("SET CHARACTER SET utf8mb4")
    cursor.execute("SET character_set_connection=utf8mb4")

    tweet_str = """CREATE TABLE %s (
                   TID BIGINT(25),
                   YEAR INT(4),
                   MONTH INT(2),
                   DAY INT(2),
                   HOUR INT(2),
                   MINUTE INT(2),
                   SECOND INT(2),
                   IN_REPLY_TO_SCREEN_NAME VARCHAR(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
                   IN_REPLY_TO_STATUS_ID BIGINT(25),
                   IN_REPLY_TO_USER_ID BIGINT(25),
                   LANG VARCHAR(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
                   POSSIBLY_SENSITIVE INT(1),
                   RETWEET_COUNT INT(10),
                   RETWEETED INT(1),
                   TEXT VARCHAR(140) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
                   UID BIGINT(25) ) CHARACTER SET utf8mb4;""" % tweet_tab

    user_str = """CREATE TABLE %s (
                  UID BIGINT(25),
                  YEAR INT(4),
                  MONTH INT(2),
                  DAY INT(2),
                  HOUR INT(2),
                  MINUTE INT(2),
                  SECOND INT(2),
                  DEFAULT_PROFILE INT(1),
                  DESCRIPTION VARCHAR(160) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
                  DEFAULT_PROFIlE_IMAGE INT(1),
                  FAVOURITES_COUNT INT(10),
                  FOLLOWERS_COUNT INT(10),
                  FRIENDS_COUNT INT(10),
                  GEO_ENABLED INT(1),
                  LANG VARCHAR(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
                  LISTED_COUNT INT(10),
                  LOCATION VARCHAR(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
                  NAME VARCHAR(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
                  PROTECTED INT(1),
                  SCREEN_NAME VARCHAR(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
                  STATUSES_COUNT INT(10),
                  UTC_OFFSET INT(10),
                  VERIFIED INT(1) ) CHARACTER SET utf8mb4;""" % user_tab
    cursor.execute(tweet_str)
    cursor.execute(user_str)
    cursor.execute("ALTER TABLE %s ADD UNIQUE(TID)" % tweet_tab)
    cursor.execute("ALTER TABLE %s ADD UNIQUE(UID)" % user_tab)
    rdb.commit()
    rdb.close()


def insertTweet(cursor, tweet, tweet_tab, rdb):
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
    var_list.append(int(tweet["possibly_sensitive"]))
    
    var_list.append(tweet["retweet_count"])
    var_list.append(int(tweet["retweeted"]))
    
    var_list.append(tweet["text"])

    var_list.append(tweet["user"]["id"])

    sql = ("INSERT IGNORE INTO " + tweet_tab + " (TID, YEAR, MONTH, DAY, HOUR, MINUTE, SECOND, IN_REPLY_TO_SCREEN_NAME, IN_REPLY_TO_STATUS_ID, IN_REPLY_TO_USER_ID, LANG, POSSIBLY_SENSITIVE, RETWEET_COUNT, RETWEETED, TEXT, UID) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
    cursor.execute(sql, tuple(var_list))


def insertUser(cursor, tweet, user_tab, rdb):
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
        var_list.append(user["description"])
    else:
        var_list.append("''")
    var_list.append(int(user["default_profile_image"]))
    var_list.append(user["favourites_count"])
    var_list.append(user["followers_count"])
    var_list.append(user["friends_count"])
    var_list.append(int(user["geo_enabled"]))
    var_list.append(user["lang"])
    var_list.append(user["listed_count"])
    var_list.append(user["location"])
    var_list.append(user["name"])
    var_list.append(int(user["protected"]))
    var_list.append(user["screen_name"])
    var_list.append(user["statuses_count"])
    if user["utc_offset"] is not None:
        var_list.append(user["utc_offset"])
    else:
        var_list.append(0)
    var_list.append(int(user["verified"]))

    insert_str = "INSERT IGNORE INTO " + user_tab + " (UID, YEAR, MONTH, DAY, HOUR, MINUTE, SECOND, DEFAULT_PROFILE, DESCRIPTION, DEFAULT_PROFILE_IMAGE, FAVOURITES_COUNT, FOLLOWERS_COUNT, FRIENDS_COUNT, GEO_ENABLED, LANG, LISTED_COUNT, LOCATION, NAME, PROTECTED, SCREEN_NAME, STATUSES_COUNT, UTC_OFFSET, VERIFIED) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    cursor.execute(insert_str, tuple(var_list)) 


def insertTweetList(host, user, passwd, db, tweet_tab, user_tab, tweets):
    """inserts a list of tweets into the specified db"""

    t_1 = datetime.now()
    t_ln = len(tweets)
    rdb = MySQLdb.connect(host=host, user=user, passwd=passwd, db=db)
    rdb.set_character_set('utf8')
    cursor = rdb.cursor()
    cursor.execute('SET NAMES utf8;')
    cursor.execute('SET CHARACTER SET utf8;')
    cursor.execute('SET character_set_connection=utf8;')

    for i, t in enumerate(tweets):
        insertTweet(cursor, t, tweet_tab)
        insertUser(cursor, t, user_tab)
        print (i * 100.) / t_ln, i, t_1

    rdb.close()
