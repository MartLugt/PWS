import snowboydecoder as sb
import speech_to_text
import query_parser
import sys
import pyaudio
import time

model = "piet.pmdl"

def record():
    detector.terminate()

    frames = speech_to_text.record(rate = 44100, device_index = 1, num_channels = detector.get_channel())
    wav = speech_to_text.get_wav(frames, 44100)
    flac = speech_to_text.get_flac_linux(wav)
    print(speech_to_text.get_google(flac, 44100))


detector = sb.HotwordDetector(model, sensitivity=0.4)
print("Listening...")

detector.start(detected_callback=record, sleep_time=0.03)

detector.terminate()
