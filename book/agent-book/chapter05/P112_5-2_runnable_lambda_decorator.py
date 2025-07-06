"""
Title   : LangChainとLangGraphによるRAG・AIエージェント実践入門
Chapter : 5 LangeChain Expression Language(LCEL)の徹底解説
Section : RunnableLambda（任意の関数をRunnableにする）
Theme   : chainデコレータを使ったRunnableLambdaの実装
Date    : 2025/05/25
Page    : P112
"""

# ＜概要＞
# - RunnableLambdaはchainデコレータを使って実装することもできる
# - デコレータの方が冗長性が少ないコードとして記述できる
# - 適用したい関数が複数ある場合はchainデコレータの方がスマート
# - チェイン構造を意識する際はRunnableLambda()の方が明示的でよい

import os
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.runnables import chain
from langchain_core.runnables import RunnableConfig
from langchain_core.tracers import LangChainTracer

# 環境変数
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGSMITH_PROJECT"] = "agent-book"


# コンポーネント定義 ------------------------------------------

# ＜ポイント＞
# - RunnableLambdaは関数に@chainのデコレータをつけるだけで作成することが可能


# プロンプト
prompt = ChatPromptTemplate.from_messages(
    messages=[
        ("system", "You are a helpful assistant."),
        ("human", "{input}"),
    ]
)

# モデル
model = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# 出力パーサー
output_parser = StrOutputParser()


# 関数定義
# --- 大文字変換
@chain
def upper(text: str) -> str:
    return text.upper()


# LCELによる実行 -----------------------------------------

# ＜ポイント＞
# - 関数名がそのままRunnableになっている


# チェーン構築
# --- 出力結果に対して関数を適用（関数を直接指定）
chain = prompt | model | output_parser | upper

# トレーサーの設定
tracer = LangChainTracer()

# 問い合わせ
ai_message = chain.invoke(
    input={"input": "Hello!"}, config=RunnableConfig(tracer=tracer)
    )

# 結果確認
print(ai_message)
