import snowboydecoder as sb
import text_to_speech
import speech_to_text
import query_parser
import commands
import sys
import pyaudio
import time
import json
import random

model = "Jarvis.pmdl"
rate = 44100

with open('conversation.json', 'r') as f:
    conversation = json.load(f)["nice"]
    print(conversation)


def main():
    frames = speech_to_text.record(rate=rate, ding=True)
    wav = speech_to_text.get_wav(frames, rate)[0]
    flac = speech_to_text.get_flac_linux(wav)
    text = speech_to_text.get_google(flac, rate)

    print(text)

    if not text:
        commands.play(random.choice(conversation["dont_understand"]))
        main()

    intent = query_parser.parse(text.lower())
    print(intent)

    commands.execute(intent, text)


def callback():
    detector.terminate()

    main()


def detect():
    global detector
    detector = sb.HotwordDetector(model, sensitivity=0.7)
    print("Listening...")

    detector.start(detected_callback=callback, sleep_time=0.03)


while True:
    detect()

