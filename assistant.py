import speech_to_text
import query_parser
import platform

frames = speech_to_text.record()

wav_data = speech_to_text.get_wav(frames, 44100)
if platform == "linux" or platform == "linux2":
    flac_data = speech_to_text.get_flac_pi(wav_data)
else:
    flac_data = speech_to_text.get_flac(wav_data)

result_google = speech_to_text.get_google(flac_data, 44100, "nl-NL")
print(result_google)
