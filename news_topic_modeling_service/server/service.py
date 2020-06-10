import news_classes
import numpy as np
import os
import pandas as pd
import pickle
import sys
import tensorflow as tf
import time

from jsonrpclib.SimpleJSONRPCServer import SimpleJSONRPCServer
#from tensorflow.contrib.learn.python.learn.estimators import model_fn
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from keras.preprocessing.sequence import pad_sequences
from tensorflow import keras
from keras.utils import to_categorical
from keras.layers import LSTM

# import packages in trainer
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'trainer'))
#import news_cnn_model

#learn = tf.contrib.learn

SERVER_HOST = 'localhost'
SERVER_PORT = 6060

MODEL_DIR = '../model'
MODEL_UPDATE_LAG_IN_SECONDS = 10

TOKENIZER_SAVE_FILE = '../model/tokenizer.pickle'
#DATA_SET_FILE = '../data/DATA_SET_FILE.csv'
DATA_SET_FILE  = '../data/labeled_news.csv'
MAX_SEQUENCE_LENGTH = 100 # maximum length of a sentence
EMBEDDING_DIM = 100 # word dimensions
VALIDATION_SPLIT = 0.16 # the proportion of validation set to all set
TEST_SPLIT = 0.2 # the proportion of test set to all set
LEARNING_RATE = 0.01
EPOCHS = 2
BATCH_SIZE = 256

#N_CLASSES = 8

VARS_FILE = '../model/vars'
# VOCAB_PROCESSOR_SAVE_FILE = '../model/vocab_procesor_save_file'
TOKENIZER_SAVE_FILE = '../model/tokenizer.pickle'

#n_words = 0

#MAX_DOCUMENT_LENGTH = 500
#vocab_processor = None

#classifier = None

"""
def restoreVars():
    with open(VARS_FILE, 'rb') as f:
        global n_words
        n_words = pickle.load(f)


    global vocab_processor
    vocab_processor = learn.preprocessing.VocabularyProcessor.restore(
        VOCAB_PROCESSOR_SAVE_FILE)
"""
def restoreVars():
    global tokenizer
    # loading
    with open(TOKENIZER_SAVE_FILE, 'rb') as handle:
        tokenizer = pickle.load(handle)
"""
def loadModel():
    global classiﬁer
    # use n_words to initialize the model
    classiﬁer = learn.Estimator(
        model_fn=news_cnn_model.generate_cnn_model(N_CLASSES, n_words),
        model_dir=MODEL_DIR)
"""
def loadModel():
    global model
    model = keras.models.load_model(VARS_FILE)

    # Prepare training and testing
    """
    df = pd.read_csv('../data/labeled_news.csv', header=None)

    # TODO: fix this until https://github.com/tensorflow/tensorflow/issues/5548 is solved.
    # We have to call evaluate or predict at least once to make the restored Estimator work.
    train_df = df[0:400]
    x_train = train_df[1]
    x_train = np.array(list(vocab_processor.transform(x_train)))
    y_train = train_df[0]
    classifier.evaluate(x_train, y_train)
    """
restoreVars()
loadModel()


class ReloadModelHandler(FileSystemEventHandler):
    def on_any_event(self, event):
        # Reload model
        print("Model update detected. Loading new model.")
        time.sleep(MODEL_UPDATE_LAG_IN_SECONDS)
        retoreVars()
        loadModel()


observer = Observer()
observer.schedule(ReloadModelHandler(), path=MODEL_DIR, recursive=False)
observer.start()

def classify(text):
    # get row of text
    #text_series = pd.Series([text])
    # vocab_processor is stored when we training the data
    """
    predict_x = np.array(list(vocab_processor.transform(text_series)))
    print(predict_x)

    y_predicted = [
        p['class'] for p in classifier.predict(
            predict_x, as_iterable=True)
    ]
    print(y_predicted[0])
    """
    text_list = []
    text_list.append(text)
    predict_x = tokenizer.texts_to_sequences(text_list)
    predict_x = pad_sequences(predict_x, maxlen=MAX_SEQUENCE_LENGTH)
    #y_predicted = model.predict_classes(predict_x)
    y_predicted = np.argmax(model.predict(predict_x), axis=-1)
    print(y_predicted)
    print('------------------')
    topic = news_classes.class_map[str(y_predicted[0])]
    print('news type'+topic)
    return topic

sentence = 'I like sports, for example nba and football'
classify(sentence)

RPC_SERVER = SimpleJSONRPCServer((SERVER_HOST, SERVER_PORT))
RPC_SERVER.register_function(classify, 'classify')

print(("Starting RPC server on %s:%d" % (SERVER_HOST, SERVER_PORT)))

RPC_SERVER.serve_forever()
