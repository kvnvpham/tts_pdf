from PyPDF2 import PdfReader
import requests
from base64 import b64decode
import os

API_KEY = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
TTS_ENDPOINT = "https://texttospeech.googleapis.com/v1/text:synthesize"

reader = PdfReader(stream='amazing-me.pdf')
num_pages = len(reader.pages)

story = ""
for num in range(4, 6):
    page = reader.pages[num]
    story += page.extractText()

headers = {
    "X-Goog-Api-Key": API_KEY,
    "Content-Type": "application/json; charset=utf-8"
}

json = {
    "input": {
        "text": story
    },
    "voice": {
        "languageCode": "en-US",
        "name": "en-US-Neural2-F",
        "ssmlGender": "FEMALE"
    },
    "audioConfig": {
        "audioEncoding": "MP3"
    }
}

response = requests.post(TTS_ENDPOINT, headers=headers, json=json)
audio_data = response.json()["audioContent"]

decode_audio = b64decode(audio_data)
with open("audio.mp3", "wb") as file:
    file.write(decode_audio)
