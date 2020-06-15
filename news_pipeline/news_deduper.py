import datetime
import os
import sys
import time

from dateutil import parser
from sklearn.feature_extraction.text import TfidfVectorizer

# import common package in parent directory
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))

import mongodb_client
import news_topic_modeling_service_client

from cloudAMQP_client import CloudAMQPClient

# TODO: use your own queue.
DEDUPE_NEWS_TASK_QUEUE_URL = "amqp://gxaifheg:ywBbygSd2rHW7KKT5m6Qaeq5tdAIu3Dm@gull.rmq.cloudamqp.com/gxaifheg"
DEDUPE_NEWS_TASK_QUEUE_NAME = "tap-news-dedupe-news-task-queue"

SLEEP_TIME_IN_SECONDS = 1

# change the table that store the news
NEWS_TABLE_NAME = "news"
SAME_NEWS_SIMILARITY_THRESHOLD = 0.9

cloudAMQP_client = CloudAMQPClient(DEDUPE_NEWS_TASK_QUEUE_URL, DEDUPE_NEWS_TASK_QUEUE_NAME)

def handle_message(msg):
    if msg is None or not isinstance(msg, dict) :
        return

    task = msg
    text = task['text']
    if text is None:
        return

    # Get all recent news based on publishedAt
    published_at = parser.parse(task['publishedAt'])
    published_at_day_begin = datetime.datetime(published_at.year, published_at.month, published_at.day, 0, 0, 0, 0)
    published_at_day_end = published_at_day_begin + datetime.timedelta(days=1)

    db = mongodb_client.get_db()
    # convert the cursor returned from mongodb to list
    same_day_news_list = list(db[NEWS_TABLE_NAME].find({'publishedAt': {'$gte': published_at_day_begin,'$lt': published_at_day_end}}))

    if same_day_news_list is not None and len(same_day_news_list) > 0:
        documents = [str(news['text']) for news in same_day_news_list]
        documents.insert(0, text)

        # calculate similarity matrix
        tfidf = TfidfVectorizer().fit_transform(documents)
        pairwise_sim = tfidf * tfidf.T
        print(pairwise_sim.A)

        rows, _ = pairwise_sim.shape

        for row in range(1, rows):
            # check each row for row in range(1, rows):
            if pairwise_sim[row, 0] > SAME_NEWS_SIMILARITY_THRESHOLD:
                print("Duplicated news. Ignore.")
                return

    # add news into mongodb
    # before store into mongodb,
    # we need to modify the published time to mongoDB datetime type
    # so that we can query the news by their publishAt
    task['publishedAt'] = parser.parse(task['publishedAt'])

    # Classify news
    title = task['title']
    if title is not None:
        topic = news_topic_modeling_service_client.classify(title)
        task['class'] = topic

    # upsert=True: if there is no news found, then insert; otherwise replace
    db[NEWS_TABLE_NAME].replace_one({'digest': task['digest']}, task, upsert=True)

def run():
    while True:
        if cloudAMQP_client is not None:
            msg = cloudAMQP_client.getMessage()
            if msg is not None:
                # Parse and process the task
                try:
                    handle_message(msg)
                except Exception as e:
                    print(e)
                    pass
            cloudAMQP_client.sleep(SLEEP_TIME_IN_SECONDS)
            #time.sleep(SLEEP_TIME_IN_SECONDS)

if __name__ == "__main__":
    run()
