"""
Title   : LangChainとLangGraphによるRAG・AIエージェント実践入門
Chapter : 4 LangChainの基礎
Section : 5 Chain - LangChain Expression Language(LCEL)の概要
Theme   : strOutputParserを連鎖に追加
Date    : 2025/06/02
Page    : P86
"""

# ＜ポイント＞
# - ChainにstrOutputParserを追加して問い合わせ結果をテキストで直接抽出する
# - プロンプト/モデル/出力パーサーのセットがChain構造の基本
# - Chainを構築する場合は出力形式に意図があるため出力パーサーの定義は必須

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser


# プロンプト定義
prompt = ChatPromptTemplate.from_messages(
    messages=[
        ("system", "ユーザーが入力した料理のレシピを考えてください。"),
        ("human", "{dish}"),
    ]
)

# パーツ定義
model = ChatOpenAI(model_name="gpt-4o-mini", temperature=0)
output_parser = StrOutputParser()

# チェイン構築
# --- strOutputParserを追加
chain = prompt | model | output_parser

# 問い合わせ
output = chain.invoke(input={"dish": "カレー"})

# 結果確認
print(output)
