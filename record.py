#!/usr/bin/env python3

import pyaudio  #pyaudio for recording
import wave     #wave for creating .wav file
import audioop  #audioOperations for checking volume of sound

#Set constants
FORMAT = pyaudio.paInt16
RATE = 44100
BUFFER_SIZE = 1024
START_COOLDOWN = 9
STOP_COOLDOWN = 43

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

print("We are now recording")

frames = []
counterThreshold = 0    #TODO: give this a better name
counterThreshold1 = 0   #TODO: give this a better name too

#If sound has been above threshold for n buffers, continue up the loop

while True:     #TODO: make this less fast. Give a cooldown
    buffer = stream.read(BUFFER_SIZE)
    level = audioop.rms(buffer, pa.get_sample_size(FORMAT))
    if level > threshold:
        print("over")
        counterThreshold1 += 1
        frames.append(buffer)
    else:
        print("under")
        counterThreshold1 = 0

    if counterThreshold1 > START_COOLDOWN:
        while True:
            buffer = stream.read(BUFFER_SIZE)
            frames.append(buffer)
            level = audioop.rms(buffer, pa.get_sample_size(FORMAT))
            if level > threshold:
                print("OVER")
                counterThreshold = 0
            else:
                print("UNDER")
                counterThreshold += 1       #TODO: cut out empty buffers after break
            if counterThreshold > STOP_COOLDOWN:
                break
        break

print("Recording is done")

stream.stop_stream() #Stop and close the stream
stream.close()
pa.terminate()       #Destroy the PyAudio object

wa = wave.open("output.wav", 'w')
wa.setnchannels(1)
wa.setsampwidth(pa.get_sample_size(FORMAT))
wa.setframerate(RATE)
wa.writeframes(b''.join(frames))
wa.close()

print("Done. Recorded to file output.wav.")
