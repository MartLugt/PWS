#!/usr/bin/env python3

import audioop  # audioOperations for checking volume of sound
import io
import os
import subprocess
import wave  # wave for creating .wav file
from urllib.parse import urlencode

import pyaudio  # pyaudio for recording
import requests

# TODO: change all mixedCase variable names to lower_case

#Set constants
FORMAT = pyaudio.paInt16
RATE = 44100
BUFFER_SIZE = 1024
START_COOLDOWN = 9
STOP_COOLDOWN = 21


def get_wav(frames, format, rate):
    with io.BytesIO() as file:
        wa = wave.open(file, 'w')
        wa.setnchannels(1)
        wa.setsampwidth(2)
        wa.setframerate(rate)
        wa.writeframes(b''.join(frames))
        wavValue = file.getvalue()
        wa.close()
    return wavValue


def get_flac(wav_data):
    base_path = "C:\\Users\martv\AppData\Local\Programs\Python\Python35\Lib\site-packages\speech_recognition\\"
    flac_converter = os.path.join(base_path,
                                  "flac-win32.exe")  # FOR WINDOWS. WHEN PORTING TO PI, CHANGE THE WHOLE WAV TO FLAC CONVERSION
    process = subprocess.Popen([
        flac_converter,
        "--stdout", "--totally-silent",
        # put the resulting FLAC file in stdout, and make sure it's not mixed with any program output
        "--best",  # highest level of compression available
        "-",  # the input FLAC file contents will be given in stdin
    ], stdin=subprocess.PIPE, stdout=subprocess.PIPE, startupinfo=None)
    flac_data, stderr = process.communicate(wav_data)
    return flac_data


def get_google(flac_data, rate, language="en-US"):
    url = "http://www.google.com/speech-api/v2/recognize?{}".format(urlencode({
        "client": "chromium",
        "lang": language,
        "key": "AIzaSyBOti4mM-6x9WDnZIjIeyEU21OpBXqWBgw",
    }))

    headers = {"Content-Type": "audio/x-flac; rate={}".format(rate)}
    r = requests.post(url, headers=headers, data=flac_data)
    return r.text


def get_wit(wav_data, language="en-US"):
    url = "https://api.wit.ai/speech"
    if language == "en-US":
        key = "EZ7V7OXWF7TURDDTFCYAM2DWLBX2OAIT"
    elif language == "nl-NL":
        key = "57UW2OZP2T3YMJTQK7CHRBCQM5QGWPNJ"
    else:
        key = None
    headers = {"Authorization": "Bearer " + key, 'accept': 'application/vnd.wit.' + str(5102017) + '+json',
               "Content-Type": "audio/wav"}
    r = requests.post(url, data=wav_data, headers=headers)
    return r.text

#First create the PyAudio object
pa = pyaudio.PyAudio()

#Create a stream for recording
stream = pa.open(format = FORMAT,
                 channels = 1,
                 rate = RATE,
                 input = True,
                 frames_per_buffer = BUFFER_SIZE)

print("First be silent, calibrating silence")
buffer = stream.read(int(RATE / 2)) #half a second
threshold = audioop.rms(buffer, pa.get_sample_size(FORMAT)) + 200

print("We are now recording. Start talking for it to start.")

frames = []
counterThreshold = 0    #TODO: give this a better name
counterThreshold1 = 0   #TODO: give this a better name too

#If sound has been above threshold for n buffers, continue up the loop

while True:     #TODO: make this less fast. Give a cooldown
    buffer = stream.read(BUFFER_SIZE)
    level = audioop.rms(buffer, pa.get_sample_size(FORMAT))
    if level > threshold:
        counterThreshold1 += 1
        frames.append(buffer)
    else:
        counterThreshold1 = 0

    if counterThreshold1 > START_COOLDOWN:
        print("Recording Activated")
        while True:
            buffer = stream.read(BUFFER_SIZE)
            frames.append(buffer)
            level = audioop.rms(buffer, pa.get_sample_size(FORMAT))
            if level > threshold:
                counterThreshold = 0
            else:
                counterThreshold += 1       #TODO: cut out empty buffers after break
            if counterThreshold > STOP_COOLDOWN:
                break
        break

print("Recording is done")

stream.stop_stream() #Stop and close the stream
stream.close()
pa.terminate()       #Destroy the PyAudio object

wav_data = get_wav(frames, FORMAT, RATE)
flac_data = get_flac(wav_data)


def goog(flac_data):
    result = get_google(flac_data, RATE, "nl-NL")
    print(result)


def wit(wav_data):
    result = get_wit(wav_data, language="nl-NL")
    print(result)


#
# import timeit
#
# t = timeit.Timer("goog(flac_data)", "from __main__ import goog, " + ",".join(globals()))
# print(t.timeit(10))
#
# t = timeit.Timer("wit(wav_data)", "from __main__ import wit, " + ",".join(globals()))
# print(t.timeit(10))
#
goog(flac_data)
wit(wav_data)
