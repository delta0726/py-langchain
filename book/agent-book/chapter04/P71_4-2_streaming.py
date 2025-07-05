"""
Title   : LangChainとLangGraphによるRAG・AIエージェント実践入門
Chapter : 4 LangChainの基礎
Section : 2 LLM/Chat Model
Theme   : ストリーミング
Date    : 2025/05/14
Page    : P71
"""

# ＜ポイント＞
# - APIの応答をストリーミングで受け取ることができる
# - CallBack機能を使ってストリーミング処理を実装することも化k脳
# - ストリーミング機能はリアルタイム性を高めることでアプリケーションのUXを向上させる

from langchain_core.messages import SystemMessage, HumanMessage
from langchain_openai import ChatOpenAI

# LLMの定義
model = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# メッセージ
messages = [
    SystemMessage(content="You are a helpful assistant."),
    HumanMessage(content="こんにちは！"),
]

# ストリーミング出力
for chunk in model.stream(input=messages):
    print(chunk.content, end="", flush=True)
