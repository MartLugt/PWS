#! /bin/python3
# get the intent and do something with it.
# You can also create modules with more complicated scripts and put them in a sepperate file. This will be more readable. 
# Good luck!
import datetime
import text_to_speech
import requests
from random import randint
from urllib.parse import urlencode
import json

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
    play("The weather in Waddinxveen is %s with a temperature of %s." % (weather, temp))


def get_mood():
    mood = randint(0, 4)
    text_to_speech.play(text_to_speech.get_watson(dmood[mood]))


def search(text):
    # First parse the text so only the search query remains.
    text.replace("search for", "")
    text.replace("search", "")

    url = "https://www.googleapis.com/customsearch/v1?parameters&{}".format(urlencode({
        "key": "AIzaSyDdsopTPMwh6kDCaSfBhctBzYiDm7VKjNs",
        "cx": "001287592891243700069:s6esochhcbm",
        "q": text,
    }))

    print(url)
    r = requests.get(url)
    result = json.loads(r.content)

    items = result["items"]

    title = items[0]["title"]

    # If the result is from wikipedia read the snippet
    if "wikipedia" in title.lower():
        snippet = items[0]["snippet"]
        print(snippet)
        # Parse snippet so that it stops after the first sentence.
        snippet = snippet.split(". ")

        play("According to Wikipedia, %s." % snippet[0])
    else:
        play("The top result is %s." % title)


def execute(intent, text = None):
    if intent == "get_time":
        get_time()
    elif intent == "get_weather":
        get_weather()
    elif intent == "get_mood":
        get_mood()
    elif intent == "search":
        search(text)


execute("search", "Search you are gay")
