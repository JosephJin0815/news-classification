import json
import os
import sys
import pickle
import redis
from bson.json_util import dumps
from datetime import datetime

REDIS_HOST = 'localhost'
REDIS_PORT = 6379

NEWS_LIST_BATCH_SIZE = 10
NEWS_LIMIT = 200 # max nums of news of one fetch
USER_NEWS_TIME_OUT_IN_SECONDS = 60 # timeout for user's pagination info in redis
NEWS_TABLE_NAME = "news"
# number of news in single page # maximum number of news of one fetch from
redis_client = redis.StrictRedis(REDIS_HOST, REDIS_PORT, db=0)

# do not install the 'bson' packge using pypi
from bson.json_util import dumps
# add the utils into the path where python will search the package from
# check https://api.mongodb.com/python/current/installation.html
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))

import mongodb_client
import news_recommendation_service_client

def getOneNews():
    """get one news"""
    print("getOneNews is called")
    res = mongodb_client.get_db()['news'].find_one()
    # dumps(res): convert bson to string
    # then convert string to json
    return json.loads(dumps(res))

def getNewsSummariesForUser(user_id, page_num):
    page_num = int(page_num)
    # news range to be fetched for the page number
    begin_index = (page_num - 1) * NEWS_LIST_BATCH_SIZE
    end_index = page_num * NEWS_LIST_BATCH_SIZE
    # the final list of news to be returned
    sliced_news = []
    db = mongodb_client.get_db()
    if redis_client.get(user_id) is not None:
        # user id already cached in redis, get next paginating data and fetch news
        news_digests = pickle.loads(redis_client.get(user_id))
        # both parameters are inclusive
        sliced_news_digest = news_digests[begin_index:end_index]
        sliced_news = list(db[NEWS_TABLE_NAME].find({'digest': {'$in': sliced_news_digest}}))
    else:
        # no cached data
        # retrieve news and store their digests list in redis with user id as key
        # retrieve news and sort by publish time in reverse order (latest first)
        total_news = list(db[NEWS_TABLE_NAME].find().sort([('publishedAt', -1)]).limit(NEWS_LIMIT))
        total_news_digest = [x['digest'] for x in total_news]
        # lambda function in python
        redis_client.set(user_id, pickle.dumps(total_news_digest))
        redis_client.expire(user_id, USER_NEWS_TIME_OUT_IN_SECONDS)
        sliced_news = total_news[begin_index:end_index]

    # TODO: user preference to customizer return new lists
    preference = news_recommendation_service_client.getPreferenceForUser(user_id)
    topPreference = None

    if preference is not None and len(preference) > 0:
        topPreference = preference[0]

    for news in sliced_news:
        # Remove text field to save bandwidth
        del news['text']
        if news['class'] == topPreference:
            news['reason'] = "Recommend"
        if news['publishedAt'].date() == datetime.today().date():
            # Add time tag to be displayed on page
            news['time'] = 'today'
    return json.loads(dumps(sliced_news))

# import common package in parent directory
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))
from cloudAMQP_client import CloudAMQPClient

# use your own config.
LOG_CLICKS_TASK_QUEUE_URL = "amqp://bubrmmet:usDFsc4gNt1b3k3E4JAxjlmv30JrpWiV@gull.rmq.cloudamqp.com/bubrmmet"
LOG_CLICKS_TASK_QUEUE_NAME = "tap-news-clicks-news-task-queue"
cloudAMQP_client = CloudAMQPClient(LOG_CLICKS_TASK_QUEUE_URL, LOG_CLICKS_TASK_QUEUE_NAME)

def logNewsClickForUser(user_id, news_id):
    message = {'userId': user_id, 'newsId': news_id, 'timestamp': str(datetime.utcnow())}
    # Send log task to click log processor
    cloudAMQP_client.sendMessage(message)
