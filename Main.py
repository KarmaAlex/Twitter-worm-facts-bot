import tweepy
import random
import time
import os
import urllib.request
from urllib.parse import urlparse
import logging
import json
import requests

#THIS BOT NOW RUNS ON A HEROKU SCHEDULER, THE TIMES OF THE TWEETS ARE DIFFERENT

#Logging settings
logging.basicConfig(filename='bot_log.log',filemode='a',format='%(asctime)s - %(levelname)s - %(message)s',level=logging.INFO)
#The bot creates a bot_log.log file where it logs tweets, reloads of files and eventual errors, the log includes a time stamp

#Read the env variables to set the twitter api login info
consumer_key = os.getenv("CONSUMER_KEY")
consumer_secret = os.getenv("CONSUMER_SECRET")
access_token = os.getenv("ACCESS_TOKEN")
access_token_secret = os.getenv("ACCESS_TOKEN_SECRET")

#Twitter auth info
auth = tweepy.OAuthHandler(consumer_key,consumer_secret)
auth.set_access_token(access_token,access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

#Attemp login to twitter api
try:
    api.verify_credentials()
    logging.info("Authenticated to twitter API successfully")
except:
    logging.error("Failed to authenticate to twitter API")
    exit()


#Sets wormed.txt raw url from github and tries to download it
try:
    url = 'https://raw.githubusercontent.com/KarmaAlex/Twitter-worm-facts-bot/master/worm%20facts.json'
    urllib.request.urlretrieve(url,"worm facts.json")
    logging.info("Pulled wormed fle from github")
except:
    logging.error("Failed to request wormed file from github")
    exit()

#Try to import the worm facts file
try:
    #Open in utf-8 encoding so that things like emojis work
    with open("worm facts.json", "r", encoding="utf-8") as worm_facts_file:
        worm_facts = json.load(worm_facts_file)
except FileNotFoundError:
    logging.error("Failed opening wormed file from disk")
    exit()
os.remove("worm facts.json")

#Declaration of various variables that are needed later
#For random generation, sets max index
i = len(worm_facts) - 1
#For endless loop
stop = False
#Empty list for last 20 tweets
last_tweets = []
#Number of hours it should wait until tweeting again
tweet_delay = 6

#Function for text only tweets
def txt_tweet(text):
    api.update_status(text)
    logging.info("Tweeted")

#Function for tweets that include media
def media_tweet(url, text):
    filename = os.path.basename(urlparse(url).path)
    with os.open("media/"+filename,"wb") as file:
        response = requests.get(url, stream=True)
        if not response.ok:
            print (response)
        for block in response.iter_content(1024):
            if not block:
                break
        file.write(block)
    if text != None:
        api.update_with_media(file,status=text)
    else:
        api.update_with_media(file)
    os.remove(file)

while stop == False:
    #Gets current time
    seconds = time.time()
    time_secs = time.localtime(seconds)
    #Gets last tweets by authenticated user
    last_tweets = api.user_timeline()
    tweet = last_tweets[0]
    #print("Controls:\nEnd Quit bot\nIns reload worm facts and print\n")
    #print(curr_time + "\n")
    #If time since last tweet is 6 hours or longer it tries to tweet
    print(time_secs.tm_hour)
    print(tweet.created_at.hour)
    if ((time_secs.tm_hour - tweet.created_at.hour) >= tweet_delay) or ((time_secs.tm_hour - tweet.created_at.hour) <= -tweet_delay):
        #Keeps trying to tweet until it doesn't encounter the duplicate status error
        #This might cause the bot to exceed the max amounts of calls to the api, however this is unlikely
        try:
            #Generate random tweet
            fact = worm_facts[random.randint(0,len(worm_facts)-1)]
            #Calls the appropriate function based on wether the tweet contains media or not
            if fact["type"] == "text":
                txt_tweet(fact["text"])
            else:
                media_tweet(fact["file"],fact["text"])
            logging.info("Tweeted")
            print("Tweeted")
            stop = True
        except tweepy.TweepError:
            logging.error("Status duplicate, trying different tweet")
    else:
        print("It has not been "+ str(tweet_delay) + " or more hours since last tweet")
        stop = True
print("Quitting...")
