import snowboydecoder as sb
import text_to_speech
import speech_to_text
import query_parser
import commands
import sys
import pyaudio
import time

model = "Jarvis.pmdl"
rate = 44100

def main():
    frames = speech_to_text.record(rate=rate, ding=True)
    wav = speech_to_text.get_wav(frames, rate)[0]
    flac = speech_to_text.get_flac_linux(wav)
    text = speech_to_text.get_google(flac, rate)

    if not text:
        commands.play("ur mom gay")
        callback()

    intent = query_parser.parse(text)
    print(intent)

    commands.execute(intent, text)


def callback():
    detector.terminate()

    main()


detector = sb.HotwordDetector(model, sensitivity=0.7)
print("Listening...")

detector.start(detected_callback=callback, sleep_time=0.03)

detector.terminate()
