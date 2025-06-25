# -*- coding: utf-8 -*-
import os
import sys
import time
import platform
import openai
from dotenv import load_dotenv, find_dotenv

# 環境設定
load_dotenv(find_dotenv())
api_key = os.getenv("OPENAI_API_KEY")

# 問い合わせ
client = openai.OpenAI(api_key=api_key)
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "iPhone8のリリース日を教えて"}],
    max_tokens=100,  # ←最大のトークン数
    n=3,  # ←生成する文章の数
    temperature=0,  # ←多様性を表すパラメータ(0が安定的、1が多様性)
)

# ChatGPTのレスポンス内容を出力
print("=== ChatGPTからの返答 ===")
for i, choice in enumerate(response.choices):
    print(f"[Response {i + 1}]")
    print(choice.message.content)

# 実行環境の情報を出力
print("\n--- 実行環境の情報 ---")
print(f"Pythonバージョン : {platform.python_version()}")
print(f"Python実行ファイル : {sys.executable}")
print(f"使用中の仮想環境 : {os.environ.get('CONDA_DEFAULT_ENV', '仮想環境情報なし')}")

# 確認用
time.sleep(5)
