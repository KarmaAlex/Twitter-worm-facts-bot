import tweepy
import random
import time
from pynput import keyboard
from os import system, sys, getcwd
import requests

#Reader be warned this code is spaghetti af

#Twitter auth
#Consumer API and API secret key
auth = tweepy.OAuthHandler("QLntDiZAtB7CjuFEs4tc1DBbS","vradE4DrnojcheXptysnPIarF5TVP5S9t8jKqrjtv3DZ8t7qG6")
#Access token and access token secret
auth.set_access_token("1215687993220042752-4Fsnxjz3ACVE7DYq2VEkNh8OBOPSU2","iWvcU54RUpFhR82ZC8Htni44SZoe8mhKxoFXxmVQ9b2F6")
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

#Attemp login to twitter api
try:
    api.verify_credentials()
    print("Authentication successful\n")
except:
    print("Error authenticating")

worm_facts = []
#Try to import the worm facts file
try:
    worm_facts_file = open("wormed.txt","r")
except FileNotFoundError:
    print("Could not find file")

#Reads all lines in the text document and copies them to empty list and closes file
for worm_fact in worm_facts_file.readlines():
    worm_facts.append(worm_fact)
worm_facts_file.close()

#Declaration of various variables that are needed later
#For random generation, sets max index
i = len(worm_facts) - 1
#Defines time the bot should tweet
tweet_time_h = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,0]
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
        try:
            worm_facts_file = open("wormed.txt","r")
        except FileNotFoundError:
            print("Could not find file")
        worm_facts.clear()
        for worm_fact in worm_facts_file.readlines():
            worm_facts.append(worm_fact)
        i = len(worm_facts) - 1
        worm_facts_file.close()
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
            #This might cause the bot to exceed the max amounts of calls to the api, in that case fuck this bot
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