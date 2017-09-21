#!/usr/bin/env python3

# NOTE: this example requires PyAudio because it uses the Microphone class

import speech_recognition as sr
from pprint import pprint

# obtain audio from the microphone
r = sr.Recognizer()
with sr.Microphone() as source:
    r.adjust_for_ambient_noise(source)
    print("Say something!")
    audio = r.listen(source, timeout=3, phrase_time_limit=6)

# recognize speech using Sphinx
try:
    print("Sphinx thinks you said " + r.recognize_sphinx(audio))
except sr.UnknownValueError:
    print("Sphinx could not understand audio")
except sr.RequestError as e:
    print("Sphinx error; {0}".format(e))

# recognize speech using Google Speech Recognition
try:
    # for testing purposes, we're just using the default API key
    # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY", show_all=True)`
    # instead of `r.recognize_google(audio, show_all=True)`
    print("Google Speech Recognition results:")
    pprint(r.recognize_google(audio, show_all=True))  # pretty-print the recognition result
except sr.UnknownValueError:
    print("Google Speech Recognition could not understand audio")
except sr.RequestError as e:
    print("Could not request results from Google Speech Recognition service; {0}".format(e))

# recognize speech using Google Cloud Speech
# GOOGLE_CLOUD_SPEECH_CREDENTIALS = r"""INSERT THE CONTENTS OF THE GOOGLE CLOUD SPEECH JSON CREDENTIALS FILE HERE"""
# try:
#     print("Google Cloud Speech recognition results:")
#     pprint(r.recognize_google_cloud(audio, credentials_json=GOOGLE_CLOUD_SPEECH_CREDENTIALS, show_all=True))  # pretty-print the recognition result
# except sr.UnknownValueError:
#     print("Google Cloud Speech could not understand audio")
# except sr.RequestError as e:
#     print("Could not request results from Google Cloud Speech service; {0}".format(e))

# recognize speech using Wit.ai
WIT_AI_KEY = "EZ7V7OXWF7TURDDTFCYAM2DWLBX2OAIT"  # Wit.ai keys are 32-character uppercase alphanumeric strings
try:
    print("Wit.ai recognition results:")
    pprint(r.recognize_wit(audio, key=WIT_AI_KEY, show_all=True))  # pretty-print the recognition result
except sr.UnknownValueError:
    print("Wit.ai could not understand audio")
except sr.RequestError as e:
    print("Could not request results from Wit.ai service; {0}".format(e))

WIT_AI_KEY_DUTCH = "57UW2OZP2T3YMJTQK7CHRBCQM5QGWPNJ"
try:
    print("Wit.ai dutch recognition results:")
    pprint(r.recognize_wit(audio, key=WIT_AI_KEY_DUTCH, show_all=True))  # pretty-print the recognition result
except sr.UnknownValueError:
    print("Wit.ai dutch couldnt understand")
except sr.RequestError as e:
    print("Could not request results; {0}".format(e))

# recognize speech using Houndify
HOUNDIFY_CLIENT_ID = "dZMG53QYNQ9Y7ZXr34r2pQ=="  # Houndify client IDs are Base64-encoded strings
HOUNDIFY_CLIENT_KEY = "WF9IOtIQKc5pDN2mvfcMUGVNQgxxvTUNsmMf9Qhrdc0bJr-RYVkaZvLgOdRl8eDTccQwpkeYcStJFQHf5Vc_cw=="  # Houndify client keys are Base64-encoded strings
try:
    print("Houndify recognition results:")
    pprint(r.recognize_houndify(audio, client_id=HOUNDIFY_CLIENT_ID, client_key=HOUNDIFY_CLIENT_KEY, show_all=True))
except sr.UnknownValueError:
    print("Houndify could not understand audio")
except sr.RequestError as e:
    print("Could not request results from Houndify service; {0}".format(e))
    print("Could not request results from IBM Speech to Text service; {0}".format(e))