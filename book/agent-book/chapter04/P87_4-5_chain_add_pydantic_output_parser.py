"""
Title   : LangChainとLangGraphによるRAG・AIエージェント実践入門
Chapter : 4 LangChainの基礎
Section : 5 Chain - LangChain Expression Language(LCEL)の概要
Theme   : PydanticOutputParserを使う連鎖
Date    : 2025/05/16
Page    : P87
"""

# ＜ポイント＞
# - 出力が期待される形式に合っているかを検証してPydanticモデルに変換する
# - PydanticModelとは構造化データの検証/型付けを簡単に行うためのクラス
# - JSONで結果を受け取る際にデータ型や出力形式をチェックする（エラーも返す）
# - 出力パーサーで出力形式を決定してからプロンプトに出力形式を読み込ませる

from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI


# 出力パーサーの構築 ---------------------------------------


# Pydanticモデルの定義
# --- データ構造の定義
class Recipe(BaseModel):
    ingredients: list[str] = Field(description="ingredients of the dish")
    steps: list[str] = Field(description="steps to make the dish")


# 出力パーサーの定義
# --- Pydanticモデルを追加
output_parser = PydanticOutputParser(pydantic_object=Recipe)


# プロンプトの構築 ---------------------------------------

# プロンプト定義
prompt = ChatPromptTemplate.from_messages(
    messages=[
        (
            "system",
            "ユーザーが入力した料理のレシピを考えてください。\n\n{format_instructions}",
        ),
        ("human", "{dish}"),
    ]
)

# フォーマット指定の追加
# --- 出力パーサーのフォーマット指定の読み込み
prompt_with_format_instructions = prompt.partial(
    format_instructions=output_parser.get_format_instructions()
)


# 問い合わせ --------------------------------------------

# モデル定義
model = ChatOpenAI(model="gpt-4o-mini", temperature=0).bind(
    response_format={"type": "json_object"}
)

# チェイン構築
chain = prompt_with_format_instructions | model | output_parser

# 問い合わせ
recipe = chain.invoke(input={"dish": "カレー"})

# 結果確認
print(type(recipe))
print(recipe)
