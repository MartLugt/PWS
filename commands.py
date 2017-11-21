#! /bin/python3
# get the intent and do something with it.
# You can also create modules with more complicated scripts and put them in a sepperate file. This will be more readable. 
# Good luck!
import datetime
import text_to_speech
import requests
from random import randint

dmood = {0: "I am very happy", 1: "I am fine", 2: "I am a bit tired", 3: "I have a headache", 4: "I am sick of your face", }

# for example:

# This intent says the current time.
def get_time():
    time = datetime.datetime.now().strftime('%H:%M')
    print(time)
    text_to_speech.play(text_to_speech.get_watson("It currently is " + time + "."))

"""def get_location():
    url = "https://www.googleapis.com/geolocation/v1/geolocate?key=AIzaSyDQTGEltrkBmtOOpkcF-kH9LRvCuq8MBhg"
    request = requests.post(url)
    
    text_to_speech.play(text_to_speech.get_watson("""

def get_mood():
    mood = randint(0, 4)
    text_to_speech.play(text_to_speech.get_watson(dmood[mood]))

intent = str(input()).lower()

if intent == "get_time":
    get_time()

