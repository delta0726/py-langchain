import time  # -*- coding: utf-8 -*-
import openai
import os
from dotenv import load_dotenv, find_dotenv

# 環境設定
load_dotenv(find_dotenv())
api_key = os.getenv("OPENAI_API_KEY")


# APIを呼び出す関数 --- (*1)
def call_chatgpt(prompt):
    client = openai.OpenAI(api_key=api_key)
    completion = client.chat.completions.create(
        model="gpt-4.1-nano", messages=[{"role": "user", "content": prompt}]
    )
    return completion.choices[0].message.content


# 実際に動かす --- (*2)
print(call_chatgpt("深呼吸してから、三毛猫の名前を3つ考えてください。"))
time.sleep(3)
