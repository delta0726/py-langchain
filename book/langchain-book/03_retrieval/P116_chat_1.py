"""
Title   : Langchain完全入門
Section : 3 Retrieval
Theme   : Chainlitの起動
Date    : 2025/04/27
Page    : P116
"""

import chainlit as cl

"""
<Chatlitの起動>
- 当ファイルのカレントディレクトリでターミナルを起動
- chainlit run .\P116_chat_1.py
"""


# ← チャットが開始されたときに実行される関数を定義する
# ← 初期表示されるメッセージを送信する
@cl.on_chat_start
async def on_chat_start():
    await cl.Message(content="準備ができました！メッセージを入力してください！").send()


# ← チャットボットからの返答を送信する
# ← メッセージが送信されたときに実行される関数を定義する
@cl.on_message
async def on_message(input_message):
    print("入力されたメッセージ: " + input_message)
    await cl.Message(content="こんにちは!").send()
