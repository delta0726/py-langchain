"""
Title   : LangChainとLangGraphによるRAG・AIエージェント実践入門
Chapter : 5 LangeChain Expression Language(LCEL)の徹底解説
Section : RunnableLambda（任意の関数をRunnableにする）
Theme   : 前処理/後処理/条件分岐のための関数をChainに加える
Date    : 2025/05/25
Page    : P111-112
"""

# ＜概要＞
# - RunnableLambdaを使うとLCELの任意の処理に関数を適用できるようになる
# - 出力パーサーのアウトプットに対して適用する使用例が多い
# - 入力データを整形してLLMが扱いやすくする使用例もある
# - 条件分岐などに使用することも可能

# ＜ユースケース＞
# 1. 出力パーサーのアウトプットに適用
#   - 文字列出力の変換やエラー処理
#   - 数値データ出力の際の評価関数/スコアリングの適用
#   - 構造化データの変換や抽出（辞書をリストに変換など）
#   - ロギングや保存処理
#   - 出力フォーマットの整形
# 2. 出力
#   - 入力データのクリーニング
#   - 構造の変換
#   - 条件分岐
#   - APIによる外部データの取得や前処理

import os
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnableLambda
from langchain_core.runnables import RunnableConfig
from langchain_core.tracers import LangChainTracer

# 環境変数
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGSMITH_PROJECT"] = "agent-book"


# コンポーネント定義 ------------------------------------------

# ＜ポイント＞
# - 処理の内容を関数として定義してRunnableLambdaでRunnableに変換する
#   --- 今回は出力テキストの文字列を大文字に変換する処理


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


# Runnable関数
convert_upper = RunnableLambda(func=upper)


# LCELによる実行 -----------------------------------------

# チェーン構築
chain = prompt | model | output_parser | convert_upper

# トレーサーの設定
tracer = LangChainTracer()

# 問い合わせ
ai_message = chain.invoke(
    input={"input": "Hello!"}, config=RunnableConfig(tracer=tracer)
)

# 結果確認
# --- 大文字に変換されている
print(ai_message)
