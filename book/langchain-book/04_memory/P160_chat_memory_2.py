"""
Title   : Langchain完全入門
Section : 4 Memory - 過去の対話を短期/長期で記憶する
Theme   : Chainを使って処理を簡素化する
Date    : 2025/04/29
Page    : P160
"""

import chainlit as cl
from langchain.chains import ConversationChain  # ← ConversationChainを追加
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory

"""
<Chatlitの起動>
- 当ファイルのカレントディレクトリでターミナルを起動
- chainlit run .\P160_chat_memory_2.py --port 8001
"""

"""
<記憶のテスト>
会話記憶を保持しているかどうかを確認するためには、「文脈に依存する情報」を尋ねたあと、それを明示せずに再び尋ねることでテストできる
ユーザーの1つ目の発言： 私の名前は田中です。
次の発言でテスト： 私の名前、覚えてる？
"""

# インスタンス構築
# --- チャットモデル
llm = ChatOpenAI(model="gpt-4o-mini")

# 会話メモリの定義
memory = ConversationBufferMemory(return_messages=True)

# Chainの設定
# --- メモリとLLMをセットで管理
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
    result = chain(message.content)
    await cl.Message(content=result["response"]).send()
