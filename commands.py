#! /bin/python3
# get the intent and do something with it.
# You can also create modules with more complicated scripts and put them in a sepperate file. This will be more readable. 
# Good luck!
import datetime
import text_to_speech
import requests
from random import randint

dmood = {0: "I am very happy", 1: "I am fine", 2: "I am a bit tired", 3: "I have a headache", 4: "I am sick of your face", }

def play(text):
    text_to_speech.play(text_to_speech.get_watson(text))

# for example:

# This intent says the current time.
def get_time():
    time = datetime.datetime.now().strftime('%H:%M')
    print(time)
    text_to_speech.play(text_to_speech.get_watson("It currently is " + time + "."))

def get_weather():
    r = requests.get("http://api.wunderground.com/api/49abb482ddb6b5b8/conditions/q/nl/waddinxveen.json")

    info = r.json()["current_observation"]

    temp = info["temp_c"]
    weather = info["weather"]
    play("The weather in Waddinxveen is %s with a temperature of %s." % (weather, temp_c))

def get_mood():
    mood = randint(0, 4)
    text_to_speech.play(text_to_speech.get_watson(dmood[mood]))

def exec(intent):

    if intent == "get_time":
        get_time()
    elif intent == "get_weather":
        get_weather()
    elif intent == "get_mood":
        get_mood()

