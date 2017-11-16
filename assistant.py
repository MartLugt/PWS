import snowboydecoder as sb
import text_to_speech
import speech_to_text
import query_parser
import sys
import pyaudio
import time

model = "piet.pmdl"
rate = 44100

def callback():
    detector.terminate()

    frames = speech_to_text.record(rate = rate, device_index = 1, num_channels = detector.get_channel(), ding = True)
    wav = speech_to_text.get_wav(frames, rate)
    flac = speech_to_text.get_flac_linux(wav)
    text = speech_to_text.get_google(flac, rate)

    sound = text_to_speech.get_watson(text)
    text_to_speech.play(sound)

detector = sb.HotwordDetector(model, sensitivity=0.4)
print("Listening...")

detector.start(detected_callback=callback, sleep_time=0.03)

detector.terminate()
