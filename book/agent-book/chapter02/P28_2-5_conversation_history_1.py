"""
Title   : LangChainとLangGraphによるRAG・AIエージェント実践入門
Chapter : 2 OpenAIのチャットAPIの基礎
Section : 
Theme   : 会話履歴を記憶したうえでの応答（記憶あり）
Date    : 2025/05/06
Page    : P28
"""

# ＜ポイント＞
# - 会話履歴を踏まえた回答をしてほしい場合は、一連のやり取りをリクエストに含める必要がある
# - 具体的にはmessageに辞書形式で複数の会話を含めることで実現する

from openai import OpenAI


# LLMの定義
client = OpenAI()

# 問い合わせ
# --- messagesで会話のやり取りを残すことで会話履歴を記憶する
# --- userとassistant(AI)の会話を続けることで履歴が残る
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "こんにちは！私はジョンと言います！"},
        {
            "role": "assistant",
            "content": "こんにちは、ジョンさん！お会いできて嬉しいです。",
        },
        {"role": "user", "content": "私の名前が分かりますか？"},
    ],
)

# 確認
# --- ジョンという名前を記憶している
print(response.to_json(indent=2))
print(response.choices[0].message.content)
