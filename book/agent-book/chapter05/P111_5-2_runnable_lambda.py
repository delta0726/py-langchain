"""
Title   : LangChainとLangGraphによるRAG・AIエージェント実践入門
Chapter : 5 LangeChain Expression Language(LCEL)の徹底解説
Section : RunnableLambda（任意の関数をRunnableにする）
Theme   : 前処理/後処理/条件分岐のための関数をChainに加える
Date    : 2025/05/25
Page    : P111
"""

# ＜概要＞
# - 任意の関数をRunnableにしてChainで利用可能にする
# - 前処理/後処理に加えて条件分岐やログ出力にも役立つ
# - より複雑な処理をしたい場合はRunnableを継承した独自クラスを作って対応する

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnableLambda


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


# LCELによる実行 -----------------------------------------

# チェーン構築
# --- 出力結果に対して関数を適用（RunnableLambdaでラップ）
chain = prompt | model | output_parser | RunnableLambda(func=upper)

# 問い合わせ
ai_message = chain.invoke(input={"input": "Hello!"})

# 結果確認
# --- 大文字に変換されている
print(ai_message)
