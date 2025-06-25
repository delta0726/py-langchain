"""
Title   : LangChainとLangGraphによるRAG・AIエージェント実践入門
Chapter : 5 LangeChain Expression Language(LCEL)の徹底解説
Section : RunnableLambda（任意の関数をRunnableにする）
Theme   : 独自関数をストリーミングに対応させたい場合
Date    : 2025/05/25
Page    : P114
"""

# ＜概要＞
# - RunnableLambdaを出力結果に対して適用するためストリーミング形式とは相いれない
# - 出力結果が出そろってから関数を適用するので、ストリーミング形式とならない
# - ただし、関数自体をジェネレータ関数として実装すことで対応可能となる

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from typing import Iterator


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
def upper(input_stream: Iterator[str]) -> Iterator[str]:
    for text in input_stream:
        yield text.upper()


# LCELによる実行 -----------------------------------------

# チェーン構築
chain = prompt | model | StrOutputParser() | upper

# ストリーミング実行
for chunk in chain.stream({"input": "Hello!"}):
    print(chunk, end="", flush=True)
