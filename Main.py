import tweepy
import random
import time
from pynput import keyboard
import os
import urllib.request
import logging

#Reader be warned this code is spaghetti af

#Logging settings
logging.basicConfig(filename='bot_log.log',filemode='a',format='%(asctime)s - %(levelname)s - %(message)s',level=logging.INFO)

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

#Sets wormed.txt raw url from github and tries to download it
try:
    url = 'https://raw.githubusercontent.com/KarmaAlex/Twitter-worm-facts-bot/master/wormed.txt'
    urllib.request.urlretrieve(url,"wormed.txt")
    logging.info("Pulled wormed fle from github")
except:
    logging.error("Failed to request wormed file from github")
    exit()

worm_facts = []
#Try to import the worm facts file
try:
    #File is opened with encoding utf-8 because that's what twitter uses
    worm_facts_file = open("wormed.txt","r",encoding=('utf-8'))
except FileNotFoundError:
    logging.error("Failed opening wormed file from disk")
    exit()

#Reads all lines in the text document and copies them to empty list and closes file
for worm_fact in worm_facts_file.readlines():
    worm_facts.append(worm_fact)
worm_facts_file.close()
os.remove("wormed.txt")

#Declaration of various variables that are needed later
#For random generation, sets max index
i = len(worm_facts) - 1
#Defines times the bot should tweet
#If you want to change the times remember that for minutes below 10 the 0 is not included so 19:05 is actually 19:5
tweet_times = ["8:0","9:0","10:0","11:0","12:0","13:0","14:0","15:0","16:0","17:0","18:0","19:0","20:0","21:0","22:0","23:0","0:0"]
#For endless loop
stop = False

#Function that is used in the keyboard listener to interrupt execution and reload worm facts
def on_press(key):
    global stop
    global i
    #Quits program when pressing the End key
    if key == keyboard.Key.end:
        print("Quitting...")
        stop = True
        #Stops listener
        return False
    #Reloads worm facts from file when pressing the Ins key
    elif key == keyboard.Key.insert:
        print("Reloading worm facts...")
        try:
            urllib.request.urlretrieve(url,"wormed.txt")
            logging.info("Pulled wormed file from github")
        except:
            logging.error("Failed to request wormed file from github")
            exit()
        try:
            worm_facts_file = open("wormed.txt","r",encoding=('utf-8'))
        except FileNotFoundError:
            logging.error("Failed opening wormed file from disk")
            exit()
        worm_facts.clear()
        for worm_fact in worm_facts_file.readlines():
            worm_facts.append(worm_fact)
        i = len(worm_facts) - 1
        worm_facts_file.close()
        os.remove("wormed.txt")
        print("Printing worm facts:")
        for worm_fact in worm_facts:
            print(worm_fact)

#Initiates keyboard listener
with keyboard.Listener(on_press=on_press) as listener:
    #Starts infinite loop that ends on key press
    while stop == False:
        #Gets current time
        seconds = time.time()
        time_secs = time.localtime(seconds)
        #Copies time to a string value with the format hh:m/hh:mm
        curr_time = str(time_secs.tm_hour) + ":" + str(time_secs.tm_min)
        print("Controls:\nEnd Quit bot\nIns reload worm facts and print\n")
        print(curr_time + "\n")
        #If time is equal to tweet time it tweets
        if curr_time in tweet_times:
            #Keeps trying to tweet until it doesn't encounter the duplicate status error
            #This might cause the bot to exceed the max amounts of calls to the api, however this is unlikely
            try:
                #Generate random tweet
                api.update_status(worm_facts[random.randint(0,i)])
                logging.info("Tweeted")
                print("Tweeted")
                time.sleep(60)
            except tweepy.TweepError:
                logging.error("Status duplicate, trying different tweet")
        else:
            print("Time is not correct, didn't tweet")
            time.sleep(60)
            print("\n")
        #Clears screen for clarity's sake, should also work on non-windows machines
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')
    #Continues listening
    listener.join()