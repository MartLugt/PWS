# Speech assistant
### This is the develpment branch
All changes should be commited to this branch and this branch should then be merged with the release branches.

In this repository all of the code files for the assistant are stored.

The text can be found at [Overleaf](https://www.overleaf.com/read/sfsdgrsfgmfb)

This repository has 3 branches. The master branch with snowboy binaries compiled for x64 UNIX systems, the RPI branch which is for the Raspberry Pi, with snowboy binaries compiled for ARMv6 UNIX systems and slightly modified Python files to make them work on the Pi. The dev branch is for working on code that applies to both branches.

## Files

#### Test***\*.wav
These files are the audio files used to feed into fromfile.py to test the speech to text engines.

#### \*.svg
Logo's

#### assistant.py
This file connects all the other files together to turn them into one cohesive program.

#### \_snowboydetect.so
Binary file that uses neural networks to detect keywords on UNIX machines.

#### commands.py
Python file with different commands the assistant responds to.

#### \*.pmdl
Voice model files for Snowboy.

#### snowboydetect.py
Low-level python file generated by snowboy. Contains Python3 bindings for \_snowboydetect.so.

#### snowboydecoder.py
Higher level python file which can be used to communicate with snowboydetect.

#### audio_devices.py
Small Python script to get all of the connected audio devices.  
Used to find out what device index to use for recording and playback on the Raspberry Pi, as this changes depending on which port the microphone is plugged in to.


#### fromfile.py
Python script used for testing of the speech to text engines.  
Uses a .wav file and returns the text as recognised by a lot of different engines.  
Based on [a file from the speech_recognition library](https://github.com/Uberi/speech_recognition/blob/master/examples/audio_transcribe.py).


#### query_parser.py
Python script that takes text and returns the intent that it thinks you had.  
Basically a bunch of if statements but simplified.


#### speech_to_text.py
Python script that uses google and wit.ai to turn speech into text.  


#### text_to_speech.py
Turns text into speech using IBM Watson.

#### tts_test.py
Python script for testing different text to speech engines and api's to turn text into speech and play it.  


