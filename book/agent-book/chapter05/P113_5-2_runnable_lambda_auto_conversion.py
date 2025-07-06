"""
Title   : LangChainとLangGraphによるRAG・AIエージェント実践入門
Chapter : 5 LangeChain Expression Language(LCEL)の徹底解説
Section : RunnableLambda（任意の関数をRunnableにする）
Theme   : RunnableLambdaへの自動変換
Date    : 2025/05/25
Page    : P113
"""

# ＜概要＞
# - RunnableLambdaを関数やデコレータで明示的に作成しなくても、実は自動作成される
#   --- 適用する関数の引数が受け取れない場合はエラーとなる
#   --- 実務では明示的にRunnableLambdaであることを示した方が良さそうだ

import os
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnableConfig
from langchain_core.tracers import LangChainTracer

# 環境変数
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGSMITH_PROJECT"] = "agent-book"

# コンポーネント定義 ------------------------------------------

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
def upper(text: str) -> str:
    return text.upper()


# 1.エラーとなるケース ------------------------------------

# ＜ポイント＞
# - upper関数は文字列を引数とする
# - modelの戻り値は文字列ではないためエラーとなる

# チェーン構築
# --- 出力パーサーをつけていない
chain = prompt | model | upper

# 問い合わせ
# --- 以下のコードを実行するとエラーとなる
# --- upper()はStrOutputParserの文字列に対して適用するため
output = chain.invoke(input={"input": "Hello!"})


# 2.自動変換されるケース -----------------------------------

# ＜ポイント＞
# - upper関数は文字列を引数とする
# - strOutputParserの戻り値は文字列であるため自動変換される

# 出力パーサーの定義
output_parser = StrOutputParser()

# チェーン構築
chain = prompt | model | output_parser | upper

# トレーサーの設定
tracer = LangChainTracer()

# 問い合わせ
output = chain.invoke(input={"input": "Hello!"}, config=RunnableConfig(tracer=tracer))

# 結果確認
print(output)
