# -*- coding: utf-8 -*-

# Script used to load all required data, functions, and models

def load():
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

    # doc2vec 
    global model_ug_dbow
    model_ug_dbow = Doc2Vec.load('d2v_model_ug_dbow.doc2vec')
    model_ug_dbow.delete_temporary_training_data(keep_doctags_vectors=True, keep_inference=True)
    #train_vecs_ugdbow = get_concat_vectors(model_ug_dbow, x_train, 100)
    #validation_vecs_ugdbow = get_concat_vectors(model_ug_dbow, x_validation, 100)

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





