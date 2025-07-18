"""
Title   : やさしく学ぶLLMエージェント
Chapter : 2 エージェント作成のための基礎知識
Section : 1 OpenAI API 
Theme   : 
Date    : 2025/06/25
Page    : P25
"""

from pathlib import Path

from openai import OpenAI


client = OpenAI()
audio_path = Path("./sample_audio.mp3")

with audio_path.open("rb") as f:
    transcription = client.audio.transcriptions.create(
        model="whisper-1", file=f, temperature=0.0
    )
print(transcription.text)


prompt = "下垣内"

with audio_path.open("rb") as f:
    transcription = client.audio.transcriptions.create(
        model="whisper-1",
        file=f,
        prompt=prompt,
        response_format="text",
        temperature=0.0,
    )
print(transcription)


audio_output_path = Path("output.mp3")
with client.audio.speech.with_streaming_response.create(
    model="tts-hd",
    voice="alloy",
    input="こんにちは。私は AI アシスタントです！",
) as response:
    response.stream_to_file(audio_output_path)