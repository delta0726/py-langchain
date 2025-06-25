"""
Title   : LangChainとLangGraphによるRAG・AIエージェント実践入門
Chapter : 2 OpenAIのチャットAPIの基礎
Section : 
Theme   : OpenAIのライブラリを使ったChatGPTへの問い合わせ
Date    : 2025/05/06
Page    : P26
"""

# ＜ポイント＞
# - OpenAIのライブラリからchatgptを使用する
# - LangChainを使う方法がスタンダードだが、本章では本家のライブラリが使用されている
# - messagesの一連のやり取りが終了するとLLMは会話履歴を消去する（保持されない）

from openai import OpenAI


# LLMの定義
client = OpenAI()

# 問い合わせ
# --- modelとmessagesが必須項目
# --- 単発の問い合わせしかしていない
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "こんにちは！私はジョンと言います！"},
    ],
)

# 確認
print(response.to_json(indent=2))
print(response.choices[0].message.content)
