import requests
from io import BytesIO
import pyaudio
import wave


BUFFER_SIZE = 1024

pa = pyaudio.PyAudio()


def get_watson(text, female = False):
    username = "6014826e-8384-4738-8e1f-16a398ee3f95"
    password = "kbfIz4iR3xGi"
    url = "https://stream.watsonplatform.net/text-to-speech/api/v1/synthesize"

    if female:
        params = (
            ("accept", "audio/wav"),
            ("text", text),
            ("voice", "en-US_LisaVoice"),
        )
    else:
        params = (
            ("accept", "audio/wav"),
            ("text", text),
            ("voice", "en-US_MichaelVoice"),
        )

    request = requests.get(url, params = params, auth=(username, password))
    print(request.content)
    print(request)
    return request


def play(request):
    # Turn the request data into a temperory file that is held in memory as a string.
    file = BytesIO(request.content)
    w = wave.open(file, "r")  # open the file with wave in r(read) mode

    stream = pa.open(format=pa.get_format_from_width(w.getsampwidth()),
                     channels=w.getnchannels(),
                     rate=w.getframerate(),
                     output=True)

    data = w.readframes(BUFFER_SIZE)

    while data:
        stream.write(data)
        data = w.readframes(BUFFER_SIZE)

    stream.stop_stream()
    stream.close()


def play_ding():
    file = "./resources/ding.wav"
    w = wave.open(file, "r")

    pa = pyaudio.PyAudio()
    stream = pa.open(format=pa.get_format_from_width(w.getsampwidth()),
                    channels=w.getnchannels(),
                    rate=w.getframerate(),
                    output=True)

    data = w.readframes(BUFFER_SIZE)

    while data:
        stream.write(data)
        data = w.readframes(BUFFER_SIZE)

    stream.stop_stream()
    stream.close()

    pa.terminate()


def play_dong():
    file = "./resources/dong.wav"
    w = wave.open(file, "r")

    pa = pyaudio.PyAudio()
    stream = pa.open(format=pa.get_format_from_width(w.getsampwidth()),
                    channels=w.getnchannels(),
                    rate=w.getframerate(),
                    output=True)

    data = w.readframes(BUFFER_SIZE)

    while data:
        stream.write(data)
        data = w.readframes(BUFFER_SIZE)

    stream.stop_stream()
    stream.close()

    pa.terminate()
