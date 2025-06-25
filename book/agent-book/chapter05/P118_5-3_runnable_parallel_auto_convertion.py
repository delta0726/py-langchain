"""
Title   : LangChainとLangGraphによるRAG・AIエージェント実践入門
Chapter : 5 LangeChain Expression Language(LCEL)の徹底解説
Section : RunnableParallel（複数のRunnableを並列につなげる）
Theme   : RunnableParallelを明示的に使用せず自動変換させる
Date    : 2025/06/04
Page    : P118
"""

# ＜概要＞
# - RunnableParallelを明示的に使用しなくても自動変換される
# - 実務では明示的に記述しておいた方が意図がつたわりやすそう（省略による簡素さも魅力的）

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI


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

# プロンプト
# --- 意見のとりまとめ
synthesize_prompt = ChatPromptTemplate.from_messages(
    messages=[
        ("system", "あなたは客観的AIです。2つの意見をまとめてください。"),
        (
            "human",
            "楽観的意見: {optimistic_opinion}\n悲観的意見: {pessimistic_opinion}",
        ),
    ]
)

# LCELによる並列実行 -----------------------------------------

# チェーン構築
# --- 楽観主義者/悲観主義者/集約者のパーツ
optimistic_chain = optimistic_prompt | model | output_parser
pessimistic_chain = pessimistic_prompt | model | output_parser
aggregate_chain = synthesize_prompt | model | output_parser

# チェーン構造化
# --- RunnableParallelを使用していない（自動変換される）
synthesize_chain = {
    "optimistic_opinion": optimistic_chain,
    "pessimistic_opinion": pessimistic_chain,
} | aggregate_chain

# 問い合わせ
output = synthesize_chain.invoke(input={"topic": "生成AIの進化について"})

# 結果確認
print(output)
