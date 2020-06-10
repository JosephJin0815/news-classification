import os
import shutil
from sklearn import metrics

import numpy as np
import pandas as pd
import tensorflow as tf

from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.utils import to_categorical
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from keras.layers import Dense, Input, Flatten, Dropout
from keras.layers import Conv1D, MaxPooling1D, Embedding, LSTM
from keras.models import Sequential
from tensorflow import keras
from keras import regularizers
import pickle

REMOVE_PREVIOUS_MODEL = True

MODEL_OUTPUT_DIR = '../model/'
DATA_SET_FILE = '../data/labeled_news.csv'
VARS_FILE = '../model/vars'
#VOCAB_PROCESSOR_SAVE_FILE = '../model/vocab_procesor_save_file'

TOKENIZER_SAVE_FILE = '../model/tokenizer.pickle'
#DATA_SET_FILE = '../data/DATA_SET_FILE.csv'
DATA_SET_FILE  = '../data/labeled_news.csv'
MAX_SEQUENCE_LENGTH = 100 # maximum length of a sentence
EMBEDDING_DIM = 100 # word dimensions
VALIDATION_SPLIT = 0.16 # the proportion of validation set to all set
TEST_SPLIT = 0.2 # the proportion of test set to all set
LEARNING_RATE = 0.01
EPOCHS = 10
BATCH_SIZE = 256


def run():
    # REMOVE_PREVIOUS_MODEL: true: remove previous result
    # otherwise, train based on previous result
    if REMOVE_PREVIOUS_MODEL:
        # Remove old model
        print("Removing previous model...")
        shutil.rmtree(MODEL_OUTPUT_DIR)
        os.mkdir(MODEL_OUTPUT_DIR)

    # Prepare training and testing data
    data_df = pd.read_csv(DATA_SET_FILE, header=None)
    data_df = data_df[1:]
    data_df = data_df.reindex(np.random.permutation(data_df.index))

    sentences=data_df[1]
    labels=data_df[6]

    # Process vocabulary
    tokenizer = Tokenizer()
    tokenizer.fit_on_texts(sentences[:8958])
    word_index = tokenizer.word_index
    print('Found %s unique tokens.' % len(word_index))

    # Because we must use same vocabulary processor for both
    # training and prediction, we should store the vocabulary processor
    # Saving n_words and vocab_processor:
    with open(TOKENIZER_SAVE_FILE, 'wb') as handle:
        pickle.dump(tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)

    sequences = tokenizer.texts_to_sequences(sentences)
    word_index = tokenizer.word_index
    print('Found %s unique tokens.' % len(word_index))
    data = pad_sequences(sequences, maxlen=MAX_SEQUENCE_LENGTH)
    print(np.unique(labels))
    labels = to_categorical(np.asarray(labels))
    print('Shape of data tensor:', data.shape)
    print('Shape of label tensor:', labels.shape)

    p1 = int(len(data)*(1-VALIDATION_SPLIT-TEST_SPLIT))
    p2 = int(len(data)*(1-TEST_SPLIT))
    x_train = data[:p1]
    y_train = labels[:p1]
    x_val = data[p1:p2]
    y_val = labels[p1:p2]
    x_test = data[p2:]
    y_test = labels[p2:]
    print('train docs: '+str(len(x_train)))
    print('val docs: '+str(len(x_val)))
    print('test docs: '+str(len(x_test)))

    # Build model
    model = Sequential()
    model.add(Embedding(len(word_index) + 1, EMBEDDING_DIM, input_length=MAX_SEQUENCE_LENGTH))
    model.add(LSTM(200, dropout=0.2, recurrent_dropout=0.2))
    model.add(Dropout(0.2))
    model.add(Dense(labels.shape[1], activation='softmax'))
    model.summary()

    opt = keras.optimizers.RMSprop(learning_rate=LEARNING_RATE)
    model.compile(loss='categorical_crossentropy', optimizer = opt, metrics=['acc'])

    # Train and predict
    history = model.fit(x_train, y_train, validation_data=(x_val, y_val), epochs=EPOCHS, batch_size=BATCH_SIZE)
    model.save(VARS_FILE)

    # Evaluate model
    print(model.evaluate(x_test, y_test, verbose=False))

if __name__ == "__main__":
    run()
