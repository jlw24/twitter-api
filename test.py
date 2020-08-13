from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import keys as k


# inherit from stream listener class

class StdOutListener(StreamListener):


    # take in data from StreamListener and
    def on_data(self, data):

        print(data)

        return True

    # if there's an error, print out error
    def on_error(self, status):
        print(status)


if __name__ == "__main__":
    listener = StdOutListener()
    auth = OAuthHandler(k.consumer_key, k.consumer_secret)
    auth.set_access_token(k.access_token, k.access_token_secret)

    stream = Stream(auth, listener)

    hashTagList = ['donald trump', 'barack obama']
    stream.filter(track=hashTagList)
    # fetchedTweetsFilename = "tweets.json"
    # twitter_streamer = TwitterStreamer()
    # twitter_streamer.stream_tweets(fetchedTweetsFilename)



