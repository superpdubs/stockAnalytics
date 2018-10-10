# -*- coding: utf-8 -*-

# Script used to load all required data, functions, and models
import keras
from gensim.models import Doc2Vec

def load():    
    ################################################################
    # MODEL LOADING
    ################################################################
    # doc2vec 
    global model_ug_dbow
    model_ug_dbow = Doc2Vec.load('d2v_model_ug_dbow.doc2vec')
    model_ug_dbow.delete_temporary_training_data(keep_doctags_vectors=True, keep_inference=True)

    print('loaded doc2vec')
    
    # neural network
    global new_model
    new_model = keras.models.load_model('my_model.h5')
    new_model.summary()





