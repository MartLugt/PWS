#! /bin/python3
# get the intent and do something with it.
# You can also create modules with more complicated scripts and put them in a sepperate file. This will be more readable. 
# Good luck!
import datetime
import text_to_speech
import requests
from random import randint
from urllib.parse import urlencode

dmood = {0: "I am very happy", 1: "I am fine", 2: "I am a bit tired", 3: "I have a headache", 4: "I am sick of your face", }

def play(text, female=False):
    if female:
        text_to_speech.play(text_to_speech.get_watson(text, female=True))
    else:
        text_to_speech.play(text_to_speech.get_watson(text))

# for example:


# This intent says the current time.
def get_time(text):
    time = datetime.datetime.now().strftime('%H:%M')
    print(time)
    text_to_speech.play(text_to_speech.get_watson("It currently is " + time + "."))


def get_weather(text):
    r = requests.get("http://api.wunderground.com/api/49abb482ddb6b5b8/conditions/q/nl/waddinxveen.json")
    print(r.json())
    info = r.json()["current_observation"]

    temp = info["temp_c"]
    weather = info["weather"]
    play("The weather in Waddinxveen is %s with a temperature of %s." % (weather, temp))


def get_news(text):
    url = "https://newsapi.org/v2/top-headlines?{}".format(urlencode({
        "language": "en",
        "apiKey": "16ecf09edfc34e0eabc143c492d3438c"
    }))

    url += "&sources="

    if "tech" in text:
        url += "ars-technica"
    elif "sport" in text:
        url += "bbc-sport"
    elif "gaming" in text or "game" in text:
        url += "polygon"
    elif "business" in text or "econom" in text:
        url += "the-economist"
    elif "reddit" in text:
        url += "reddit-r-all"
    else:
        url += "bbc-news"

    print(url)

    r = requests.get(url)
    news = r.json()["articles"]

    # play("OK, here you go:")

    print(news)

    text = ""
    for article in news:
        if article["description"] is None:
            article["description"] = ""
        text += article["title"] + ". " + article["description"] + ".,. "
        print(text)

    play(text)


def get_mood(text):
    mood = randint(0, 4)
    text_to_speech.play(text_to_speech.get_watson(dmood[mood]))


def search(text):
    # First parse the text so only the search query remains.
    text.replace("search", "")
    if "for" in text:
        text.replace("for", "")


    url = "https://www.googleapis.com/customsearch/v1?parameters&{}".format(urlencode({
        "key": "AIzaSyDdsopTPMwh6kDCaSfBhctBzYiDm7VKjNs",
        "cx": "001287592891243700069:s6esochhcbm",
        "q": text,
    }))

    print(url)
    r = requests.get(url)
    result = r.json()
    print(result)

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
        get_time(text)
    elif intent == "get_weather":
        get_weather(text)
    elif intent == "get_mood":
        get_mood(text)
    elif intent == "search":
        search(text)
    elif intent == "get_news":
        get_news(text)


execute("get_news", "reddit ")

def guess():
    max = input("Maximum: ")

    answer = randint(0, int(max))

    turns = 1

    def game():
    	global turns
	    guess = int(input("Your guess: "))
	    if (guess < answer):
		    say("Guess higher!")
		    turns = turns + 1
		    game()
	    elif (guess > answer):
		    say("Guess lower!")
		    turns = turns + 1
		    game()
	    else:
		    say("Congratulations! You finished in " + str(turns) + " turns!")

    game()
