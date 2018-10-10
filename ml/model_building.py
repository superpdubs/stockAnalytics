#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Followed and adapted parts (1-10) of the blog:
# https://towardsdatascience.com/another-twitter-sentiment-analysis-bb5b01ebad90

##############################################################################
##### BUILDING DOC2VEC AND NEURAL NETWORK MODELS
##############################################################################

import pandas as pd  
import numpy as np
my_df = pd.read_csv('cleaned_tweets.csv',index_col=0)

# SPLITTING DATA INTO TRAIN, VALIDATION, TEST
x = my_df.text
y = my_df.target
from sklearn.cross_validation import train_test_split
x_train, x_validation_and_test, y_train, y_validation_and_test = train_test_split(x, y, test_size=0.1)
x_validation, x_test, y_validation, y_test = train_test_split(x_validation_and_test, y_validation_and_test, test_size=.5)


###########
# Doc2Vec. 
# WARNING: takes around an hour to train
###########
from tqdm import tqdm
from gensim.models import Doc2Vec
from gensim.models.doc2vec import LabeledSentence
import multiprocessing
from sklearn import utils

# unigram model
def labelize_tweets_ug(tweets,label):
    result = []
    prefix = label
    for i, t in zip(tweets.index, tweets):
        result.append(LabeledSentence(t.split(), [prefix + '_%s' % i]))
    return result
  
all_x = pd.concat([x_train,x_validation,x_test])
all_x_w2v = labelize_tweets_ug(all_x, 'all')

# unigram DBOW 
cores = multiprocessing.cpu_count()
model_ug_dbow = Doc2Vec(dm=0, size=100, negative=5, min_count=2, workers=cores, alpha=0.065, min_alpha=0.065)
model_ug_dbow.build_vocab([x for x in tqdm(all_x_w2v)])

for epoch in range(30):
    model_ug_dbow.train(utils.shuffle([x for x in tqdm(all_x_w2v)]), total_examples=len(all_x_w2v), epochs=1)
    model_ug_dbow.alpha -= 0.002
    model_ug_dbow.min_alpha = model_ug_dbow.alpha
    
def get_vectors(model, corpus, size):
    vecs = np.zeros((len(corpus), size))
    n = 0
    for i in corpus.index:
        prefix = 'all_' + str(i)
        vecs[n] = model.docvecs[prefix]
        n += 1
    return vecs
  
train_vecs_dbow = get_vectors(model_ug_dbow, x_train, 100)
validation_vecs_dbow = get_vectors(model_ug_dbow, x_validation, 100)
model_ug_dbow.save('d2v_model_ug_dbow.doc2vec')


##################
# Neural network #
##################
import keras

from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.layers import Flatten
from keras.layers.embeddings import Embedding
from keras.preprocessing import sequence

# Initial model: 1 hidden layer with 64 hidden nodes
model_d2v_01 = Sequential()
model_d2v_01.add(Dense(64, activation='relu', input_dim=100))
#model_d2v_01.add(Dropout(0.3))
model_d2v_01.add(Dense(1, activation='sigmoid'))
model_d2v_01.compile(optimizer='adam',
              loss='binary_crossentropy',
              metrics=['accuracy'])

model_d2v_01.fit(train_vecs_dbow, y_train,
                 validation_data=(validation_vecs_dbow, y_validation),
                 epochs=10, batch_size=32, verbose=2)

model_d2v_01.save('my_model.h5')


