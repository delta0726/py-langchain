"""
Title   : LangChainとLangGraphによるRAG・AIエージェント実践入門
Chapter : 5 LangeChain Expression Language(LCEL)の徹底解説
Section : RunnableParallel（複数のRunnableを並列につなげる）
Theme   : RunnableLambdaとの組み合わせ（itemgetterを使う例）
Date    : 2025/06/04
Page    : P119
"""

# ＜概要＞
# - itemgetterを使うとプロンプトから明示的にトピックを与えることができる
# - 意見集約プロセスにもトピックを知らせることができる
# - itemgetterを使わないと集約プロセスはトピックを知らず文章だけを見て集約作業をする

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from operator import itemgetter


# コンポーネント定義 ------------------------------------------

# ＜ポイント＞
# - これまでと同様にプロンプトには{topic}がある


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
        (
            "system",
            "あなたは客観的AIです。{topic}について2つの意見をまとめてください。",
        ),
        (
            "human",
            "楽観的意見: {optimistic_opinion}\n悲観的意見: {pessimistic_opinion}",
        ),
    ]
)


# itemgetterの動作確認 ---------------------------

# インスタンス生成
topic_getter = itemgetter("topic")
topic = topic_getter({"topic": "生成AIの進化について"})

# 確認
print(topic)
print(type(topic))


# LCELによる並列実行 -----------------------------------------

# チェーン構築（パーツ）
# --- 楽観主義者/悲観主義者/集約者のパーツ
optimistic_chain = optimistic_prompt | model | output_parser
pessimistic_chain = pessimistic_prompt | model | output_parser
aggregate_chain = synthesize_prompt | model | output_parser


# チェーン構造化
# --- RunnableParallelを使用していない（自動変換される）
# --- aggregate_chainにtopicを明示的に渡している
synthesize_chain = {
    "optimistic_opinion": optimistic_chain,
    "pessimistic_opinion": pessimistic_chain,
    "topic": itemgetter("topic"),
} | aggregate_chain

# 問い合わせ
output = synthesize_chain.invoke(input={"topic": "生成AIの進化について"})
print(output)
