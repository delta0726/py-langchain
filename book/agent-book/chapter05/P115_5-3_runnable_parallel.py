"""
Title   : LangChainとLangGraphによるRAG・AIエージェント実践入門
Chapter : 5 LangeChain Expression Language(LCEL)の徹底解説
Section : RunnableParallel（複数のRunnableを並列につなげる）
Theme   : Chainを活用して複数の問い合わせを並列的に行う
Date    : 2025/06/04
Page    : P115
"""

# ＜概要＞
# - RunnableParallelを使うと複数のChainをまとめて問い合わせることができる
# - 複数視点で問い合わせしたい場合に使用し、結果は辞書型で返される
# - 内部的には並列的に問い合わせしているため、逐次的に問い合わせるより高速

import pprint
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnableParallel


# コンポーネント定義 ------------------------------------------

# LLMモデル
model = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# 出力パーサー
output_parser = StrOutputParser()

# プロンプト
# --- 楽観主義者
optimistic_prompt = ChatPromptTemplate.from_messages(
    messages=[
        (
            "system",
            "あなたは楽観主義者です。ユーザーの入力に対して楽観的な意見をください。",
        ),
        ("human", "{topic}"),
    ]
)

# プロンプト
# --- 悲観主義者
pessimistic_prompt = ChatPromptTemplate.from_messages(
    messages=[
        (
            "system",
            "あなたは悲観主義者です。ユーザーの入力に対して悲観的な意見をください。",
        ),
        ("human", "{topic}"),
    ]
)


# LCELによる並列実行 -----------------------------------------

# チェーン構築
# --- 楽観主義者/悲観主義者のパーツ
optimistic_chain = optimistic_prompt | model | output_parser
pessimistic_chain = pessimistic_prompt | model | output_parser

# チェーン構造化
# --- 並列的に問い合わせる（意見集約などは行っていない）
parallel_chain = RunnableParallel(
    steps__={
        "optimistic_opinion": optimistic_chain,
        "pessimistic_opinion": pessimistic_chain,
    }
)

# 問い合わせ
output = parallel_chain.invoke(input={"topic": "生成AIの進化について"})

# 結果確認
pprint.pprint(output)
