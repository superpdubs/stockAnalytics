#!/usr/bin/env python

import twitter
# import apiKey
from resources import apiKey
from _datetime import datetime, timedelta
from newsapi import NewsApiClient
import pyEX
import json
import requests
import csv
import ml.classifier

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
	print([t.text for t in results])
	tweets_from_API = [t.text for t in results]

	ml.classifier.classifier(tweets_from_API)
	return results

# print(twitterAdvancedSearch(query="AAPL", resultType="popular", count=10))

# print([r for r in twitterAdvancedSearch(query="Microsoft",
#                                      resultType="recent",
#                                      count="5")])


def twitterEmbed(status_id, url):
	result = api.GetStatusOembed(status_id=status_id, url=url, hide_media=True)
	return result

# print(twitterEmbed(status_id=1037962403370225664, url="https://t.co/qvUU30HkJM"))

# print(twitterEmbed(status_id=1041699384151498754, url="https://t.co/bwQz4nOJHd"))



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

def pyEXLivePrice(query):

	livePrice = pyEX.price(query)
	return livePrice

def pyEXChart(query):

	# chartData = pyEX.chart(symbol=query, timeframe='6m')
	chartData = pyEX.chart(symbol=query)

	price = []
	date = []

	for x in chartData:
		price.append(x['close'])
		date.append(x['date'])

	return price, date

# pyEXChart("AAPL")

def iEXManualRequest(query):

	print("accessing endpoint")
	payload = {'symbols': query, 'types': 'ohlc,price,news,company,chart'}
	r = requests.get("https://api.iextrading.com/1.0/stock/market/batch", params=payload)
	print(r.url)

	price = r.json()[query]["price"]

	close = []
	date = []
	for x in r.json()[query]["chart"]:
		close.append(x['close'])
		date.append(x['date'])

	ohlc = r.json()[query]["ohlc"]
	if (ohlc["open"]["time"] >= ohlc["close"]["time"]):
		ohlc.update({'live': True})
	if (ohlc["open"]["time"] < ohlc["close"]["time"]):
		ohlc.update({'live': False})

	company = r.json()[query]["company"]
	news = r.json()[query]["news"]

	print(datetime.now())
	return price, close, date, ohlc, company, news

# iEXManualRequest("AAPL");
