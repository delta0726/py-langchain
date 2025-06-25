"""
Title   : Chatgpt API & Python
Section : 4 独自のデータで学んだチャットボットを作ろう
Theme   : whisperを使って字幕形式で出力する
Date    : 2025/05/05
Page    : P160
"""

from openai import OpenAI

# LLMの定義
client = OpenAI()

# 音声ファイルを開く
# --- 1.5分のwavファイル
file = open("wav/sample.wav", "rb")

# 文字起こし
# --- パラメータを追加(srt: 字幕形式)
# --- whisperは1分あたり0.006USD(1回の実行で0.01USDくらいかかる)
transcript = client.audio.transcriptions.create(
    model="whisper-1", file=file, response_format="srt"
)

# 結果表示
print(transcript)
