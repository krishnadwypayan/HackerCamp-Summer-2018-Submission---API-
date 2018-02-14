from googleplaces import GooglePlaces, types, lang
import re
import time
from main import mongo as mongo
import countries

# Google API Key
YOUR_API_KEY = 'AIzaSyBAaSHwdm7HgjEx855RGM6vszvWVm99t_o'
google_places = GooglePlaces(YOUR_API_KEY)

# Clean the html content from a string
def cleanhtml(raw_html):
	cleanr = re.compile('<.*?>')
	cleantext = re.sub(cleanr, '', raw_html)
	return cleantext

# Return the SEARCH_INDEX where each SEARCH_INDEX holds specific typeS.
def getSearchIndex(val):
	SEARCH_INDEX1 = [types.TYPE_MUSEUM, types.TYPE_AQUARIUM, types.TYPE_ZOO, types.TYPE_SYNAGOGUE]
	SEARCH_INDEX2 = [ types.TYPE_PARKING, types.TYPE_PARK, types.TYPE_MEAL_DELIVERY, types.TYPE_STADIUM]
	SEARCH_INDEX3 = [types.TYPE_MOSQUE, types.TYPE_HINDU_TEMPLE, types.TYPE_CHURCH]
	SEARCH_INDEX4 = [types.TYPE_CAFE, types.TYPE_BAR, types.TYPE_CASINO , types.TYPE_SHOPPING_MALL]
	SEARCH_INDEX5 = [types.TYPE_CITY_HALL, types.TYPE_LIBRARY, types.TYPE_LOCAL_GOVERNMENT_OFFICE]
	SEARCH_INDEX6 = [types.TYPE_TRAIN_STATION, types.TYPE_BUS_STATION]
	SEARCH_INDEX7 = [types.TYPE_HOSPITAL, types.TYPE_ATM, types.TYPE_PET_STORE]
	SEARCH_INDEX8 = [types.TYPE_POLICE]
	SEARCH_INDEX9 = [types.TYPE_ART_GALLERY, types.TYPE_MOVIE_THEATER, types.TYPE_BOOK_STORE]
	SEARCH_INDEX10 = [types.TYPE_DENTIST, types.TYPE_BEAUTY_SALON, types.TYPE_GAS_STATION]
	SEARCH_INDEX11 = [types.TYPE_BANK, types.TYPE_BAKERY, types.TYPE_ELECTRONICS_STORE]
	SEARCH_INDEX12 = [types.TYPE_SCHOOL, types.TYPE_STORE]
	SEARCH_INDEX13 =[types.TYPE_POST_OFFICE, types.TYPE_TAXI_STAND]

	mapper = {1: SEARCH_INDEX1, 2: SEARCH_INDEX2, 3: SEARCH_INDEX3, 4: SEARCH_INDEX4, 
	5: SEARCH_INDEX5, 6: SEARCH_INDEX6, 7: SEARCH_INDEX7, 8: SEARCH_INDEX8, 9: SEARCH_INDEX9, 
	10: SEARCH_INDEX10, 11: SEARCH_INDEX11, 12: SEARCH_INDEX12, 13: SEARCH_INDEX13,}

	return mapper[val]

# Returns a set containing the locations populated nearby the given search location
def populateNearbyLocations(location):
	output = set()
	for i in range(1, 14):
		print "Loading locations [", i, "/ 14 ]..."
		query_result = google_places.nearby_search(location=str(location), radius=500, types=getSearchIndex(i))
		for place in query_result.places:
			place.get_details()
			for p in cleanhtml(place.details['adr_address']).split(','):
				output.add(p)
			time.sleep(1.1)
	return output

# Returns the tweets in the radius of 500m of the specified location
def getTweets(place, page):
	locations = populateNearbyLocations(place)
	updated_locations = locations.copy()
	for locs in locations:
		for country in countries.countries:
			if country['name'] == locs.encode("utf-8").strip():
				print locs.encode("utf-8")
				updated_locations.remove(locs)
	tweets = mongo.db.tweets
	output = []
	for t in tweets:
		for loc in updated_locations:
			if re.search(loc, str(t['tweet_user_location'])):
				tweet_details = {'tweet_id' : tweet_id, 'tweet_time' : tweet_time, 'tweet_screen_name' : tweet_screen_name,
							'tweet_text' : tweet_text, 'tweet_lang' : tweet_lang, 'tweet_user_followers_count' : tweet_user_followers_count,
							'tweet_user_friends_count' : tweet_user_friends_count, 'tweet_user_listed_count' : tweet_user_listed_count,
							'tweet_user_favourites_count' : tweet_user_favourites_count, 'tweet_retweet_count' : tweet_retweet_count,
							'tweet_in_reply_to_screen_name' : tweet_in_reply_to_screen_name, 'tweet_place_country' : tweet_place_country,
							'tweet_place_name' : tweet_place_name, 'tweet_user_location' : tweet_user_location,	'tweet_entities_hashtags' : tweet_entities_hashtags, 
							'tweet_entities_urls' : tweet_entities_urls, 'tweet_entities_user_mentions_name' : tweet_entities_user_mentions_name, 
							'tweet_entities_user_mentions_screen_name' : tweet_entities_user_mentions_screen_name}
				output.append(tweet_details)

	outtweets = [[tweet['tweet_time'], tweet['tweet'].encode("utf-8"), tweet['screen_name'].encode("utf-8"), tweet['tweet_user_location']] for tweet in output[(page-1)*10:(page-1)*10 + 10]]
	with open(os.path.join(os.getcwd()+'/CSV/in_%s_radius_tweets_%s.csv' % place % str(page)), 'wb') as f:
		writer = csv.writer(f)
		writer.writerow(["created_at", "text", "screen_name", "location"])
		writer.writerows(outtweets)
	pass
	return output[(page-1)*10:(page-1)*10 + 10]