from main import *

# Filter the tweets according to the given expression evaluation.
def conditionFilter(mongo, expression, page):
	conditions = ['<', '>', '<=', '>=', '=', '!=']
	condition = ""
	pos = 0
	for c in conditions:
		pos = expression.find(c)
		if pos is not -1:
			condition = c
			break
	column_name = expression[0:pos]
	value = expression[pos+len(condition):]
	if condition == "=":
		condition = "=="
	tweets = mongo.db.tweets
	output = []
	column = '%s' %column_name
	for t in tweets.find():
		exp = [str(t[column]), condition, value]
		if eval(" ".join(exp)) == True:
			output_dict = dict()
			output_dict['tweet_time'] = t['tweet_time']
			output_dict['tweet'] = t['tweet_text']
			output_dict['screen_name'] = t['tweet_screen_name']
			output_dict[column_name] = t[column]
			output.append(output_dict)

	outtweets = [[tweet['tweet_time'], tweet['tweet'].encode("utf-8"), tweet['screen_name'].encode("utf-8"), tweet[column]] for tweet in output[(page-1)*10:(page-1)*10 + 10]]	
	with open(os.path.join(os.getcwd()+'/CSV/%s_filtered_tweets_%s.csv' %(column, str(page))), 'wb') as f:
		writer = csv.writer(f)
		writer.writerow(["created_at", "text", "screen_name", column_name])
		writer.writerows(outtweets)
	pass
	
	return output[(page-1)*10:(page-1)*10 + 10]

# Sort by tweets according to the date(ascending/descending)
def sortByDate(mongo, asc, page):
	tweets = mongo.db.tweets
	output = []
	for t in tweets.find().sort('tweet_time'):
		output.append({
				'tweet_time' : t['tweet_time'],
				'tweet' : t['tweet_text'],
				'screen_name' : t['tweet_screen_name']
			})

	desc_output = []
	if asc.lower() == "descending":
		for v in reversed(output):
			desc_output.append(v)
		output = desc_output

	outtweets = [[tweet['tweet_time'], tweet['tweet'].encode("utf-8"), tweet['screen_name'].encode("utf-8")] for tweet in output[(page-1)*10:(page-1)*10 + 10]]	
	with open(os.path.join(os.getcwd()+'/CSV/%s_order_sorted_tweets_%s.csv' %(asc, str(page))), 'wb') as f:
		writer = csv.writer(f)
		writer.writerow(["created_at", "text", "screen_name"])
		writer.writerows(outtweets)
	pass

	return output[(page-1)*10:(page-1)*10 + 10]

# Filter tweets to generate output containing only text, tweet_time and screen_name.
def getTweetsWithText(mongo, page):
	tweets = mongo.db.tweets
	output = []
	for t in tweets.find():
		output.append({
				'tweet_time' : t['tweet_time'],
				'tweet' : t['tweet_text'],
				'screen_name' : t['tweet_screen_name']
				})

	outtweets = [[tweet['tweet_time'], tweet['tweet'].encode("utf-8"), tweet['screen_name'].encode("utf-8")] for tweet in output[(page-1)*10:(page-1)*10 + 10]]
	with open(os.path.join(os.getcwd()+'/CSV/get_tweets_with_text_only_%s.csv' % str(page)), 'wb') as f:
		writer = csv.writer(f)
		writer.writerow(["created_at", "text", "screen_name"])
		writer.writerows(outtweets)
	pass
	return output[(page-1)*10:(page-1)*10 + 10]

# Search for the specific word appearing anywhere in the tweet details.
def regexMatchTweets(mongo, keyword, page):
	tweets = mongo.db.tweets
	output = []
	for t in tweets.find():
		if re.search(keyword, str(t)):
			output_dict = dict()
			output_dict['tweet_time'] = t['tweet_time']
			output_dict['tweet_text'] = t['tweet_text']
			output_dict['tweet_screen_name'] = t['tweet_screen_name']
			output.append(output_dict)
	
	outtweets = [[tweet['tweet_time'], tweet['tweet_text'].encode("utf-8"), tweet['tweet_screen_name'].encode("utf-8")] for tweet in output[(page-1)*10:(page-1)*10 + 10]]
	with open(os.path.join(os.getcwd()+'/CSV/%s_search_tweets_%s.csv' %(keyword, str(page))), 'wb') as f:
		writer = csv.writer(f)
		writer.writerow(["created_at", "text", "screen_name"])
		writer.writerows(outtweets)
	pass

	return output[(page-1)*10:(page-1)*10 + 10]

# Search for the text in the screen_name or the tweet_text.
def textSearchInTweetOrUsername(mongo, keyword, page):
	tweets = mongo.db.tweets
	output = []
	for t in tweets.find():
		text = t['tweet_text'].lower().encode("utf-8").split()
		screen_name = t['tweet_screen_name'].lower().encode("utf-8").split()
		if keyword in text or keyword in screen_name:
			output.append({
					'tweet_time' : t['tweet_time'],
					'tweet' : t['tweet_text'],
					'screen_name' : t['tweet_screen_name']
					})

	outtweets = [[tweet['tweet_time'], tweet['tweet'].encode("utf-8"), tweet['screen_name'].encode("utf-8")] for tweet in output[(page-1)*10:(page-1)*10 + 10]]
	with open(os.path.join(os.getcwd()+'/CSV/%s_matched_tweets_%s.csv' % (keyword, str(page))), 'wb') as f:
		writer = csv.writer(f)
		writer.writerow(["created_at", "text", "screen_name"])
		writer.writerows(outtweets)
	pass
	return output[(page-1)*10:(page-1)*10 + 10]

def filterTweetsByURLs(mongo, page):
	tweets = mongo.db.tweets
	output = []
	for t in tweets.find():
		if t['tweet_entities_urls'] is not "":
			output.append({
					'tweet_time' : t['tweet_time'],
					'tweet' : t['tweet_text'],
					'screen_name' : t['tweet_screen_name'],
					'url_mentions' : t['tweet_entities_urls']
				})
	outtweets = [[tweet['tweet_time'], tweet['tweet'].encode("utf-8"), tweet['screen_name'].encode("utf-8"), tweet['tweet_entities_urls']] for tweet in output[(page-1)*10:(page-1)*10 + 10]]
	with open(os.path.join(os.getcwd()+'/CSV/url_mentions_tweets_%s.csv' % str(page)), 'wb') as f:
		writer = csv.writer(f)
		writer.writerow(["created_at", "text", "screen_name"])
		writer.writerows(outtweets)
	pass
	return output[(page-1)*10:(page-1)*10 + 10]	