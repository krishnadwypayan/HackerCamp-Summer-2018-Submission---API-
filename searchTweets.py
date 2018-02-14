from main import *

#Function that prints the exception message.
def getExceptionMessage(msg):
    words = msg.split(' ')

    errorMsg = ""
    for index, word in enumerate(words):
        if index not in [0,1,2]:
            errorMsg = errorMsg + ' ' + word
    errorMsg = errorMsg.rstrip("\'}]")
    errorMsg = errorMsg.lstrip(" \'")
    return errorMsg

# Streams the tweets of the user from his/her timeline.
def getTweetsOfScreenName(api, screen_name, page):
	alltweets = []
	try:
		new_tweets = api.user_timeline(screen_name = screen_name,count=200)
		alltweets.extend(new_tweets)
		outtweets = [[tweet.id_str, tweet.user.screen_name, tweet.created_at, tweet.text.encode("utf-8")] for tweet in alltweets]
		with open(os.path.join(os.getcwd()+'/CSV/%s_timeline_tweets_%s.csv' %(screen_name ,str(page))), 'wb') as f:
			writer = csv.writer(f)
			writer.writerow(["tweet_id", "screen_name", "created_at", "text"])
			writer.writerows(outtweets)
		pass
	except tweepy.TweepError as e:
		print e.api_code
		print getExceptionMessage(e.reason)

	return alltweets[(page-1)*10:(page-1)*10 + 10]

#Get all the tweets from the database of the search_string and their metadata. The results are paginated.
def getAllTweets(mongo, api, search_string, page):
	max_tweets = 500
	searched_tweets = []
	last_id = -1
	while len(searched_tweets) < max_tweets:
		count = max_tweets - len(searched_tweets)
		try:
			new_tweets = api.search(q=search_string, count=count, max_id=str(last_id - 1))
			searched_tweets.extend(new_tweets)
			last_id = new_tweets[-1].id
		except tweepy.TweepError as e:
			print e.api_code
			print getExceptionMessage(e.reason)

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
			tweet_entities_user_mentions_name = vals[u'name'].encode("utf-8")
			tweet_entities_user_mentions_screen_name = vals[u'screen_name'].encode("utf-8")
		tweet_user_location = tweet.user.location.encode("utf-8")
		tweet_place_country = ""
		tweet_place_name = ""
		if tweet.place is not None:
			tweet_place_country = tweet.place.country
			tweet_place_name = tweet.place.name
		
		tweets.insert({'tweet_id' : tweet_id, 'tweet_time' : tweet_time, 'tweet_screen_name' : tweet_screen_name,
						'tweet_text' : tweet_text, 'tweet_lang' : tweet_lang, 'tweet_user_followers_count' : tweet_user_followers_count,
						'tweet_user_friends_count' : tweet_user_friends_count, 'tweet_user_listed_count' : tweet_user_listed_count,
						'tweet_user_favourites_count' : tweet_user_favourites_count, 'tweet_retweet_count' : tweet_retweet_count,
						'tweet_in_reply_to_screen_name' : tweet_in_reply_to_screen_name, 'tweet_place_country' : tweet_place_country,
						'tweet_place_name' : tweet_place_name, 'tweet_user_location' : tweet_user_location,	'tweet_entities_hashtags' : tweet_entities_hashtags, 
						'tweet_entities_urls' : tweet_entities_urls, 'tweet_entities_user_mentions_name' : tweet_entities_user_mentions_name, 
						'tweet_entities_user_mentions_screen_name' : tweet_entities_user_mentions_screen_name})
		
		inside_output = {'tweet_id' : tweet_id, 'tweet_time' : tweet_time, 'tweet_screen_name' : tweet_screen_name,
						'tweet_text' : tweet_text, 'tweet_lang' : tweet_lang, 'tweet_user_followers_count' : tweet_user_followers_count,
						'tweet_user_friends_count' : tweet_user_friends_count, 'tweet_user_listed_count' : tweet_user_listed_count,
						'tweet_user_favourites_count' : tweet_user_favourites_count, 'tweet_retweet_count' : tweet_retweet_count,
						'tweet_in_reply_to_screen_name' : tweet_in_reply_to_screen_name, 'tweet_place_country' : tweet_place_country,
						'tweet_place_name' : tweet_place_name, 'tweet_user_location' : tweet_user_location,	'tweet_entities_hashtags' : tweet_entities_hashtags, 
						'tweet_entities_urls' : tweet_entities_urls, 'tweet_entities_user_mentions_name' : tweet_entities_user_mentions_name, 
						'tweet_entities_user_mentions_screen_name' : tweet_entities_user_mentions_screen_name}
		output.append(inside_output)

	outtweets = [[tweet['tweet_time'], str(tweet['tweet_text']), str(tweet['tweet_screen_name'])] for tweet in output[(page-1)*10:(page-1)*10 + 10]]
	with open(os.path.join(os.getcwd()+'/CSV/%s_search_tweets_%s.csv' %(search_string, str(page))), 'wb') as f:
		writer = csv.writer(f)
		writer.writerow(["created_at", "text", "screen_name"])
		writer.writerows(outtweets)
	pass
	return output[(page-1)*10:(page-1)*10 + 10]