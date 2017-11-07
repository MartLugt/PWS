import speech_to_text
import query_parser
import sys

# TODO: add command line arguments for rate, flac compiler, language, device index. 
frames = speech_to_text.record(rate = 44100, device_index = 1)

wav_data = speech_to_text.get_wav(frames, 44100)
if sys.platform == "linux" or sys.platform == "linux2":
    flac_data = speech_to_text.get_flac_linux(wav_data)
else:
    flac_data = speech_to_text.get_flac(wav_data)

result_google = speech_to_text.get_google(flac_data, 44100, "en-UK")
print(result_google)

print(query_parser.parse(result_google))

