#!/usr/bin/env python3

import pyaudio  #pyaudio for recording
import wave     #wave for creating .wav file
import audioop  #audioOperations for checking volume of sound


#First create the PyAudio object
pa = pyaudio.PyAudio()

#Create a stream for recording
stream = pa.open(format = pyaudio.paInt16,
                 channels = 1,
                 rate = 44100,
                 input = True,
                 frames_per_buffer = 1024)

print("We are now recording")
print("First be silent, calibrating silence")
buffer = stream.read(22050) #half a second
threshold = audioop.rms(buffer, pa.get_sample_size(pyaudio.paInt16)) + 200

frames = []

while True:     #TODO: make this less fast. Give a cooldown
    buffer = stream.read(1024)
    level = audioop.rms(buffer, pa.get_sample_size(pyaudio.paInt16))
    if level > threshold:
        frames.append(buffer)
        while True:
            buffer = stream.read(1024)
            level = audioop.rms(buffer, pa.get_sample_size(pyaudio.paInt16))
            if level > threshold:
                frames.append(buffer)
            else:
                break
        break

print("Recording is done")

stream.stop_stream() #Stop and close the stream
stream.close()
pa.terminate()       #Destroy the PyAudio object

wa = wave.open("output.wav", 'w')
wa.setnchannels(1)
wa.setsampwidth(pa.get_sample_size(pyaudio.paInt16))
wa.setframerate(44100)
wa.writeframes(b''.join(frames))
wa.close()

print("Done. Recorded to file.")

