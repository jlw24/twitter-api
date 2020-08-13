import tweepy
from keys import consumer_key, consumer_secret, token

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

# Construct the API instance
api = tweepy.API(auth)

for tweet in tweepy.Cursor(api.search, q='productmanagement').items(10):
    print(tweet.text)
# # Iterate through all of the authenticated user's friends
# for friend in tweepy.Cursor(api.friends).items():
#     # Process the friend here
#     process_friend(friend)
#
# # Iterate through the first 200 statuses in the home timeline
# for status in tweepy.Cursor(api.home_timeline).items(200):
#     # Process the status here
#     process_status(status)