#!/usr/bin/env python3

import io
import wave
from urllib.parse import urlencode

import pyaudio
import requests

BUFFER_SIZE = 4096

text = "Hallo maat!"


def get_voicerss():
    key = "6dfbb0ac7bfc4571969d1fd6dfe7a6b0"
    # Two different ways of accomplishing the same goal
    url = "https://api.voicerss.org/?{}".format(urlencode({
        "key": key,
        "hl": "nl-nl",
        "src": text,
        "c": "WAV",
    }))
    return requests.post(url)


def get_watson():
    username = "a3a10d5d-ce68-410c-b066-f82c08242c60"
    password = "pnsxzzkxaVcj"
    url = "https://stream.watsonplatform.net/text-to-speech/api/v1/synthesize"

    # Two different ways of accomplishing the same goal
    params = (
        ('accept', 'audio/wav'),
        ('text', text),
        ('voice', 'en-US_AllisonVoice'),
    )

    request = requests.get(url, params=params, auth=(username, password))
    return request


# TODO: get new api key
def get_ispeak():
    key = "01d0b6f0dc6c29b45cbe884ec11a1923"
    url = "http://api.ispeech.org/api/rest"

    params = (
        ('action', 'convert'),
        ('text', text),
        ('key', key),
        ('format', 'wav'),
    )

    request = requests.get(url, params=params)
    return request


def play(request):
    file = io.BytesIO(request.content)  # When using str.encode(request.text), there is a lot of noise.
    w = wave.open(file, "r")

    pa = pyaudio.PyAudio()

    stream = pa.open(format=pa.get_format_from_width(w.getsampwidth()),
                     channels=w.getnchannels(),
                     rate=w.getframerate(),
                     output=True)

    data = w.readframes(BUFFER_SIZE)

    while data:
        stream.write(data)
        data = w.readframes(BUFFER_SIZE)

    stream.stop_stream()
    stream.close()

    pa.terminate()


rss_data = get_voicerss()
print("Playing voicerss:")
play(rss_data)

ibm_data = get_watson()
print("Playing ibm watson:")
play(ibm_data)

ispeak_data = get_ispeak()
print(ispeak_data.text)
print("Playing ispeak:")
play(ispeak_data)
