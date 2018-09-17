#!/usr/bin/env python

import twitter
# import apiKey
from resources import apiKey
from _datetime import datetime, timedelta
from newsapi import NewsApiClient
import pyEX
import json

########
# init API key Settings
########

# init Twitter API keys
api = twitter.Api(consumer_key=apiKey.twitter_consumerKey,
                  consumer_secret=apiKey.twitter_consumerSecret,
                  access_token_key=apiKey.twitter_accessToken,
                  access_token_secret=apiKey.twitter_accessSecret
                  )

# init NewsAPI API keys
newsapi = NewsApiClient(api_key=apiKey.newsAPI_Key)


# Basic search for Twitter tweets, returns 10 tweets
def twitterBasicSearch(query):
    queryString = "q={}&result_type=recent&count=10".format(query)
    # queryString = f"q={query}&result_type=recent&count=10&lang=en"
    results = api.GetSearch(raw_query=queryString)
    return results


# print([r for r in twitterBasicSearch(query="Microsoft")])


# Advanced search, allowing for query, result_type and count modifications
def twitterAdvancedSearch(query, resultType, count):
    queryString = "q={}&result_type={}&count={}&lang=en".format(query, resultType, count)
    results = api.GetSearch(raw_query=queryString)
    return results

print(twitterAdvancedSearch(query="AAPL", resultType="popular", count=10))

# print([r for r in twitterAdvancedSearch(query="Microsoft",
#                                      resultType="recent",
#                                      count="5")])

# Everything search, gets the last 2 weeks of most recent news
def newsApiEverythingSearch(query):
    date_fortnightAgo = datetime.now() - timedelta(days=14)
    date_fortnightAgo = date_fortnightAgo.strftime("%Y-%m-%d")
    date_now = datetime.now().strftime("%Y-%m-%d")

    results = newsapi.get_everything(q=query,
                                     language="en",
                                     sort_by="relevancy",
                                     from_param=date_fortnightAgo,
                                     to=date_now)

    # print(results.get('articles'))


# print(newsApiEverythingSearch(query="Apple"))

def pyEXTest(query):
    result = pyEX.ohlc(query);
    return result

# print(pyEXTest("AAPL"))

def pyEXStockInfo(query):

    queryResult = pyEX.ohlc(query)

    currentPrice = pyEX.price(query)

    company = pyEX.company(query)

    if (queryResult.get('open').get('time') >= queryResult.get('close').get('time')):
        queryResult.update({'live': True})

    if (queryResult.get('open').get('time') < queryResult.get('close').get('time')):
        queryResult.update({'live': False})

    queryResult.update({'currentPrice': currentPrice})
    queryResult.update({'companyDetails': company})

    return queryResult


# print(pyEXStockInfo("AAPL"))

def pyEXNews(query):

    newsResult = pyEX.news(query, count=10)
    return newsResult

# print(pyEXNews("AAPL"))