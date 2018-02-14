# -*- coding: utf-8 -*-

#Imports
import csv, json, itertools, re, time, tweepy, os, errno
from flask import Flask, jsonify, url_for, redirect, request
from flask_pymongo import PyMongo
from flask_restful import Api, Resource
from flask_cors import CORS, cross_origin
from requests import get, post, put, delete
from HTMLParser import HTMLParser
from googleplaces import GooglePlaces, types, lang
from locations import *
import searchTweets
import filterTweets

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

# Google Places API
YOUR_API_KEY = 'AIzaSyDsb7cZdFqYBL3L6uFc2Wc-YJxaaWFjNnE'
google_places = GooglePlaces(YOUR_API_KEY)

# Check whether CSV Folder exists. Create, if not.
def checkCSVFolder():
	try:
		os.makedirs("CSV")
	except OSError as e:
		if e.errno != errno.EEXIST:
			raise

# Stream twitter feed. Twitter only allows access to a users most recent 3240 tweets with this method
@app.route('/twitter', methods=['GET'])
def streamFeed():
	screen_name = request.args.get('name')
	checkCSVFolder()
	return jsonify({'result' : searchTweets.getTweetsOfScreenName(api, screen_name)})

# Get all tweets(limit set to 500, can be modified) matching a search_string and push them to database.
@app.route('/tweets/get', methods=['GET'])
def searchQuery():
	search_string = request.args.get('find')
	page = int(request.args.get('page'))
	checkCSVFolder()
	return jsonify({'result' : searchTweets.getAllTweets(mongo, api, search_string, page)})

#Get output of all tweets containing their text only.
@app.route('/tweets/texts', methods=['GET'])
def getTweetsText():
	page = int(request.args.get('page'))
	checkCSVFolder()
	return jsonify({'result' : filterTweets.getTweetsWithText(mongo, page)})

# Text Search in tweet text/user name.
@app.route('/tweets/text', methods=['GET'])
def searchTextInTweet():
	keyword = request.args.get('text')
	checkCSVFolder()
	return jsonify({'result' : textSearchInTweetOrUsername(mongo, keyword)})

# Sort data based on date/time.
@app.route('/tweets/date', methods=['GET'])
def sortByDate():
	page = int(request.args.get('page'))
	asc = request.args.get('sort')
	checkCSVFolder()
	return jsonify({'result' : filterTweets.sortByDate(mongo, asc, page)})

# Filtering on values
@app.route('/tweets/filter', methods=['GET'])
def filterTweetsByCondition():
	expression = request.args.get('get')
	page = int(request.args.get('page'))
	checkCSVFolder()
	return jsonify({'result' : filterTweets.conditionFilter(mongo, expression, page)})

# Regex matching of a given string
@app.route('/tweets/search', methods=['GET'])
def matchString():
	keyword = request.args.get('find')
	page = request.args.get('page')
	checkCSVFolder()
	return jsonify({'result' : filterTweets.regexMatchtweets(mongo, keyword, page)})

# Getting Tweets of a nearby location
@app.route('/tweets/nearby', methods=['GET'])
def getNearbyTweets():
	place = request.args.get('place')
	output = getTweets(place)
	checkCSVFolder()
	return jsonify({'result' : getTweets(place)})

# Main program
if __name__ == '__main__':
	app.run(debug=True)