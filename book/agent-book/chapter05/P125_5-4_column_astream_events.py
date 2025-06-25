"""
Title   : LangChainとLangGraphによるRAG・AIエージェント実践入門
Chapter : 5 LangeChain Expression Language(LCEL)の徹底解説
Section : RunnablePassthrough - 入力をそのまま出力する
Theme   : astream_events
Date    : 2025/05/25
Page    : P124
"""

# ＜概要＞
# -

import os
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_community.retrievers import TavilySearchAPIRetriever
from langchain_core.runnables import RunnablePassthrough


# 環境設定
load_dotenv()
api_key = os.getenv("TAVILY_API_KEY")


# コンポーネント定義 ------------------------------------------

# プロンプト
prompt = ChatPromptTemplate.from_template(
    template='''\
以下の文脈だけを踏まえて質問に回答してください。

文脈: """
{context}
"""

質問: {question}
'''
)

# LLMモデル
model = ChatOpenAI(model_name="gpt-4o-mini", temperature=0)


# 検索リトリーバー
retriever = TavilySearchAPIRetriever(k=3)


# RunnableParallelを使う記法 -----------------------------------

# Chain構築
chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | model
    | StrOutputParser()
)


# 非同期実行関数
async def main():
    print("=== LangChain Streaming ===")
    async for event in chain.astream_events("東京の今日の天気は？", version="v2"):
        if event["event"] == "on_parser_stream":
            chunk = event["data"]["chunk"]
            print(chunk, end="", flush=True)


# 実行
await main()
