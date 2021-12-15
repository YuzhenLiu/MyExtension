import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cookies_analyser.settings")
os.environ.setdefault('TF_CPP_MIN_LOG_LEVEL', '2')

import django

django.setup()

import sqlite3
import numpy as np
import pandas as pd
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import load_model
from analyser.models import Cookie, Temp

connection = sqlite3.connect('db.sqlite3', check_same_thread=False)
alphabet = "0123456789abcdefghijklmnopqrstuvwxyz()<>{}[]+-/=~`!@#$%^&*,;.?:_|\"'\\"


def classify():
    classifier = load_model('model.h5')
    data, cookie_ids = preprocess()
    if data.size == 0:
        return
    predictions = classifier.predict(data, batch_size=128, verbose=2)
    count = 0
    for prediction in predictions:
        if prediction[1] >= 0.5:
            Temp.objects.filter(id=cookie_ids[count]).update(isMalicious=1)
        else:
            Temp.objects.filter(id=cookie_ids[count]).update(isMalicious=0)
        count += 1


def preprocess():
    df = pd.read_sql_query("SELECT * FROM analyser_temp", connection)
    cookie_ids = df['id'].values
    texts = df['value'].values
    texts = [text.lower() for text in texts]
    token = Tokenizer(num_words=None, char_level=True, oov_token='UNK')
    token.fit_on_texts(texts)
    char_dict = {}
    for i, char in enumerate(alphabet):
        char_dict[char] = i + 1
    token.word_index = char_dict.copy()
    token.word_index[token.oov_token] = max(char_dict.values()) + 1

    sequences = token.texts_to_sequences(texts)
    data = pad_sequences(sequences, maxlen=512, padding='post')
    data = np.array(data, dtype='float32')
    return data, cookie_ids


if __name__ == '__main__':
    print('Classifying...')
    classify()
