"""
Title   : Chatgpt API & Python
Section : 4 独自のデータで学んだチャットボットを作ろう
Theme   : トランスクリプトを取得してLLMで要約する
Date    : 2025/05/05
Page    : P171
"""

from openai import OpenAI

# LLMの定義
client = OpenAI()

# 音声ファイルを開く
# --- 1.5分のwavファイル
file = open("sample.wav", "rb")

# 文字起こし
# --- whisperは1分あたり0.006USD(1回の実行で0.01USDくらいかかる)
transcript = client.audio.translations.create(
    model="whisper-1",
    file=file,
)

# ChatGPTで要約する
summary = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {
            "role": "user",
            "content": f"以下の文章を日本語に翻訳し、3行の箇条書きで要約してください:\n{transcript}"
        }
    ]
)

print(f"要約結果: \n{summary.choices[0].message.content}")
print(f"要約に使用したトークン数: {summary.usage.total_tokens}")
