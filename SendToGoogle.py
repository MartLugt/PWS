#!/usr/bin/env python3

from urllib.request import Request

url = "http://www.google.com/speech-api/v2/recognize?{}".format(urlencode({
    "client": "chromium",
    "lang": "en-UK",
    "key": "AIzaSyBOti4mM-6x9WDnZIjIeyEU21OpBXqWBgw",
    }))
request = Request(url, data=output.wav