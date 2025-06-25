"""
Title   : Chatgpt API & Python
Section : 4 独自のデータで学んだチャットボットを作ろう
Theme   : whisperを使って音声データの文字おこしをする
Date    : 2025/05/05
Page    : P158
"""

from openai import OpenAI

# LLMの定義
client = OpenAI()

# 音声ファイルを開く
# --- 1.5分のwavファイル
file = open("wav/sample.wav", "rb")

# 文字起こし
# --- whisperは1分あたり0.006USD(1回の実行で0.01USDくらいかかる)
transcript = client.audio.transcriptions.create(
    model="whisper-1",
    file=file,
)

# 結果表示
print(transcript.text)

# 保存
with open("text/output.txt", "w", encoding="utf-8") as file:
    file.write(transcript.text)
