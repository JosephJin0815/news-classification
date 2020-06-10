import os
import sys
import time

from newspaper import Article

# import common package in parent directory
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'scraper'))

import cnn_news_scraper
from cloudAMQP_client import CloudAMQPClient

# TODO: use your own queue.
SCRAPE_NEWS_TASK_QUEUE_URL = "amqp://jamkyqms:HFH8eLsHiLjAWiiJKw2FTsJWmCoyK15J@gull.rmq.cloudamqp.com/jamkyqms"
SCRAPE_NEWS_TASK_QUEUE_NAME = "tap-news-scraper-news-task-queue"
DEDUPE_NEWS_TASK_QUEUE_URL = "amqp://gxaifheg:ywBbygSd2rHW7KKT5m6Qaeq5tdAIu3Dm@gull.rmq.cloudamqp.com/gxaifheg"
DEDUPE_NEWS_TASK_QUEUE_NAME = "tap-news-dedupe-news-task-queue"

SLEEP_TIME_IN_SECONDS = 5

dedupe_news_queue_client = CloudAMQPClient(DEDUPE_NEWS_TASK_QUEUE_URL, DEDUPE_NEWS_TASK_QUEUE_NAME)
scrape_news_queue_client = CloudAMQPClient(SCRAPE_NEWS_TASK_QUEUE_URL, SCRAPE_NEWS_TASK_QUEUE_NAME)

def handle_message(msg):
    if msg is None or not isinstance(msg, dict):
        print('message is broken')
        return
    task = msg
    text = None

    # we only support CNN now
    # if task['source'] == 'cnn':
    #    print('scraping CNN news')
    #    text = cnn_news_scraper.extract_news(task['url'])
    #else:
    #    print('News source [%s] is not supported.' % task['source'])
    #    #return
    ##task['text'] = article.text.encode('utf-8')
    #task['text'] = text
    # use newspaper3k instead
    article = Article(task['url'])
    article.download()
    article.parse()
    # task['text'] = article.text.encode('utf-8')
    task['text'] = article.text
    dedupe_news_queue_client.sendMessage(task)

def run():
    while True:
        if scrape_news_queue_client is not None:
            msg = scrape_news_queue_client.getMessage()
            if msg is not None:
                # parse and process the task
                try:
                    handle_message(msg)
                except Exception as e:
                    print(e) # coding=utf-8
                    pass
            scrape_news_queue_client.sleep(SLEEP_TIME_IN_SECONDS)
            #time.sleep(SLEEP_TIME_IN_SECONDS)

if __name__ == '__main__':
    run()
