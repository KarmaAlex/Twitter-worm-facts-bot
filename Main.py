import tweepy
import random
import time
from pynput import keyboard
import os
import urllib.request

#Reader be warned this code is spaghetti af

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
    print("Authentication successful\n")
except:
    print("Error authenticating")

#Sets wormed.txt raw url from github and downloads it
url = 'https://raw.githubusercontent.com/KarmaAlex/Twitter-worm-facts-bot/master/wormed.txt'
urllib.request.urlretrieve(url,"wormed.txt")

worm_facts = []
#Try to import the worm facts file
try:
    #File is opened with encoding utf-8 because that's what twitter uses
    worm_facts_file = open("wormed.txt","r",encoding=('utf-8'))
except FileNotFoundError:
    print("Could not find file")
    exit()

#Reads all lines in the text document and copies them to empty list and closes file
for worm_fact in worm_facts_file.readlines():
    worm_facts.append(worm_fact)
worm_facts_file.close()
os.remove("wormed.txt")

#Declaration of various variables that are needed later
#For random generation, sets max index
i = len(worm_facts) - 1
#Defines time the bot should tweet
tweet_time_h = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,0]
tweet_time_m = 0
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
        urllib.request.urlretrieve(url,"wormed.txt")
        try:
            worm_facts_file = open("wormed.txt","r",encoding=('utf-8'))
        except FileNotFoundError:
            print("Could not find file")
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
        curr_time = time.localtime(seconds)
        print("Controls:\nEnd Quit bot\nIns reload worm facts and print\n")
        print(str(curr_time.tm_hour) + ":" + str(curr_time.tm_min) + "\n")
        #If time is equal to tweet time it tweets
        if curr_time.tm_hour in tweet_time_h and curr_time.tm_min == tweet_time_m:
            #Keeps trying to tweet until it doesn't encounter the duplicate status error
            #This might cause the bot to exceed the max amounts of calls to the api, however this is unlikely
            try:
                #Generate random tweet
                api.update_status(worm_facts[random.randint(0,i)])
                print("Tweeted")
                time.sleep(60)
            except tweepy.TweepError:
                print("Status Duplicate, trying again")
        else:
            print("Time is not correct, didn't tweet")
            time.sleep(60)
            print("\n")

    #Continues listening
    listener.join()