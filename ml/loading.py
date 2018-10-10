# -*- coding: utf-8 -*-

# Script used to load all required data, functions, and models

import re
import pandas as pd  
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
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
    my_df = pd.read_csv('clean_tweet.csv',index_col=0)
    
    print('cleaned tweets')
    
    ################################################################
    # MODEL LOADING
    ################################################################
    # doc2vec 
    global model_ug_dbow
    model_ug_dbow = Doc2Vec.load('d2v_model_ug_dbow.doc2vec')
    model_ug_dbow.delete_temporary_training_data(keep_doctags_vectors=True, keep_inference=True)

    print('loaded doc2vec')
    
    # neural network
    import keras
    global new_model
    new_model = keras.models.load_model('my_model.h5')
    new_model.summary()





