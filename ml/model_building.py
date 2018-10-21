#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Followed and adapted parts (1-10) of the blog:
# https://towardsdatascience.com/another-twitter-sentiment-analysis-bb5b01ebad90

##############################################################################
##### BUILDING DOC2VEC AND NEURAL NETWORK MODELS
##############################################################################

import pandas as pd  
import numpy as np
#my_df = pd.read_csv('cleaned_tweets.csv',index_col=0)

# SPLITTING DATA INTO TRAIN, VALIDATION, TEST
# clean_df is from data_preprocessing.py
# for some reason, using read.csv() method produces multiple NaN entries which were not present before 
x = clean_df.text
y = clean_df.target
from sklearn.cross_validation import train_test_split
x_train, x_validation, y_train, y_validation = train_test_split(x, y, test_size=0.1)

###########
# Doc2Vec. 
# WARNING: takes around an hour to train
# Guided by: https://medium.com/@mishra.thedeepak/doc2vec-simple-implementation-example-df2afbbfbad5
###########
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from nltk.tokenize import word_tokenize
import multiprocessing

cores = multiprocessing.cpu_count()
# aggregate all x
all_x = pd.concat([x_train,x_validation])

# tag each tweet (or document)
tagged_tweets = [TaggedDocument(words=word_tokenize(_d.lower()), tags=[str(i)]) for i, _d in enumerate(all_x)]

# build and train doc2vec model
max_epochs = 30
size = 100
alpha = 0.05

# define model
d2v_model = Doc2Vec(dm=0,
                    size=size,
                    alpha=alpha,
                    min_alpha=0.06,
                    min_count=1,
                    workers=cores)

d2v_model.build_vocab(tagged_tweets)

# train the model
for epoch in range(max_epochs):
    print('Iteration:', epoch)
    d2v_model.train(tagged_tweets,
                total_examples=d2v_model.corpus_count,
                epochs=d2v_model.iter) # try 1 epoch??  
    d2v_model.alpha -= 0.002
    d2v_model.min_alpha = d2v_model.alpha

d2v_model.save("d2v_model.doc2vec")

# d2v_model.docvecs contains an array of it's doc2vec vectors
# We are going to split them into their corresponding training and validation sets

# getting training doc2vec vectors
def get_train_vectors(model, corpus, size):
    vecs = np.zeros((len(corpus), size))
    for i in range(0,1440000):
        vecs[i] = d2v_model.docvecs[i]
    return vecs

# getting validation doc2vec vectors
def get_val_vectors(model, corpus, size):
    vecs = np.zeros((len(corpus), size))
    n = 0
    for i in range(1440001,160001):
        vecs[n] = d2v_model.docvecs[i]
        n += 1
    return vecs

train_vecs_d2v = get_train_vectors(d2v_model, x_train, 100)
val_vecs_d2v = get_val_vectors(d2v_model, x_validation, 100)


##################
# Neural network #
##################
# Neural network architecture
# -Take in a 100-dimensional vector produced by doc2vec model
# -One hidden layer with 64 nodes (reasonably minimal complexity)
# -30% dropout to make the model more generalisable and forcing it to learn what it 'needs' to
# -Output layer is a sigmoid layer with binary output (pos/neg)
# -Adams optimizer is used (good algo for basic, starter neural network)
# -binary crossentropy for the loss function since we are doing binary ouputs, not specific percentage sentiment
#################################
import keras

from keras.models import Sequential
from keras.layers import Dense, Dropout

    model = Sequential()
    model.add(Dense(64, activation='relu', input_dim=100))
    #model.add(Dense(256, activation='relu', input_dim=100))
    model.add(Dropout(0.3))
    #model.add(Dense(256, activation='relu'))
    #model.add(Dropout(0.5))
    #model.add(Dense(256, activation='relu'))
    #model.add(Dropout(0.5))
    model.add(Dense(1, activation='sigmoid'))
    model.compile(optimizer='adam',
                  loss='binary_crossentropy',
                  metrics=['accuracy'])
    
    model.fit(train_vecs_d2v, y_train,
                     validation_data=(val_vecs_d2v, y_validation),
                     epochs=10, batch_size=32, verbose=2)

model.save('my_model.h5')

# 256x256x256: 0.0932 -> 0.1139
