# -*- coding: utf-8 -*-
import os
import time
import sys
import platform
import openai
from dotenv import load_dotenv, find_dotenv

# 環境設定
load_dotenv(find_dotenv())
api_key = os.getenv("OPENAI_API_KEY")

client = openai.OpenAI(api_key=api_key)
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "iPhone8のリリース日を教えて"}],
)


# ChatGPTのレスポンス内容を出力
print(response.choices[0].message.content)

# 実行環境の情報を出力
print("\n--- 実行環境の情報 ---")
print(f"Pythonバージョン : {platform.python_version()}")
print(f"Python実行ファイル : {sys.executable}")
print(f"使用中の仮想環境 : {os.environ.get('CONDA_DEFAULT_ENV', '仮想環境情報なし')}")

# 確認用
time.sleep(5)
