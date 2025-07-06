"""
Title   : LangChainとLangGraphによるRAG・AIエージェント実践入門
Chapter : 4 LangChainの基礎
Section : 5 Chain - LangChain Expression Language(LCEL)の概要
Theme   : promptとmodelの連鎖
Date    : 2025/05/16
Page    : P87
"""

# ＜概要＞
# - PydanticOutputParserよりもwith_structured_output()を使うことが推奨されている
# - with_structured_output()は、モデルに出力パーサーを密統合したもの
# - 構造的なアウトプットを期待する場合のベストプラクティス

# ＜推奨理由＞
# - LangChainチームは以下の理由からwith_structured_output()の利用を推奨している
#   --- モデル自体に構造化出力の責任を持たせることで、上流でのコントロールが促進される
#   --- model.bind(response_format={"type": "json_object"})を自動で行うことによる安全性の向上
#   --- 密結合は再利用性を低下させるが、タスクが固定的であれば簡素化につながる
#   --- プロンプトで出力フォーマットの指定をする必要がなくなる

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field


# Pydanticモデルの定義 --------------------------------------

# ＜ポイント＞
# - BaseModelを継承して出力形式を定義
# - PydanticOutputParserによる出力パーサーの定義は必要ない
class Recipe(BaseModel):
    ingredients: list[str] = Field(description="ingredients of the dish")
    steps: list[str] = Field(description="steps to make the dish")


# プロンプト定義 -------------------------------------------

# ＜ポイント＞
# - プロンプトにoutput_parser.get_format_instructions()を指定していない
# - これは、内部的にwith_structured_output()が内部的に指示しているため

prompt = ChatPromptTemplate.from_messages(
    messages=[
        ("system", "ユーザーが入力した料理のレシピを考えてください。"),
        ("human", "{dish}"),
    ]
)


# モデル定義 ----------------------------------------------

# ＜ポイント＞
# - with_structured_output()でモデルと出力パーサーを密結合

model = ChatOpenAI(model="gpt-4o-mini").with_structured_output(schema=Recipe)


# 問い合わせ ----------------------------------------------

# チェイン構築
chain = prompt | model

# 問い合わせ
recipe = chain.invoke(input={"dish": "カレー"})

# 結果確認
print(type(recipe))
print(recipe)
