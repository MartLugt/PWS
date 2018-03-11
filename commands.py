#! /bin/python3
# get the intent and do something with it.
# You can also create modules with more complicated scripts and put them in a seperate file. This will be more readable.
# Good luck!
import sys
import datetime
import text_to_speech
import time
import speech_to_text as stt
import requests
import random
import pyaudio
from io import BytesIO
import wave
import json
import icalendar
from pytz import timezone
from urllib.parse import urlencode

with open('conversation.json', 'r') as f:
    conversation = json.load(f)["nice"]


def init(user):
    file_name = user + "_data.json"
    with open(file_name, 'r') as f:
        global user_data
        user_data = json.load(f)

    with open("text.json", 'r') as f:
        global conversation
        conversation = json.load(f)


def change_voice(text):
    global female
    play(random.choice(conversation['change_voice']))
    text = record()
    if text.lower() == "yes":
        if female:
            female = False
        else:
            female = True
        play("Okay")


def play(text, female=False):
    text_to_speech.play(text_to_speech.get_watson(text, female))


def record(text=True, ding=True, full=False, check=True):
    if text:
        frames = stt.record(ding=ding, stop_s=0.5)
        w = stt.get_wav(frames)[0]
        f = stt.get_flac_linux(w)
        ttext = stt.get_google(f, 44100, full=full)
        print(ttext)
        if check:
            if not ttext:
                play(random.choice(conversation["dont_understand"]))
                time.sleep(2.5)
                record(ding, full)
        return ttext
    else:
        frames = stt.record(ding=ding)
        print(stt.get_wav(frames))
        return json.dumps(stt.get_wav(frames)[1].decode("utf-8"))


# this command shuts down the system, giving the user a message beforehand.
def stop(text):
    play(random.choice(conversation['shutdown']))
    sys.exit(0)


# This intent says the current time.
def get_time(text):
    time = datetime.datetime.now().strftime('%H:%M')
    print(time)
    text_to_speech.play(text_to_speech.get_watson("It currently is " + time + "."))


def get_weather(text):
    r = requests.get("http://api.wunderground.com/api/49abb482ddb6b5b8/conditions/q/nl/gouda.json")
    print(r.json())
    info = r.json()["current_observation"]

    temp = info["temp_c"]
    weather = info["weather"]
    play("The weather in Gouda is %s with a temperature of %s." % (weather, temp))


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

    play(random.choice(conversation["ok"]))

    print(news)

    if len(news) > 3:
        news = news[:3]

    text = ""
    for article in news:
        if article["description"] is None:
            article["description"] = ""
        text += article["title"] + ". " + article["description"] + ". "
        print(text)

    play(text, True)


def get_mood(text):
    play(random.choice(conversation["moods"]))
    print("Mood has been executed")


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


def calendar(text):
    url = "https://calendar.google.com/calendar/ical/martvanderlugt%40hetnet.nl/" \
          "private-be9edc91db33c2af45984c4d72bb96fe/basic.ics"

    cal = requests.get(url).content
    gcal = icalendar.Calendar.from_ical(cal)

    events = []

    for component in gcal.walk():
        if component.name == "VEVENT":
            start = component.get("dtstart").dt
            end = component.get("dtend").dt

            if type(start) is datetime.date:
                start = datetime.datetime.combine(start, datetime.time())
            if type(end) is datetime.date:
                end = datetime.datetime.combine(end, datetime.time())

            start = timezone("Europe/Amsterdam").localize(start)
            # start = start.astimezone(timezone("Europe/Amsterdam"))
            end = timezone("Europe/Amsterdam").localize(end)
            # end = end.astimezone(timezone("Europe/Amsterdam"))

            event = {"summary": component.get("summary"),
                     "location": component.get("location"),
                     "start": start,
                     "end": end}

            print(event["summary"])

            events.append(event)

    events = sorted(events, key=lambda k: k["start"])
    print(events)

    upcomming_events = []

    for ev in events:
        if ev["start"] >= datetime.datetime.now(tz=timezone("Europe/Amsterdam")):
            upcomming_events.append(ev)
            print(ev["start"], "True")
        else:
            print(ev["start"], "False")

    text = ""

    for ev in upcomming_events:
        if ev["start"].strftime("%H:%M") == "00:00":
            time = ev["start"].strftime("On %e %B")
        else:
            time = ev["start"].strftime("On %e %B, at %H:%M")

        text += "%s, you have %s" % (time, ev["summary"])

        if ev["location"] != "":
            text += " at %s. " % ev["location"]
        else:
            text += ". "

    play(text)


def get_num(text):
    while True:
        res_full = record(full=True, check=False)
        if res_full is not None or res_full is not []:
            for res in res_full["alternative"]:
                try:
                    return int(res["transcript"])
                except ValueError:
                    continue
        print(text)
        play(text)
        time.sleep(1)


# this is a game of guess the number
def number_guess(text):
    play(conversation["set_max_number"])  # the user has to give a maximum
    time.sleep(1)
    maximum = get_num(conversation["no_number"])

    answer = random.randint(1, maximum)  # a random number between 0 and max is picked
    play("Guess a number between one and " + str(maximum))
    time.sleep(1)

    def game(turns):
        guess = get_num(conversation["no_number_guess"])
        if int(guess) < int(answer):  # when guessed too low
            play("Guess higher")
            time.sleep(1)
            turns = turns + 1
            game(turns)
        elif int(guess) > int(answer):  # when guessed too high
            play("Guess lower")
            time.sleep(1)
            turns = turns + 1
            game(turns)
        else:
            if turns == 1:
                play("Congratulations! You finished in " + str(turns) + " turn")
            else:
                play("Congratulations! You finished in " + str(turns) + " turns")

    game(1)


# this command will repeat what the user said
def echo(text):
    text = text.lower().replace("echo", " ")
    play(text)


def snowboy(text):
    token = "fe0506fb0b11122ed1e16582ea0ae4f18a438196"
    play(conversation["what_name"])
    name = record()
    print(name)
    play("Ok! The name is %s. Now please say this name after each beep." % name)

    wav1 = record(text=False)
    wav2 = record(text=False)
    wav3 = record(text=False)

    url = "https://snowboy.kitt.ai/api/v1/train/"

    data = {
        "name": name,
        "language": "en",
        "microphone": "None",
        "token": token,
        "voice_samples": [
            {"wave": wav1},
            {"wave": wav2},
            {"wave": wav3}
        ]
    }

    print(data)

    response = requests.post(url, json=data)

    with open((name + ".pmdl"), "w") as outfile:
        outfile.write(response.content)


def joke(text):
    r = random.randint(0, 5)
    j = open('jokes.txt')
    lines = j.readlines()
    # a random joke with two lines will get picked
    if r == 0:
        play(lines[0])
        time.sleep(2.0)
        play(lines[1])
    elif r == 1:
        play(lines[2])
        time.sleep(2.0)
        play(lines[3])
    elif r == 2:
        play(lines[4])
        time.sleep(2.0)
        play(lines[5])
    elif r == 3:
        play(lines[6])
        time.sleep(2.0)
        play(lines[7])
    elif r == 4:
        play(lines[8])
        time.sleep(2.0)
        play(lines[9])
    elif r == 5:
        play(lines[10])
        time.sleep(2.0)
        play(lines[11])


def make_note(text):
    text = text.replace("make", "")
    text = text.replace("note", "")
    notes = open("notes.txt", "w")
    play("Noted %s" %text)
    notes.write(text)
    notes.close()


def get_notes(text):
    notes = open('notes.txt', 'r')
    play(random.choice(conversation['notes']))
    note = notes.read()
    play(note)
    notes.close()


def execute(intent, text=None):
    # this function is needed to execute the right command
    intent = intent[0]
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
    elif intent == "get_cal":
        calendar(text)
    elif intent == "guess":
        number_guess(text)
    elif intent == "joke":
        joke(text)
    elif intent == "get_note":
        get_notes(text)
    elif intent == "make_note":
        make_note(text)
    elif intent == "change_voice":
        change_voice(text)
    elif intent == "echo":
        echo(text)
    elif intent == "stop":
        stop(text)
    elif intent == "twentyone":
        twentyone(text)
