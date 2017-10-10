#!/usr/bin/env python3

import audioop  # audioOperations for checking volume of sound
import io
import json
import os
import subprocess
import wave  # wave for creating .wav file
from urllib.parse import urlencode

import pyaudio  # pyaudio for recording
import requests

# Add comments explaining why, not what!!

# Set constants
FORMAT = pyaudio.paInt16
RATE = 44100
BUFFER_SIZE = 4096
START_COOLDOWN = int(RATE / BUFFER_SIZE * 0.2)  # In seconds
STOP_COOLDOWN = int(RATE / BUFFER_SIZE * 0.75)  # In seconds
DEVICE_INDEX = 0  # 2, needs to be 0 for windows, use audio_devices.py to determine right index


class UnknownValueError(Exception):
    pass


def get_wav(frames, format, rate):
    with io.BytesIO() as file:
        wa = wave.open(file, 'w')
        wa.setnchannels(1)
        wa.setsampwidth(2)
        wa.setframerate(rate)
        wa.writeframes(b''.join(frames))
        wav_value = file.getvalue()
        wa.close()
    return wav_value


def get_flac(wav_data):
    base_path = "C:\\Users\martv\AppData\Local\Programs\Python\Python35\Lib\site-packages\speech_recognition\\"
    flac_converter = os.path.join(base_path, "flac-win32.exe")  # For Windows x86 and x86-64.
    process = subprocess.Popen([
        flac_converter,
        "--stdout", "--totally-silent",
        # put the resulting FLAC file in stdout, and make sure it's not mixed with any program output
        "--best",  # highest level of compression available
        "-",  # the input FLAC file contents will be given in stdin
    ], stdin=subprocess.PIPE, stdout=subprocess.PIPE, startupinfo=None)
    flac_data, stderr = process.communicate(wav_data)
    return flac_data


def get_flac_pi(wav_data):
    base_path = "/usr/bin"
    flac_converter = os.path.join(base_path, "flac")  # FOR PI.
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
    response = requests.post(url, headers=headers, data=flac_data)
    # Now parse it into the sentence with the best confidence
    print(response.text)

    result_full = []
    for line in response.text.split('\n'):
        if line == "":
            continue
        r = json.loads(line)["result"]
        if r:
            result_full = r[0]

    if not isinstance(result_full, dict):
        raise UnknownValueError()

    if "alternative" in result_full["alternative"]:
        result_best = max(result_full["alternative"], key=lambda alternative: alternative["confidence"])
        if lambda alternative: alternative["confidence"] < 0.7:
            print("not confident; confidence < 0,7")
    else:
        result_best = result_full["alternative"][0]
        print("not confident; no confidence info")
    return result_best["transcript"]


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


# First create the PyAudio object
pa = pyaudio.PyAudio()

# Create a stream for recording
stream = pa.open(input_device_index=DEVICE_INDEX,
                 format=FORMAT,
                 channels=1,
                 rate=RATE,
                 input=True,
                 frames_per_buffer=BUFFER_SIZE)

print("First be silent, calibrating silence")
buffer = stream.read(int(RATE / 2))  # half a second
threshold = audioop.rms(buffer, pa.get_sample_size(FORMAT)) + 200

print("We are now recording. Start talking for it to start.")

frames = []
counter_threshold_stop = 0
counter_threshold_start = 0

# If sound has been above threshold for n buffers, continue up the loop

while True:
    buffer = stream.read(BUFFER_SIZE)
    level = audioop.rms(buffer, pa.get_sample_size(FORMAT))
    if level > threshold:
        counter_threshold_start += 1
        frames.append(buffer)
    else:
        counter_threshold_start = 0

    if counter_threshold_start > START_COOLDOWN:
        print("Recording Activated")
        while True:
            buffer = stream.read(BUFFER_SIZE)
            frames.append(buffer)
            level = audioop.rms(buffer, pa.get_sample_size(FORMAT))
            if level > threshold:
                counter_threshold_stop = 0
            else:
                counter_threshold_stop += 1  # TODO: cut out empty buffers after break
            if counter_threshold_stop > STOP_COOLDOWN:
                break
        break

print("Recording is done")

stream.stop_stream()  # Stop and close the stream
stream.close()
pa.terminate()  # Destroy the PyAudio object

wav_data = get_wav(frames, FORMAT, RATE)
flac_data = get_flac(wav_data)

result_google = get_google(flac_data, RATE, "en-US")
print(result_google)

result_wit = get_wit(wav_data, language="en-US")
print(result_wit)
