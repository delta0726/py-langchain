"""
Title   : Langchain完全入門
Section : 4 Memory - 過去の対話を短期/長期で記憶する
Theme   : 過去の記憶を持つチャットボットの作成
Date    : 2025/04/29
Page    : P156
"""

import chainlit as cl
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.schema import HumanMessage

"""
<Chatlitの起動>
- 当ファイルのカレントディレクトリでターミナルを起動
- chainlit run .\P156_chat_memory_1-1.py
"""

"""
<記憶のテスト>
会話記憶を保持しているかどうかを確認するためには、「文脈に依存する情報」を尋ねたあと、それを明示せずに再び尋ねることでテストできる
ユーザーの1つ目の発言： 私の名前は田中です。
次の発言でテスト： 私の名前、覚えてる？
"""


# インスタンス構築
# --- チャットモデル
chat = ChatOpenAI(model="gpt-4o-mini")

# 会話メモリの定義
memory = ConversationBufferMemory(return_messages=True)


# 開始メッセージ
@cl.on_chat_start
async def on_chat_start():
    await cl.Message(
        content="私は会話の文脈を考慮した返答ができるチャットボットです。メッセージを入力してください。"
    ).send()


# 入出力処理
@cl.on_message
async def on_message(message: str):
    # メモリの内容を取得
    memory_message_result = memory.load_memory_variables({})

    # メモリの内容からメッセージのみを取得
    messages = memory_message_result["history"]
    messages.append(HumanMessage(content=message.content))

    # 言語モデルを呼び出す
    result = chat(messages)

    # メモリにメッセージを追加
    memory.save_context(
        {"input": message.content},
        {"output": result.content},
    )

    # AIからのメッセージを送信
    await cl.Message(content=result.content).send()
