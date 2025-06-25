"""
Title   : Chatgpt API & Python
Section : 4 独自のデータで学んだチャットボットを作ろう
Theme   : 与えた知識に基づく回答を行うチャットボットの作成
Date    : 2025/05/04
Page    : P134
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

# リスト定義
# --- 会話履歴の格納用
conversation_history = []

while True:
    # ユーザーの入力した文字を変数「user_input」に格納
    user_input = input()

    # 終了
    # --- ユーザーの入力した文字が「exit」の場合はループを抜ける
    if user_input == "exit":
        break

    # 回答出力
    conversation_history.append({"role": "user", "content": user_input})
    answer = answer_question(question=user_input, conversation_history=conversation_history)
    print("ChatGPT:", answer)

    # 回答格納
    conversation_history.append({"role": "assistant", "content": answer})


# 会話履歴の表示
print("\n--- 会話履歴 ---")
print(conversation_history)
