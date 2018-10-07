# -*- coding: utf-8 -*-

##########################################################################
################## IGNORE THIS FILE! USED FOR TESTING PURPOSES ###########
###########################################################################

import re
import pandas as pd  
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
tqdm.pandas(desc="progress-bar")
from gensim.models import Doc2Vec
from gensim.models.doc2vec import LabeledSentence
import multiprocessing
from sklearn import utils
from bs4 import BeautifulSoup
from nltk.tokenize import WordPunctTokenizer

################################################################
# DATA CLEANING AND PREPARATION
################################################################
tok = WordPunctTokenizer()
pat1 = r'@[A-Za-z0-9_]+' # removing @ tags
pat2 = r'https?://[^ ]+' # removing https pages
combined_pat = r'|'.join((pat1, pat2))
www_pat = r'www.[^ ]+'   # removing www pages
# handling contraction words
negations_dic = {"isn't":"is not", "aren't":"are not", "wasn't":"was not", "weren't":"were not",
                "haven't":"have not","hasn't":"has not","hadn't":"had not","won't":"will not",
                "wouldn't":"would not", "don't":"do not", "doesn't":"does not","didn't":"did not",
                "can't":"can not","couldn't":"could not","shouldn't":"should not","mightn't":"might not",
                "mustn't":"must not"}
neg_pattern = re.compile(r'\b(' + '|'.join(negations_dic.keys()) + r')\b')

def tweet_cleaner(text):
    soup = BeautifulSoup(text, 'lxml')
    souped = soup.get_text()
    try:
        bom_removed = souped.decode("utf-8-sig").replace(u"\ufffd", "?")
    except:
        bom_removed = souped
    stripped = re.sub(combined_pat, '', bom_removed)
    stripped = re.sub(www_pat, '', stripped)
    lower_case = stripped.lower()
    neg_handled = neg_pattern.sub(lambda x: negations_dic[x.group()], lower_case)
    letters_only = re.sub("[^a-zA-Z]", " ", neg_handled)
    # tokenize and join to remove uncessary white spaces
    words = [x for x  in tok.tokenize(letters_only) if len(x) > 1]
    return (" ".join(words)).strip()

csv = 'clean_tweet.csv'
my_df = pd.read_csv(csv,index_col=0)
my_df.dropna(inplace=True)
my_df.reset_index(drop=True,inplace=True)

x = my_df.text
y = my_df.target
from sklearn.cross_validation import train_test_split
x_train, x_validation_and_test, y_train, y_validation_and_test = train_test_split(x, y, test_size=0.25)
x_validation, x_test, y_validation, y_test = train_test_split(x_validation_and_test, y_validation_and_test, test_size=.5)


################################################################
# MODEL LOADING
################################################################
from gensim.models import Doc2Vec

def get_concat_vectors(model1, corpus, size):
    vecs = np.zeros((len(corpus), size))
    n = 0
    for i in corpus.index:
        prefix = 'all_' + str(i)
        vecs[n] = model1.docvecs[prefix]
        n += 1
    return vecs

# doc2vec 
model_ug_dbow = Doc2Vec.load('d2v_model_ug_dbow.doc2vec')
model_ug_dbow.delete_temporary_training_data(keep_doctags_vectors=True, keep_inference=True)
train_vecs_ugdbow = get_concat_vectors(model_ug_dbow, x_train, 100)
validation_vecs_ugdbow = get_concat_vectors(model_ug_dbow, x_validation, 100)

# neural network
import keras
import numpy as np

from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.layers import Flatten
from keras.layers.embeddings import Embedding
from keras.preprocessing import sequence

# Initial model: 1 hidden layer with 64 hidden nodes
model_d2v_01 = Sequential()
model_d2v_01.add(Dense(64, activation='relu', input_dim=100))
model_d2v_01.add(Dropout(0.3))
model_d2v_01.add(Dense(1, activation='sigmoid'))
model_d2v_01.compile(optimizer='adam',
              loss='binary_crossentropy',
              metrics=['accuracy'])

model_d2v_01.fit(train_vecs_ugdbow, y_train,
                 validation_data=(validation_vecs_ugdbow, y_validation),
                 epochs=10, batch_size=32, verbose=2)

new_model = keras.models.load_model('my_model.h5')
new_model.summary()

################################################################
# PREDICTION/CLASSIFICATION OF NEW TWEETS
# 1. collect new tweet from API
# 2. clean tweet 
# 3. produce doc2vec representation of tweet
# 4. input this vector into neural network to classify tweet
################################################################

# retrieve tweet from API and put into a list
tweets_from_API = ['@TSLA tesla is such a great stock to buy', 'today was a terrible day @GOOG sad', 'wobcke grumpy #TSLA']
cleaned_tweets = []
num_tweets = len(tweets_from_API)

# clean tweets
cleaned_tweets = [tweet_cleaner(tweet) for tweet in tweets_from_API]

# convert to series 
new_tweet = pd.Series(cleaned_tweets)

# feed tweets into doc2vec model
infer_vector = [model_ug_dbow.infer_vector(tweet) for tweet in new_tweet]
for i in range(0,num_tweets-1):
    if i == 0:
        input_vectors = infer_vector[i]
    input_vectors = np.append(input_vectors, infer_vector[i])
    
# classify tweets as good/bad
ynew = new_model.predict_classes(infer_vector.reshape(num_tweets,100))

# classification vector of 0s and 1s
ynew # I forgot which is which i.e. (0,1)=(good, bad) or vice-versa)






