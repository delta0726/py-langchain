"""
Title   : Chatgpt API & Python
Section : 4 独自のデータで学んだチャットボットを作ろう
Theme   : p158_3-4-1_text.pyと同様
Date    : 2025/05/05
Page    : P163
"""

from openai import OpenAI


# LLMの定義
client = OpenAI()

# 音声ファイルを開く
# --- 1.5分のwavファイル
file = open("sample.wav", "rb")

# 文字起こし
# --- whisperは1分あたり0.006USD(1回の実行で0.01USDくらいかかる)
transcript = client.audio.transcriptions.create(
    model="whisper-1",
    file=file,
)

# 確認
print(transcript.text)
