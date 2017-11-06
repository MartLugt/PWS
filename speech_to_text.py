#!/usr/bin/env python3

import audioop  # audio operations for checking volume of sound
import io
import json
import os
import subprocess
import wave  # wave for creating .wav file
from sys import platform
from urllib.parse import urlencode
from urllib.request import Request, urlopen
import pyaudio  # pyaudio for recording
import requests
import sys

# Get OS and set constants
if platform == "win32":
    DEVICE_INDEX = 0
elif platform == "linux" or platform == "linux2":
    DEVICE_INDEX = 1

# Set constants
FORMAT = pyaudio.paInt16  # Audio bit depth
BUFFER_SIZE = 4096  # Buffer size. The smaller the more accurate. Will overflow on Pi if too small.



# get_wav turns buffers into a wav file.
def get_wav(data, rate):
    with io.BytesIO() as file:
        wa = wave.open(file, 'w')
        wa.setnchannels(1)
        wa.setsampwidth(2)
        wa.setframerate(rate)
        wa.writeframes(b''.join(data))
        wav_value = file.getvalue()
        wa.close()
    return wav_value


# Google only accepts flac (snobs), get_flac turns the wav file into a flac_file.
def get_flac(data):
    base_path = "C:\\Users\\162891\AppData\Local\Programs\Python\Python36-32\Lib\site-packages\speech_recognition"
    flac_converter = os.path.join(base_path, "flac-win32.exe")  # For Windows x86 and x86-64.
    process = subprocess.Popen([
        flac_converter,
        "--stdout", "--totally-silent",
        # put the resulting FLAC file in stdout, and make sure it's not mixed with any program output
        "--best",  # highest level of compression available
        "-",  # the input FLAC file contents will be given in stdin
    ], stdin=subprocess.PIPE, stdout=subprocess.PIPE, startupinfo=None)
    result_data, stderr = process.communicate(data)
    return result_data


def get_flac_raw(data):
    base_path = "/home/martlugt/speech_recognition/speech_recognition/"
    flac_converter = os.path.join(base_path, "flac-linux-x86_64")
    process = subprocess.Popen([
        flac_converter,
        "--stdout",
        "--best"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, startupinfo=None)
    result_data, stderr = process.communicate(data)
    return result_data


# Google only accepts flac (snobs), get_flac_pi turns the wav file into a flac_file using the flac module on Pi.
def get_flac_pi(data):
    base_path = "/home/martlugt/speech_recognition/speech_recognition/"
    flac_converter = os.path.join(base_path, "flac-linux-x86_64")  # FOR PI.
    process = subprocess.Popen([
        flac_converter,
        "--stdout", #  "--totally-silent",
        # put the resulting FLAC file in stdout, and make sure it's not mixed with any program output
        "--compression-level-8",  # highest level of compression available
        "-",  # the input FLAC file contents will be given in stdin
    ], stdin=subprocess.PIPE, stdout=subprocess.PIPE, startupinfo=None)
    result_data, stderr = process.communicate(data)
    return result_data


# get_google sends the audio to google and returns the line with the best confidence.
def get_google(data, rate, language="en-US"):
    url = "http://www.google.com/speech-api/v2/recognize?{}".format(urlencode({
        "client": "chromium",
        "lang": language,
        "key": "AIzaSyBOti4mM-6x9WDnZIjIeyEU21OpBXqWBgw",
    }))

    headers = {"Content-Type": "audio/x-flac; rate={}".format(rate)}
    response = requests.post(url, headers=headers, data=data)
    # Now parse it into the sentence with the best confidence
    print(response.text)

    result_full = []
    for line in response.text.split('\n'):
        if not line:
            continue
        r = json.loads(line)["result"]
        if len(r) != 0:
            result_full = r[0]
            break

    if not isinstance(result_full, dict):
        print(result_full)
        raise ValueError

    result_best = result_full["alternative"][0]
    if "confidence" in result_best:
        if result_best["confidence"] < 0.7:
            print("Not confident")
    else:
        print("No confidence information")

    return result_best["transcript"]


# get_wit turns the audio data into a dictionary.
def get_wit(data, language="en-US"):
    url = "https://api.wit.ai/speech"
    if language == "en-US":
        key = "EZ7V7OXWF7TURDDTFCYAM2DWLBX2OAIT"
    elif language == "nl-NL":
        key = "57UW2OZP2T3YMJTQK7CHRBCQM5QGWPNJ"
    else:
        key = None
    headers = {"Authorization": "Bearer " + key, 'accept': 'application/vnd.wit.' + str(6112017) + '+json',
               "Content-Type": "audio/wav"}
    r = requests.post(url, data=data, headers=headers)
    return r.text

def record(rate):
    # First create the PyAudio object
    pa = pyaudio.PyAudio()

    START_COOLDOWN = int(rate / BUFFER_SIZE * 0.2)  # Start cooldown in seconds
    STOP_COOLDOWN = int(rate / BUFFER_SIZE * 0.75)  # Stop cooldown in seconds

    # Create a stream for recording
    stream = pa.open(input_device_index=DEVICE_INDEX,
                     format=FORMAT,
                     channels=1,
                     rate=RATE,
                     input=True,
                     frames_per_buffer=BUFFER_SIZE)

    print("First be silent, calibrating silence")
    buffer = stream.read(int(RATE / 2))  # half a second
    threshold = audioop.rms(buffer, pa.get_sample_size(FORMAT)) * 1.2  # threshold needs to be a bit bigger.

    print("We are now recording. Start talking for it to start.")

    frames = []
    counter_threshold_stop = 0
    counter_threshold_start = 0


    while True:
        buffer = stream.read(BUFFER_SIZE)
        level = audioop.rms(buffer, pa.get_sample_size(FORMAT))
        if level > threshold:
            counter_threshold_start += 1
            frames.append(buffer)
        else:
            frames = []
            counter_threshold_start = 0
        # If sound has been above threshold for n buffers, continue up the loop.
        if counter_threshold_start > START_COOLDOWN:
            print("Recording Activated")
            while True:
                buffer = stream.read(BUFFER_SIZE)
                frames.append(buffer)
                level = audioop.rms(buffer, pa.get_sample_size(FORMAT))
                if level > threshold:
                    counter_threshold_stop = 0
                else:
                    counter_threshold_stop += 1
                # If sound has been below threshold for n buffers, stop recording.
                if counter_threshold_stop > STOP_COOLDOWN:
                    frames = frames[:-STOP_COOLDOWN]  # Removing the buffers written in the stop cooldown.
                    break
            break

    print("Recording is done")

    stream.stop_stream()  # Stop and close the stream
    stream.close()
    pa.terminate()  # Destroy the PyAudio object

    return frames

