"""
Title   : LangChainとLangGraphによるRAG・AIエージェント実践入門
Chapter : 5 LangeChain Expression Language(LCEL)の徹底解説
Section : 5 まとめ
Theme   : Chat HistoryとMemory
Date    : 2025/06/28
Page    : P126
"""

# ＜概要＞
# - アプリケーションを想定して会話履歴を管理したい場合はmemory機能を活用

import os
from uuid import uuid4
from dotenv import load_dotenv

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langchain_community.chat_message_histories import SQLChatMessageHistory

# 環境設定
load_dotenv()
api_key = os.getenv("TAVILY_API_KEY")


# コンポーネント定義 ------------------------------------------

# プロンプト
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant."),
        MessagesPlaceholder("chat_history", optional=True),
        ("human", "{input}"),
    ]
)

# LLMモデル
model = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# Chain構築
chain = prompt | model | StrOutputParser()


# 関数定義 :SQLiteで会話履歴を管理 ------------------------------------

# ＜ポイント＞
# - 関数内で問い合わせと履歴のDB書き込みを行う
# - 会話履歴をSQLiteに書き込む


def respond(session_id: str, human_message: str) -> str:
    # DB定義
    chat_message_history = SQLChatMessageHistory(
        session_id=session_id, connection="sqlite:///sqlite.db"
    )

    # 問い合わせ
    ai_message = chain.invoke(
        input={
            "chat_history": chat_message_history.get_messages(),
            "input": human_message,
        }
    )

    # 履歴の書き込み
    chat_message_history.add_user_message(message=human_message)
    chat_message_history.add_ai_message(message=ai_message)

    return ai_message


# 実行 --------------------------------------------------------------

# セッション開始
session_id = uuid4().hex

# 会話
output1 = respond(
    session_id=session_id,
    human_message="こんにちは！私はジョンと言います！",
)
print(output1)

output2 = respond(
    session_id=session_id,
    human_message="私の名前が分かりますか？",
)
print(output2)
