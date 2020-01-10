import tweepy
import random
import time
from pynput import keyboard

#Twitter auth
#Consumer API and API secret key
auth = tweepy.OAuthHandler("QLntDiZAtB7CjuFEs4tc1DBbS","vradE4DrnojcheXptysnPIarF5TVP5S9t8jKqrjtv3DZ8t7qG6")
#Access token and access token secret
auth.set_access_token("1215687993220042752-4Fsnxjz3ACVE7DYq2VEkNh8OBOPSU2","iWvcU54RUpFhR82ZC8Htni44SZoe8mhKxoFXxmVQ9b2F6")
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

#Attemp login
try:
    api.verify_credentials()
    print("Authentication successful")
except:
    print("Error authenticating")
    exit()


worm_facts = []
#Try to import the worm facts file
try:
    worm_facts_file = open("wormed.txt","r")
except FileNotFoundError:
    print("Could not find file")
    exit()

#Reads all lines in the text document and copies them to empty list
for worm_fact in worm_facts_file.readlines():
    worm_facts.append(worm_fact)

#Declaration of various variables that are needed later
i = len(worm_facts) - 1
tweet_time_h = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,0]
tweet_time_m = 0
stop = False

#I don't know what this does but it interrupts the script upon pressing the End key
def on_press(key):
    global stop
    if key == keyboard.Key.end:
        print("End pressed")
        stop = True
        #Stops listener
        return False

#Initiates keyboard listener
with keyboard.Listener(on_press=on_press) as listener:
    #Starts infinite loop that ends on key press
    while stop == False:
        print("Running")
        #Gets current time
        seconds = time.time()
        curr_time = time.localtime(seconds)
        #If time is equal to tweet time it tweets
        if curr_time.tm_hour in tweet_time_h and curr_time.tm_min == tweet_time_m:
            #Random fact generation
            api.update_status(worm_facts[random.randint(0,i)])
            print("Tweeted")
        else:
            print("Time is not correct, didn't tweet")
        #Waits 60 seconds, hopefully won't tweet twice in one minute
        time.sleep(60)
    #Continues listening
    listener.join()

worm_facts_file.close()
exit()