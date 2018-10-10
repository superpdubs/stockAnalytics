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
import matplotlib.pyplot as plt
from tqdm import tqdm
from gensim.models import Doc2Vec
from gensim.models.doc2vec import LabeledSentence
import multiprocessing
from sklearn import utils
from bs4 import BeautifulSoup
from nltk.tokenize import WordPunctTokenizer
    
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
    infer_vector = [model_ug_dbow.infer_vector(tweet) for tweet in input_tweets]
    for i in range(0,num_tweets-1):
        if i == 0:
            input_vectors = infer_vector[i]
        input_vectors = np.append(input_vectors, infer_vector[i])
    
    # classify tweets as good/bad
    ynew = new_model.predict_classes(input_vectors.reshape(num_tweets,100))
    
    # classification vector of 0s and 1s
    # example output: [[0],[1],[1]]
    print(ynew) # I forgot which is which i.e. (0,1)=(good, bad) or vice-versa
    return ynew








def tweet_cleaner(text):
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