"""
Title   : LangChainとLangGraphによるRAG・AIエージェント実践入門
Chapter : 4 LangChainの基礎
Section : 5 Chain - LangChain Expression Language(LCEL)の概要
Theme   : promptとmodelの連鎖
Date    : 2025/05/16
Page    : P87
"""

# ＜ポイント＞
# - 実際にLLMでJSON形式で構造化データを取得する際はwith_structured_outputを使う
# - PydanticOutputParserを直接使うよりも簡素に記述することができる
# - with_structured_outputは構造化出力のためのモデルに適用するヘルパー関数(メソッド)
# - プロンプトに構造データの定義を与えずモデルにメソッドとして指示している

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field


# Pydanticモデルの定義
class Recipe(BaseModel):
    ingredients: list[str] = Field(description="ingredients of the dish")
    steps: list[str] = Field(description="steps to make the dish")


# プロンプト定義
prompt = ChatPromptTemplate.from_messages(
    messages=[
        ("system", "ユーザーが入力した料理のレシピを考えてください。"),
        ("human", "{dish}"),
    ]
)

# モデル定義
model = ChatOpenAI(model="gpt-4o-mini")

# チェイン構築
chain = prompt | model.with_structured_output(schema=Recipe)

# 問い合わせ
recipe = chain.invoke(input={"dish": "カレー"})

# 結果確認
print(type(recipe))
print(recipe)
