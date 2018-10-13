# -*- coding: utf-8 -*-

# Followed and adapted parts (1-10) of the blog:
# https://towardsdatascience.com/another-twitter-sentiment-analysis-bb5b01ebad90

##############################################################################
##### CLEAN THE DATA (TWEETS)
##############################################################################

import pandas as pd  
# load the data
cols = ['sentiment','id','date','query_string','user','text']
df = pd.read_csv("C:/Users/Patrick/Documents/GitHub/stockAnalytics/ml/training.1600000.processed.noemoticon.csv",header=None, names=cols, encoding="ISO-8859-1")
#df = pd.read_csv("/Users/patrick/Documents/GitHub/stockAnalytics/ml/training.1600000.processed.noemoticon.csv",header=None, names=cols, encoding="ISO-8859-1")
 
# dropping useless columns
df.drop(['id','date','query_string','user'],axis=1,inplace=True) 

import re
from bs4 import BeautifulSoup

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

#testing = df.text[:100]
#test_result = []
#for t in testing:
#    test_result.append(tweet_cleaner(t))
#test_result


# DATA CLEANING IN PROCESS
nums = [0,1600000]
print("Cleaning...\n")
clean_tweet_texts = []
for i in range(nums[0],nums[1]):
    if (i+1)%10000 == 0:
        print("Tweets %d of %d has been processed" % ( i+1, nums[1] ))
    clean_tweet_texts.append(tweet_cleaner(df['text'][i]))
len(clean_tweet_texts)    
            
clean_df = pd.DataFrame(clean_tweet_texts,columns=['text'])
clean_df['target'] = df.sentiment
clean_df.head()

# remove NULL entries i.e. tweets with only @'s or urls
clean_df.dropna(inplace=True)
clean_df.reset_index(drop=True,inplace=True)

# save as csv
clean_df.to_csv('cleaned_tweets.csv',encoding='utf-8')