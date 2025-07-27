"""
Title   : LangChainとLangGraphによるRAG・AIエージェント実践入門
Chapter : 4 LangChainの基礎
Section : 1 LangChainの概要
Theme   : LangSmithのセットアップ
Date    : 2025/05/14
Page    : P66
"""

# ＜概要＞
# - LangSmithはLLMに実行トレースやプロンプト管理ができるWebサービス
# - WebページのTracing Projectにプロジェクトが作成される（小文字）


# ＜URL＞
# https://smith.langchain.com/


import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tracers import LangChainTracer


# 環境変数の設定
# --- その他の設定は環境変数に直接書き込む
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGSMITH_PROJECT"] = "agent-book"

# モデルとプロンプト
llm = ChatOpenAI(model="gpt-4o-mini")
prompt = ChatPromptTemplate.from_template("日本の首都は？")
chain = prompt | llm

# LangSmithトレーサーの設定
tracer = LangChainTracer()

# 問い合わせ
response = chain.invoke(
    {},
    config={
        "callbacks": [tracer],
        "project_name": "AGENT_BOOK",
    }
)

# 確認
print(response.content)
