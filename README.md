# Speech assistant
In this repository all of the code files for the assistant are stored.

According to all known laws of aviation, there is no way a bee should bee able to fly.

## Files

#### audio_devices.py
Small Python script to get all of the connected audio devices.  
Used to find out what device index to use for recording and playback on the Raspberry Pi, as this changes depending on which port the microphone is plugged in to.


#### fromfile.py
Python script used for testing of the speech to text engines.  
Uses a .wav file and returns the text as recognised by a lot of different engines.  
Based on [a file from the speech_recognition library](https://github.com/Uberi/speech_recognition/blob/master/examples/audio_transcribe.py).


#### howto.md
Markdown file with instructions and good practices on using Git and GitHub.


#### query_parser.py
Python script that takes text and returns the intent that it thinks you had.  
Basically a bunch of if statements but simplified.


#### speech_to_text.py
Python script that uses google and wit.ai to turn speech into text.  
`TODO: add more info`


#### tts_test.py
Python script for testing different text to speech engines and api's to turn text into speech and play it.  
`TODO: add more info`

