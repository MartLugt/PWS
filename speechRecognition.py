#!/usr/bin/env python3

import pyaudio
import wave

#First create the PyAudio object
pa = pyaudio.PyAudio()

#Create a stream for recording
stream = pa.open(format = pyaudio.paInt16,
                 channels = 1,
                 rate = 44100,
                 input = True,
                 frames_per_buffer = 1024)

print("We are now recording")

frames = []

for i in range(0, int(44100 / 1024 * 5)) :  #Why do we need this???? (rate / buffersize * record seconds)
    frames.append(stream.read(1024))

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