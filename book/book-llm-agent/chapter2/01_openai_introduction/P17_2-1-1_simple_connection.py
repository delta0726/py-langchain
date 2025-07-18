"""
Title   : やさしく学ぶLLMエージェント
Chapter : 2 エージェント作成のための基礎知識
Section : 1 OpenAI API 
Theme   : 
Date    : 2025/06/25
Page    : P21
"""

# テキスト生成の基本的な流れ

from openai import OpenAI

client = OpenAI()

response = client.chat.completions.create(
    temperature=0.0,
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "こんにちは"}],
)

print(response.choices[0].message.content)


# シンプルな対話 AI の作成

history = []
n = 10  # 会話の上限
model = "gpt-4o-mini"
for _ in range(n):
    user_input = input("ユーザ入力: ")
    if user_input == "exit":
        break
    print(f"ユーザ: {user_input}")
    history.append({"role": "user", "content": user_input})
    response = client.chat.completions.create(model=model, messages=history)
    content = response.choices[0].message.content
    print(f"AI: {content}")
    history.append({"role": "assistant", "content": content})