# Script used to deal with new tweets; classifying them

################################################################
# PREDICTION/CLASSIFICATION OF NEW TWEETS
# 1. collect new tweet from API
# 2. clean tweet
# 3. produce doc2vec representation of tweet
# 4. input this vector into neural network to classify tweet
################################################################

import re
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import app

# retrieve tweet from API and put into a list
def classifier(tweets_from_API):
    #tweets_from_API = ['@TSLA tesla is such a great stock to buy', 'today was a terrible day @GOOG sad', 'wobcke grumpy #TSLA']
    cleaned_tweets = []
    num_tweets = len(tweets_from_API)

    # clean tweets
    cleaned_tweets = [tweet_cleaner(tweet) for tweet in tweets_from_API]

    # convert to series
    input_tweets = pd.Series(cleaned_tweets)

    # feed tweets into doc2vec model
    infer_vector = [app.model_ug_dbow.infer_vector(tweet) for tweet in input_tweets]
    for i in range(0,num_tweets-1):
        if i == 0:
            input_vectors = infer_vector[i]
        input_vectors = np.append(input_vectors, infer_vector[i])
    
    # remember to do a dummy prediction after the model is loaded
    #ynew = app.neural_model.predict_classes(input_vectors.reshape(np.zeros((2,100)),100))
    
    # classify tweets as good/bad
    ynew = app.neural_model.predict_classes(input_vectors.reshape(num_tweets,100))  
    
    # classification vector of 0s and 1s
    # example output: [[1],[1],[1]]
    print('CLASSIFICATION VECTOR:', ynew) # I forgot which is which i.e. (0,1)=(good, bad) or vice-versa
    return ynew

# DATA CLEANING FUNCTION
def tweet_cleaner(text):
    # lower case first
    text = text.lower()

    # removing @ tags
    cleaned_at = re.sub(r'@[A-Za-z0-9_]+', '', text)

    # removing https pages
    cleaned_https = re.sub(r'https?://[^ ]+', '', cleaned_at)

    # removing www pages
    cleaned_www = re.sub(r'www.[^ ]+', '', cleaned_https)

    # decode HTML
    cleaned_html = BeautifulSoup(cleaned_www, 'lxml').get_text()

    # removing contraction words
    cleaned_contr = re.sub(r'n\'t', ' not', cleaned_html)

    # removing special characters
    cleaned_special = re.sub(r'[^ a-z]', '', cleaned_contr)

    # trailing whitespace/tabs
    cleaned_trail = re.sub(r'[ \t]+$', '', cleaned_special)

    # excess whitespace
    cleaned_all = re.sub(r'\s+', ' ', cleaned_trail)
    return cleaned_all