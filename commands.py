#! /bin/python3
# get the intent and do something with it.
# You can also create modules with more complicated scripts and put them in a sepperate file. This will be more readable. 
# Good luck!
import datetime
import text_to_speech

# for example:

# This intent says the current time.
def get_time():
    time = datetime.datetime.now().strftime('%H:%M')
    print(time)
    text_to_speech.play(text_to_speech.get_watson("It currently is " + time + "."))

intent = str(input()).lower()

if intent == "get_time":
    get_time()
