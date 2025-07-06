"""
Title   : LangChainとLangGraphによるRAG・AIエージェント実践入門
Chapter : 5 LangeChain Expression Language(LCEL)の徹底解説
Section : LCELの｢|｣でさまざまなRunnableを連鎖させる
Theme   : チェイン同士をパイプで連結する
Date    : 2025/06/04
Page    : P108-109
"""

# ＜概要＞
# - チェイン同士もパイプで結合することができ、新たなチェインを構築することができる
# - 単一のChainと同様にinvoke()などのメソッドを使用することができる
# - この性質により構造的にな問い合わせ(CoTなど)が実現可能となる

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI


# コンポーネント定義 ------------------------------------------

# LLMモデル
model = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# 出力パーサー
output_parser = StrOutputParser()

# プロンプト
# --- Chain of Thought (CoT)
cot_prompt = ChatPromptTemplate.from_messages(
    messages=[
        ("system", "ユーザーの質問にステップバイステップで回答してください。"),
        ("human", "{question}"),
    ]
)

# プロンプト
# --- CoTの結論抽出
summarize_prompt = ChatPromptTemplate.from_messages(
    messages=[
        ("system", "ステップバイステップで考えた回答から結論だけ抽出してください。"),
        ("human", "{text}"),
    ]
)


# LCELによるCotプロセス -----------------------------------------

# チェーン構築
cot_chain = cot_prompt | model | output_parser
summarize_chain = summarize_prompt | model | output_parser

# チェイン結合
# --- cot_chainのアウトプットは{text}として渡される
cot_summarize_chain = cot_chain | summarize_chain

# 問い合わせ
output = cot_summarize_chain.invoke(input={"question": "10 + 2 * 3"})

# 結果確認
print(output)
