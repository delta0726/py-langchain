"""
Title   : やさしく学ぶLLMエージェント
Chapter : 2 エージェント作成のための基礎知識
Section : 1 OpenAI API 
Theme   : 
Date    : 2025/06/25
Page    : P22
"""

from openai import OpenAI

client = OpenAI()

# 生成できた部分から順に表示する

history = []
n = 10  # 会話の上限
model = "gpt-4o-mini"
for _ in range(n):
    user_input = input("ユーザ入力: ")
    if user_input == "exit":
        break
    print(f"ユーザ: {user_input}")
    history.append({"role": "user", "content": user_input})
    # stream=True でストリーミングを有効化
    stream = client.chat.completions.create(model=model, messages=history, stream=True)
    print("AI: ", end="")
    # 応答を集める文字列
    ai_content = ""
    # ストリーミングの各チャンクを処理
    for chunk in stream:
        # message ではなく ChoiceDelta
        content = chunk.choices[0].delta.content
        # ChoiceDelta の finish_reason が stop なら生成完了
        if chunk.choices[0].finish_reason == "stop":
            break
        print(content, end="")
        ai_content += content
    print()
    history.append({"role": "assistant", "content": ai_content})