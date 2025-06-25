# MAGI ToTを用いて質問に答えるプログラム
import os
import openai
import time
from dotenv import load_dotenv, find_dotenv

# 環境設定
load_dotenv(find_dotenv())
api_key = os.getenv('OPENAI_API_KEY')


# ChatGPTのAPIを呼び出す関数 --- (*1)
def call_chatgpt(prompt):
    # APIを呼び出す
    client = openai.OpenAI()
    completion = client.chat.completions.create(
        model='gpt-4.1-nano', messages=[{'role': 'user', 'content': prompt}]
    )
    # 応答を返す
    return completion.choices[0].message.content


# ユーザーから質問を入力する --- (*2)
user = '今は何時ですか？'
user = user.replace('`', '"')  # 「`」をエスケープ
print('質問: ', user)

# 現在時刻を返すプロンプトを作成 --- (*3)
datetime_str = time.strftime('%Y年%m月%d日 %H:%M')
prompt = f"""
### 指示:
以下の前提情報を利用して質問に答えてください。
### 前提情報:
現在時刻: {datetime_str}
### 質問応答の例:
- 質問: 今何時ですか？
- 応答: 今は、{datetime_str}です。
### 質問:
```{user}```
"""

# ChatGPTを呼び出す --- (*4)
res = call_chatgpt(prompt)
print('AIの答え: ' + res)
time.sleep(3)
