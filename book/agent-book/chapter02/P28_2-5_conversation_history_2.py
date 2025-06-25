"""
Title   : LangChainとLangGraphによるRAG・AIエージェント実践入門
Chapter : 2 OpenAIのチャットAPIの基礎
Section : 
Theme   : 会話履歴を記憶したうえでの応答（記憶なし）
Date    : 2025/05/06
Page    : P28
"""

# ＜ポイント＞
# - 会話履歴を踏まえた回答をしてほしい場合は、一連のやり取りをリクエストに含める必要がある
# - インスタンスが別になると会話履歴は保持されない

from openai import OpenAI


# LLMの定義
client = OpenAI()

# 問い合わせ
# --- response_1で名前を伝え、response_2で名前の記憶を問いかける
response_1 = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "こんにちは！私はジョンと言います！"},
    ],
)

response_2 = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "私の名前が分かりますか？"},
    ],
)

# 確認
# --- 対話を繋げていないので名前を記憶していない
print(response_1.choices[0].message.content)
print(response_2.choices[0].message.content)
