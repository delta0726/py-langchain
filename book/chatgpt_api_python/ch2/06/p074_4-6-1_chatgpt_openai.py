"""
Title   : Chatgpt API & Python
Section : 2 開発環境やAPIの準備をしよう
Theme   : Chatgpt APIの接続テスト（openai）
Date    : 2025/04/30
Page    : P74
"""

from openai import OpenAI


# LLMの定義
client = OpenAI()

# 問い合わせ
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "user", "content": "Pythonについて教えてください"},
    ],
)

# 結果確認
print(response.choices[0].message.content)
