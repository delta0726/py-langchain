"""
Title   : Langchain完全入門
Section : 4 Memory - 過去の対話を短期/長期で記憶する
Theme   : 過去の記憶を持たないチャットボットの反応を確認する
Date    : 2025/04/27
Page    : P156
"""

import chainlit as cl
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage

"""
<Chatlitの起動>
- 当ファイルのカレントディレクトリでターミナルを起動
- chainlit run .\P156_chat_memory_1-2.py
"""

"""
<記憶なしのテスト>
過去の対話を記憶していないため毎回新しい応答を返します。
- 私の名前は田中です
- 私の名前、覚えてる？
"""


# インスタンス構築
chat = ChatOpenAI(model="gpt-4o-mini")

# 開始メッセージ
@cl.on_chat_start
async def on_chat_start():
    await cl.Message(
        content="私は文脈を保持しないチャットボットです。毎回独立した応答を返します。メッセージを入力してください。"
    ).send()


@cl.on_message
async def on_message(message: str):
    # メッセージをそのまま渡す（記憶なし）
    messages = [HumanMessage(content=message.content)]

    # 言語モデルを呼び出す
    result = chat(messages)

    # AIからのメッセージを送信
    await cl.Message(content=result.content).send()