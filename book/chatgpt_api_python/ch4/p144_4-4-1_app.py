"""
Title   : Chatgpt API & Python
Section : 4 独自のデータで学んだチャットボットを作ろう
Theme   : チャットボットに性格を与える
Date    : 2025/05/02
Page    : P144
"""

from openai import OpenAI
from search import answer_question

"""
質問1: チェックインは何時から可能ですか？
質問2: 駐車場はありますか？
質問3: exit
"""

# LLMの定義
client = OpenAI()

# 最初にメッセージを表示する
print("質問を入力してください")

conversation_history = [
    {
        "role": "system",
        "content": "あなたは世界的に有名な詩人です。詩的な比喩表現を使って回答してください",
    }
]

while True:
    # ユーザーの入力した文字を変数「user_input」に格納
    user_input = input()

    # ユーザーの入力した文字が「exit」の場合はループを抜ける
    if user_input == "exit":
        break

    conversation_history.append({"role": "user", "content": user_input})
    answer = answer_question(user_input, conversation_history)

    print("ChatGPT:", answer)
    conversation_history.append({"role": "assistant", "content": answer})


# 会話履歴の表示
print("\n--- 会話履歴 ---")
print(conversation_history)
