# -*- coding: utf-8 -*-

#Imports
from flask import Flask, jsonify, url_for, redirect, request
from flask_pymongo import PyMongo
from flask_restful import Api, Resource
from flask_cors import CORS, cross_origin
from requests import get, post, put, delete
import tweepy
import csv
import json
from HTMLParser import HTMLParser

#App Configurations
app = Flask(__name__)
app.config["MONGO_DBNAME"] = "tweets_db"
mongo = PyMongo(app, config_prefix='MONGO')
APP_URL = "http://127.0.0.1:5000"
CORS(app)

# Twitter API credentials
consumer_key = "NGaZMivs4c4z90l7wOlGcRT4H"
consumer_secret = "Q68NpvZA3nkaiE68JHG14NxjWB6bYsrLiTFVQvuqLEf2k3ZTkn"
access_key = "835375692825100288-nhFWSCFVHezFMQ4nlmdIBF5PdKR4PRO"
access_secret = "86AJTwkCN3tbmjAmyzTjeYRRIfOibginaVvi0klBnYDvi"

#authorize twitter, initialize tweepy
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)

#Get all the tweets and their metadata
@app.route('/tweets', methods=['GET'])
def getAllTweets():
	tweets = mongo.db.tweets
	output = []
	for t in tweets.find():
		output.append({'tweet_id' : t['tweet_id'], 
						'tweet_time' : t['tweet_time'], 
						'tweet_screen_name' : t['tweet_screen_name'],
						'tweet_text' : t['tweet_text'],
						'tweet_lang' : t['tweet_lang'],
						'tweet_user_followers_count' : t['tweet_user_followers_count'],
						'tweet_user_friends_count' : t['tweet_user_friends_count'],
						'tweet_user_listed_count' : t['tweet_user_listed_count'],
						'tweet_user_favourites_count' : t['tweet_user_favourites_count'],
						'tweet_retweet_count' : t['tweet_retweet_count'],
						'tweet_in_reply_to_screen_name' : t['tweet_in_reply_to_screen_name'],
						'tweet_place_country' : t['tweet_place_country'],
						'tweet_place_name' : t['tweet_place_name'],
						'tweet_entities_hashtags' : t['tweet_entities_hashtags'],
						'tweet_entities_urls' : t['tweet_entities_urls'],
						'tweet_entities_user_mentions_name' : t['tweet_entities_user_mentions_name'],
						'tweet_entities_user_mentions_screen_name' : t['tweet_entities_user_mentions_screen_name']
						})
	return jsonify({'result' : output})

#Get all tweets(limit set to 500, can be modified) matching a search_string and push them to database
@app.route('/tweets', methods=['GET','POST'])
def searchQuery():
	search_string = request.data
	max_tweets = 500
	searched_tweets = []
	last_id = -1
	while len(searched_tweets) < max_tweets:
		count = max_tweets - len(searched_tweets)
		try:
			new_tweets = api.search(q=search_string, count=count, max_id=str(last_id - 1))
			if not new_tweets:
				break
			searched_tweets.extend(new_tweets)
			last_id = new_tweets[-1].id
		except tweepy.TweepError as e:
			break

	tweets = mongo.db.tweets
	tweets.remove({})
	output = []
	for tweet in searched_tweets:
		tweet_id = tweet.id_str
		tweet_time = tweet.created_at
		tweet_text = tweet.text.encode("utf-8")
		tweet_screen_name = tweet.user.screen_name
		tweet_in_reply_to_screen_name = tweet.in_reply_to_screen_name
		tweet_lang = tweet.user.lang
		tweet_user_followers_count = tweet.user.followers_count
		tweet_user_friends_count = tweet.user.friends_count
		tweet_user_listed_count = tweet.user.listed_count
		tweet_user_favourites_count = tweet.user.favourites_count
		tweet_retweet_count = tweet.retweet_count
		tweet_entities_hashtags = tweet.entities[u'hashtags']
		tweet_entities_urls = tweet.entities[u'urls']
		tweet_entities_user_mentions = tweet.entities[u'user_mentions']
		tweet_entities_user_mentions_name = ""
		tweet_entities_user_mentions_screen_name = ""
		for vals in tweet_entities_user_mentions:
			tweet_entities_user_mentions_name = vals[u'name']
			tweet_entities_user_mentions_screen_name = vals[u'screen_name']
		tweet_place_country = ""
		tweet_place_name = ""
		if tweet.place is not None:
			tweet_place_country = tweet.place.country
			tweet_place_name = tweet.place.name
		
		tweet = tweets.insert({
								'tweet_id' : tweet_id, 
								'tweet_time' : tweet_time,
								'tweet_screen_name' : tweet_screen_name,
								'tweet_text' : tweet_text, 
								'tweet_lang' : tweet_lang,
								'tweet_user_followers_count' : tweet_user_followers_count,
								'tweet_user_friends_count' : tweet_user_friends_count,
								'tweet_user_listed_count' : tweet_user_listed_count,
								'tweet_user_favourites_count' : tweet_user_favourites_count,
								'tweet_retweet_count' : tweet_retweet_count,
								'tweet_in_reply_to_screen_name' : tweet_in_reply_to_screen_name,
								'tweet_place_country' : tweet_place_country,
								'tweet_place_name' : tweet_place_name,
								'tweet_entities_hashtags' : tweet_entities_hashtags,
								'tweet_entities_urls' : tweet_entities_urls,
								'tweet_entities_user_mentions_name' : tweet_entities_user_mentions_name,
								'tweet_entities_user_mentions_screen_name' : tweet_entities_user_mentions_screen_name
							})
		
		inside_output = {
							'tweet_id' : tweet_id, 
							'tweet_time' : tweet_time,
							'tweet_screen_name' : tweet_screen_name,
							'tweet_text' : tweet_text, 
							'tweet_lang' : tweet_lang,
							'tweet_user_followers_count' : tweet_user_followers_count,
							'tweet_user_friends_count' : tweet_user_friends_count,
							'tweet_user_listed_count' : tweet_user_listed_count,
							'tweet_user_favourites_count' : tweet_user_favourites_count,
							'tweet_retweet_count' : tweet_retweet_count,
							'tweet_in_reply_to_screen_name' : tweet_in_reply_to_screen_name,
							'tweet_place_country' : tweet_place_country,
							'tweet_place_name' : tweet_place_name,
							'tweet_entities_hashtags' : tweet_entities_hashtags,
							'tweet_entities_urls' : tweet_entities_urls,
							'tweet_entities_user_mentions_name' : tweet_entities_user_mentions_name,
							'tweet_entities_user_mentions_screen_name' : tweet_entities_user_mentions_screen_name
						}

		output.append(inside_output)
	return jsonify({'result' : output})

#Get output of all tweets containing their text only
@app.route('/tweets/text', methods=['GET'])
def getTweetsText():
	tweets = mongo.db.tweets
	output = []
	for t in tweets.find():
		output.append({

			'tweet' : t['tweet_text']})
	return jsonify({'result' : output})

#Text Search in tweet text/user name
@app.route('/tweets/text', methods=['POST'])
def searchTextInTweet():
	keyword = request.data
	tweets = mongo.db.tweets
	output = []
	for t in tweets.find():
		text = t['tweet_text'].encode("utf-8")
		screen_name = t['tweet_screen_name'].encode("utf-8")
		if keyword in text or keyword in screen_name:
			output.append({
								'tweet' : t['tweet_text'],
								'screen_name' : t['tweet_screen_name']
						})
	return jsonify({'result' : output})

#Main program
if __name__ == '__main__':
    app.run(debug=True)