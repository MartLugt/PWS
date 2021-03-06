#!/usr/bin/env python3

import audioop  # audio operations for checking volume of sound
import base64
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
import text_to_speech

# Set constants
FORMAT = pyaudio.paInt16  # Audio bit depth

pa = pyaudio.PyAudio()
STREAM = pa.open(channels=1,
                 format=FORMAT,
                 rate=44100,
                 input=True,
                 frames_per_buffer=BUFFER_SIZE,
                  )

BUFFER_SIZE = 16384  # Buffer size. The smaller the more accurate. Will overflow on Pi if too small.



# get_wav turns buffers into a wav file.
def get_wav(data, rate=44100):
    with io.BytesIO() as file:
        wa = wave.open(file, 'w')
        wa.setnchannels(1)
        wa.setsampwidth(2)
        wa.setframerate(rate)
        wa.writeframes(b''.join(data))
        wav_value = file.getvalue()
        bvalue = base64.b64encode(wav_value)
        wa.close()
    return wav_value, bvalue


# Google only accepts flac (snobs), get_flac turns the wav file into a flac_file.
def get_flac(data):
    base_path = "C:\\Users\\Mart\\Desktop"
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


# Google only accepts flac (snobs), get_flac_pi turns the wav file into a flac_file using the flac module on Pi.
def get_flac_linux(data):
    base_path = "/usr/bin/"
    flac_converter = os.path.join(base_path, "flac")  # for linux
    process = subprocess.Popen([
        flac_converter,
        "--stdout",
        "--totally-silent",
        # put the resulting FLAC file in stdout, and make sure it's not mixed with any program output
        "--compression-level-8",  # highest level of compression available
        "-",  # the input FLAC file contents will be given in stdin
    ], stdin=subprocess.PIPE, stdout=subprocess.PIPE, startupinfo=None)
    result_data, stderr = process.communicate(data)
    return result_data


# get_google sends the audio to google and returns the line with the best confidence.
def get_google(data, rate, language="en-US", full=False):
    url = "http://www.google.com/speech-api/v2/recognize?{}".format(urlencode({
        "client": "chromium",
        "lang": language,
        "key": "AIzaSyBOti4mM-6x9WDnZIjIeyEU21OpBXqWBgw",
    }))

    headers = {"Content-Type": "audio/x-flac; rate={}".format(rate)}
    response = requests.post(url, headers=headers, data=data)
    # Now parse it into the sentence with the best confidence

    result_full = []
    for line in response.text.split('\n'):
        if not line:
            continue
        r = json.loads(line)["result"]
        if len(r) != 0:
            result_full = r[0]
            break

    if full:
        return result_full

    if not isinstance(result_full, dict):
        print(result_full)
        raise ValueError

    result_best = result_full["alternative"][0]
    if "confidence" in result_best:
        if result_best["confidence"] < 0.7:
            print("Not confident")
    else:
        print("No confidence information")
    print(result_best["transcript"])
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


def record(rate = 44100, ding=False, start_s=0.2, stop_s=0.75):

    # First create the PyAudio object
    start_cooldown = int(rate / BUFFER_SIZE * start_s)  # Start cooldown in seconds
    stop_cooldown = int(rate / BUFFER_SIZE * stop_s)  # Stop cooldown in seconds

    STREAM.start_stream()

    print("First be silent, calibrating silence")
    buffer = STREAM.read(int(rate/2))

    threshold = audioop.rms(buffer, pa.get_sample_size(FORMAT)) * 1.2  # threshold needs to be a bit bigger.

    print("We are now recording. Start talking for it to start.")

    if ding:
        text_to_speech.play_ding()

    frames = []
    counter_threshold_stop = 0
    counter_threshold_start = 0

    while True:
        buffer = STREAM.read(BUFFER_SIZE)
        level = audioop.rms(buffer, pa.get_sample_size(FORMAT))
        if level > threshold:
            counter_threshold_start += 1
            frames.append(buffer)
        else:
            frames = []
            counter_threshold_start = 0
        # If sound has been above threshold for n buffers, continue up the loop.
        if counter_threshold_start > start_cooldown:
            print("Recording Activated")
            while True:
                buffer = STREAM.read(BUFFER_SIZE)
                frames.append(buffer)
                level = audioop.rms(buffer, pa.get_sample_size(FORMAT))
                if level > threshold:
                    counter_threshold_stop = 0
                else:
                    counter_threshold_stop += 1
                # If sound has been below threshold for n buffers, stop recording.
                if counter_threshold_stop > stop_cooldown:
                    frames = frames[:-stop_cooldown]  # Removing the buffers written in the stop cooldown.
                    break
            break

    print("Recording is done")

    STREAM.stop_stream()  # Stop and close the stream
    # stream.close()
    # pa.terminate()  # Destroy the PyAudio object

    if ding:
        text_to_speech.play_dong()

    return frames

# record(44100, 1)
