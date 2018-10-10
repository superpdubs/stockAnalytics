# -*- coding: utf-8 -*-

# Script used to load all required data, functions, and models

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


def load():
    ################################################################
    # DATA CLEANING AND PREPARATION
    ################################################################

    csv = 'clean_tweet.csv'
    my_df = pd.read_csv(csv,index_col=0)
    my_df.dropna(inplace=True)
    my_df.reset_index(drop=True,inplace=True)
    
    print('cleaned tweets')
    
    x = my_df.text
    y = my_df.target
    from sklearn.cross_validation import train_test_split
    x_train, x_validation_and_test, y_train, y_validation_and_test = train_test_split(x, y, test_size=0.25)
    x_validation, x_test, y_validation, y_test = train_test_split(x_validation_and_test, y_validation_and_test, test_size=.5)

    print('splitted data')
    
    ################################################################
    # MODEL LOADING
    ################################################################
    from gensim.models import Doc2Vec

    # doc2vec 
    global model_ug_dbow
    model_ug_dbow = Doc2Vec.load('d2v_model_ug_dbow.doc2vec')
    model_ug_dbow.delete_temporary_training_data(keep_doctags_vectors=True, keep_inference=True)
    #train_vecs_ugdbow = get_concat_vectors(model_ug_dbow, x_train, 100)
    #validation_vecs_ugdbow = get_concat_vectors(model_ug_dbow, x_validation, 100)

    print('loaded doc2vec')
    
    # neural network
    import keras
    global new_model
    new_model = keras.models.load_model('my_model.h5')
    new_model.summary()

  
#def get_concat_vectors(model1, corpus, size):
#    vecs = np.zeros((len(corpus), size))
#        n = 0
#        for i in corpus.index:
#            prefix = 'all_' + str(i)
#            vecs[n] = model1.docvecs[prefix]
#            n += 1
#        return vecs





