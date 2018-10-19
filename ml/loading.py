# -*- coding: utf-8 -*-

# Script used to load all required data, functions, and models

import numpy as np
import keras
from gensim.models import Doc2Vec

def loadDoc():
    # doc2vec
    model_ug_dbow = Doc2Vec.load('ml/d2v_model.doc2vec')
    model_ug_dbow.delete_temporary_training_data(keep_doctags_vectors=True, keep_inference=True)

    print('loaded doc2vec')
    return model_ug_dbow

def loadNeural():
    # neural network
    neural_model = keras.models.load_model('ml/my_model.h5')
    print('testing model:', neural_model.predict(np.zeros((3,100))))
    neural_model.summary()
    return neural_model
