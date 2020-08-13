from tweepy.streaming import StreamListener
from tweepy import API
from tweepy import Cursor
from tweepy import OAuthHandler
from tweepy import Stream
import keys as k
import numpy as np
import pandas as pd

class TwitterClient():
    def __init__(self, twitter_user=None):
        self.auth = TwitterAuthenticator().authenticateTwitterApp()
        self.twitterClient = API(self.auth)
        self.twitterUser = twitter_user

    def getTwitterClientAPI(self):
        return self.twitterClient

    def getUserTimelineTweets(self, num_tweets):
        tweets = []
        for tweet in Cursor(self.twitterClient.user_timeline, id=self.twitterUser).items(num_tweets):
            tweets.append(tweet)

        return tweets

    def getFriendList(self, num_friends):
        friends = []
        for friend in Cursor(self.twitterClient.friends).items(num_friends):
            friends.append(friend)

        return friends

    def homeTimelineTweets(self, num_tweets):
        tweets = []
        for tweet in Cursor(self.twitterClient.home_timeline).items(num_tweets):
            tweets.append(tweet)

        return tweet

class TwitterAuthenticator():

    def authenticateTwitterApp(self):

        auth = OAuthHandler(k.consumer_key, k.consumer_secret)
        auth.set_access_token(k.access_token, k.access_token_secret)

        return auth


class TwitterStreamer():

    """
    Class for streaming and processing live tweets
    """
    def __init__(self):
        self.twitterAuthenticator = TwitterAuthenticator()

    def stream_tweets(self, fetchedTweetsFilename, hashTagList):

        # This handles twitter authentication and the connection to the twitter streaming API
        listener = TwitterListener(fetchedTweetsFilename)

        auth = self.twitterAuthenticator.authenticateTwitterApp()

        stream = Stream(auth, listener)

        stream.filter(track=hashTagList)

# inherit from stream listener class

class TwitterListener(StreamListener):

    """
    Basic listener class that prints received tweets to STDout
    """

    def __init__(self, fetchedTweetsFilename):
        self.fetchedTweetsFilename = fetchedTweetsFilename

    # take in data from StreamListener and
    def on_data(self, data):
        try:
            print(data)
            with open(self.fetchedTweetsFilename, 'a') as tf:
                tf.write(data)
        except BaseException as e:
            print("Error on data: %s" % str(e))
        return True

    # if there's an error, print out error
    def on_error(self, status):
        if status == 420:
            # Return False on data method in case rate limit occurs
            return False
        print(status)


class TweetAnalyzer():
    """
    Functionality for analyzing and categorizing tweets
    """

    def tweetsToDataframe(self, tweets):

        df = pd.DataFrame(data=[tweet.text for tweet in tweets], columns=['Tweets'])
        df['id'] = np.array([tweet.id for tweet in tweets])
        df['source'] = np.array([tweet.source for tweet in tweets])
        df['likes'] = np.array([tweet.favorite_count for tweet in tweets])
        df['retweets'] = np.array([tweet.retweet_count for tweet in tweets])

        return df



if __name__ == "__main__":

    twitter_client = TwitterClient()
    api = twitter_client.getTwitterClientAPI()
    tweet_analyzer = TweetAnalyzer()

    tweets = api.user_timeline(screen_name="elonmusk", count=20)

    df = tweet_analyzer.tweetsToDataframe(tweets)

    print(dir(tweets[0]))
    print(tweets[0].id)
    print(df.head(300).to_string())


    # hashTagList = ['andrew yang']
    # fetchedTweetsFilename = "tweets.txt"
    # # twitter_streamer = TwitterStreamer()
    # # twitter_streamer.stream_tweets(fetchedTweetsFilename, hashTagList)
    #
    # twitterClient = TwitterClient('pycon')
    # print(twitterClient.getUserTimelineTweets(2))



