import click_log_processor
import os
import sys

from datetime import datetime

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))
import mongodb_client

PREFERENCE_MODEL_TABLE_NAME = "user_preference_model"
NEWS_TABLE_NAME = "news"
NUM_OF_CLASS = 8

def test_basic():
    db = mongodb_client.get_db()
    db[PREFERENCE_MODEL_TABLE_NAME].delete_many({'userId': 'test_user'})

    msg = {'userId':'test_user',
        'newsId':'c524274e6bf39e9b33c71619661b4441',
        'timestamp':str(datetime.utcnow())
    }

    click_log_processor.handle_message(msg)

    model = db[PREFERENCE_MODEL_TABLE_NAME].find_one({'userId':'test_user'})
    assert model is not None
    assert len(model['preference']) == NUM_OF_CLASS

    print('test case pass')

if __name__ == '__main__':
    test_basic()
