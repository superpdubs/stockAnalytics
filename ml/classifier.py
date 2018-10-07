# Script used to deal with new tweets; classifying them

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



