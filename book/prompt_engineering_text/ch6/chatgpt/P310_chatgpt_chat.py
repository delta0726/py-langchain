import time
import openai
import os
from dotenv import load_dotenv, find_dotenv

# 環境構築
load_dotenv(find_dotenv())
api_key = os.getenv("OPENAI_API_KEY")

# クライアントを生成
client = openai.OpenAI(api_key=api_key)

# 会話履歴を保持する変数
messages = []


# APIを呼び出す関数
# --- 会話履歴にユーザー入力を追加
# --- APIに問い合わせる際に会話履歴を渡す（これをしないと連続的な会話と認識されない）
# --- 回答を会話履歴を追加
def call_chatgpt_chat(user_text):
    messages.append({"role": "user", "content": user_text})
    completion = client.chat.completions.create(model="gpt-4.1-nano", messages=messages)
    res = completion.choices[0].message.content
    messages.append({"role": "assistant", "content": res})
    return res


# ユーザーからの入力を連続で尋ねる
# --- 質問1：群馬県と有名な温泉を教えて（終了するには"quit"と入力）
# --- 質問2：長野県と有名な温泉を教えて（終了するには"quit"と入力）
# --- ChatGPTを呼び出す
counter = 0  # 入力回数を追跡

while counter < 3:
    user = input("あなた: ")
    if user == "quit" or user == "exit":
        break
    if user == "":
        continue
    res = call_chatgpt_chat(user)
    print("AI: " + res)
    counter += 1

# Finalize
time.sleep(3)
