"""
Title   : Langchain完全入門
Section : 4 Memory - 過去の対話を短期/長期で記憶する
Theme   : 会話履歴をDB保存して永続化させる
Date    : 2025/04/27
Page    : P163
"""


import os
import chainlit as cl
from langchain.chains import ConversationChain
from langchain.chat_models import ChatOpenAI
from langchain.memory import RedisChatMessageHistory
from langchain.memory import ConversationBufferMemory


# インスタンス構築
# --- チャットモデル
llm = ChatOpenAI(model="gpt-4o-mini")


history = RedisChatMessageHistory(
    session_id="chat_history",
    url=os.environ.get("REDIS_URL")
    )

# チャット履歴の保存
memory = ConversationBufferMemory(
    return_messages=True, 
    chat_memory=history
    )

# Chainの設定
chain = ConversationChain(memory=memory, llm=llm)

# 開始メッセージ
@cl.on_chat_start
async def on_chat_start():
    await cl.Message(
        content="私は会話の文脈を考慮した返答をできるチャットボットです。メッセージを入力してください。"
    ).send()

# 入出力処理
@cl.on_message
async def on_message(message: str):
    result = chain(message)

    await cl.Message(content=result["response"]).send()
