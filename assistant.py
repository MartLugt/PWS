import snowboydecoder as sb
import text_to_speech
import speech_to_text
import query_parser
import commands
import sys
import pyaudio
import time

model = "piet.pmdl"
rate = 44100


def callback():
    detector.terminate()

    frames = speech_to_text.record(rate = rate, ding = True)
    wav = speech_to_text.get_wav(frames, rate)[0]
    flac = speech_to_text.get_flac_linux(wav)
    text = speech_to_text.get_google(flac, rate)

    intent = query_parser.parse(text)

    commands.execute(intent)


detector = sb.HotwordDetector(model, sensitivity=0.7)
print("Listening...")

detector.start(detected_callback=callback, sleep_time=0.03)

detector.terminate()
