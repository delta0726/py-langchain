"""
Title   : LangChainとLangGraphによるRAG・AIエージェント実践入門
Chapter : 5 LangeChain Expression Language(LCEL)の徹底解説
Section : LCELの｢|｣でさまざまなRunnableを連鎖させる
Theme   : チェイン同士をパイプで連結する
Date    : 2025/06/04
Page    : P108
"""

# ＜概要＞
# - チェイン同士もパイプで結合することができ、新たなチェインを構築することができる
# - 単一のChainと同様にinvoke()などのメソッドを使用することができる
# - この性質により構造的にな問い合わせ(CoTなど)が実現可能となる
#   --- 個々のプロンプトの目的が明確化されて役割の分離が促進される
#   --- プログラムの構造でCoTを表現することでプロンプトの役割を分離する

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

# ＜ポイント＞
# - プロンプト1の段階でCoTが行われている（出力テキストは冗長になっている）
# - プロンプト2は冗長なテキストから結果のみをを抽出している
# - CoTは1人がステップを踏んで考えるだけ（多人数での意見集約を行うものではない）


# LLMモデル
model = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# 出力パーサー
output_parser = StrOutputParser()

# プロンプト1
# --- Chain of Thought (CoT)
cot_prompt = ChatPromptTemplate.from_messages(
    messages=[
        ("system", "ユーザーの質問にステップバイステップで回答してください。"),
        ("human", "{question}"),
    ]
)

# プロンプト2
# --- CoTの結論抽出
summarize_prompt = ChatPromptTemplate.from_messages(
    messages=[
        ("system", "ステップバイステップで考えた回答から結論だけ抽出してください。"),
        ("human", "{text}"),
    ]
)


# LCELによるCotプロセス -----------------------------------------

# チェイン構築
cot_chain = cot_prompt | model | output_parser
summarize_chain = summarize_prompt | model | output_parser

# チェイン結合
# --- 最初のチェインの結果を{text}で受け取る
cot_summarize_chain = cot_chain | summarize_chain

# 質問
question = "10 + 2 * 3"

# トレーサーの設定
tracer = LangChainTracer()

# 問い合わせ
output = cot_summarize_chain.invoke(
    input={"question": question}, config=RunnableConfig(tracer=tracer)
)

# 結果確認
print(output)
