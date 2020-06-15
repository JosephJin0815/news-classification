# -*- coding: utf-8 -*# since we have alpha, we need utf-8
""" Time decay model
If selected:
p = (1-α)p + α
If not:
p = (1-α)p Where p is the selection probability, and α is the degree of weight decrease.
The result of this is that the nth most recent selection will have a weight of (1-α)^n.
Using a coefficient value of 0.05 as an example,
the 10th most recent selection would only have half the weight of the most recent.
Increasing epsilon would bias towards more recent results more.
"""
import news_classes
import os
import sys

#import common package in parent directory
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))
import mongodb_client
from cloudAMQP_client import CloudAMQPClient

NUM_OF_CLASS = 8
INITIAL_P = 1.0 / NUM_OF_CLASS
ALPHA = 0.1
SLEEP_TIME_IN_SECONDS = 2

LOG_CLICKS_TASK_QUEUE_URL = "amqp://bubrmmet:usDFsc4gNt1b3k3E4JAxjlmv30JrpWiV@gull.rmq.cloudamqp.com/bubrmmet"
LOG_CLICKS_TASK_QUEUE_NAME = "tap-news-clicks-news-task-queue"

PREFERENCE_MODEL_TABLE_NAME = "user_preference_model"
NEWS_TABLE_NAME = "news"
cloudAMQP_client = CloudAMQPClient(LOG_CLICKS_TASK_QUEUE_URL, LOG_CLICKS_TASK_QUEUE_NAME)

def handle_message(msg):
    if msg is None or not isinstance(msg, dict):
        print('message is broken')
        return

    if ('userId' not in msg or 'newsId' not in msg or 'timestamp' not in msg):
        return

    userId = msg['userId']
    newsId = msg['newsId']
    # if model exist, then
    # update user's preference
    # otherwise create new one
    db = mongodb_client.get_db()
    model = db[PREFERENCE_MODEL_TABLE_NAME].find_one({'userId':userId})

    # If model not exists, create a new one
    if model is None:
        print("Creating preference model for new user: %s" % userId)
        new_model = {'userId' : userId}
        preference = {}
        # initialize same value for each class
        # INITIAL_P: 1.0/8
        for i in news_classes.classes:
            preference[i] = float(INITIAL_P)
        new_model['preference'] = preference
        model = new_model
        print("Update prefernce model for user: %s" % userId)

    # Update model using time decay method.
    news = db[NEWS_TABLE_NAME].find_one({'digest': newsId})
    # news should have 'class' field
    # and the class should be in the news_class list
    if (news is None or 'class' not in news or news['class'] not in news_classes.classes):
        print("Skipping processing...")
        return

    # Update the clicked one.
    click_class = news['class']
    old_p = model['preference'][click_class]
    model['preference'][click_class] = float((1 - ALPHA) * old_p + ALPHA)

    # Update the non-clicked classes.
    for i, prob in model['preference'].items():
        if not i == click_class:
            old_p = model['preference'][i]
            model['preference'][i] = float((1 - ALPHA) * old_p)

    # upsert=True : if there is no record in database, then insert this record.
    db[PREFERENCE_MODEL_TABLE_NAME].replace_one({'userId': userId}, model, upsert=True)

def run():
    while True:
        if cloudAMQP_client is not None:
            msg = cloudAMQP_client.getMessage()
            if msg is not None:
                try:
                    handle_message(msg)
                except Exception as e:
                    print(e)
                    pass
            cloudAMQP_client.sleep(SLEEP_TIME_IN_SECONDS)

if __name__ == "__main__":
    run()
