"""
Title   : Langchain完全入門
Section : 2 Language Models
Theme   : ストリーミングモードで結果を逐次表示
Date    : 2025/04/26
Page    : P74
"""

from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage


# インスタンスの作成
# --- streamingをTrueに設定し、ストリーミングモードで実行
# --- StreamingStdOutCallbackHandlerはコールバックの方法を指定（到着の都度print）
chat = ChatOpenAI(
    streaming=True,
    callbacks=[StreamingStdOutCallbackHandler()],
)

# 問い合わせ
# --- ストリーミングモードでの実行
resp = chat(messages=[HumanMessage(content="おいしいステーキの焼き方を教えて")])
