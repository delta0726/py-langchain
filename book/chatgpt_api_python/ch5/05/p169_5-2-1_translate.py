import os
from openai import OpenAI
client = OpenAI()

file = open("sample.wav", "rb")

transcript = client.audio.translations.create(
    model="whisper-1",
    file=file,
)

print(transcript.text)