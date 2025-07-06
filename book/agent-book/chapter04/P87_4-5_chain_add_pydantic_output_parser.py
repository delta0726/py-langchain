"""
Title   : LangChainとLangGraphによるRAG・AIエージェント実践入門
Chapter : 4 LangChainの基礎
Section : 5 Chain - LangChain Expression Language(LCEL)の概要
Theme   : PydanticOutputParserを使う連鎖
Date    : 2025/07/06
Page    : P87-88
"""


# ＜概要＞
# - PydanticOutputParserを使用することで出力パーサーの出力形式を指示
# - プロンプトに｢以下の形式で出力してください｣という趣旨の指示を入れている
# - LLMモデルに出力結果がJSONになるように強制している
# - プロンプト/モデル/出力パーサーのすべてのステップで出力形式を指示している

from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI


# 出力パーサーの構築 ---------------------------------------

# ＜ポイント＞
# - PydanticOutputParserで出力形式を指定した出力パーサーを定義


# Pydanticモデルの定義
# --- データ構造の定義
class Recipe(BaseModel):
    ingredients: list[str] = Field(description="ingredients of the dish")
    steps: list[str] = Field(description="steps to make the dish")


# 出力パーサーの定義
# --- Pydanticモデルを追加
output_parser = PydanticOutputParser(pydantic_object=Recipe)


# プロンプトの構築 ---------------------------------------

# ＜ポイント＞
# - 出力パーサーの出力形式をプロンプトに埋め込んでいる
# - partial()でプロンプトの一部のプレースホルダーのみを更新している
# - get_format_instructions()は出力形式を文字列に変換する機能を持つ
#   --- PydanticOutputParser、JsonOutputParser、EnumOutputParserで利用可能

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
# --- partial()は一部のプレースホルダーのみを更新する
# --- 出力パーサーのフォーマット指定の読み込み
prompt_with_format_instructions = prompt.partial(
    format_instructions=output_parser.get_format_instructions()
)

# 参考：指定したフォーマット
output_parser.get_format_instructions()


# モデル --------------------------------------------

# ＜ポイント＞
# - bind()はRunnableインターフェースに追加する設定用のメソッド
# - response_format引数で出力形式を強制することができる（今回はJSONオブジェクト）
# - モデル側で出力をコントロールすることでPydanticOutputParserの結果を安定させる


# モデル定義
model = ChatOpenAI(model="gpt-4o-mini", temperature=0).bind(
    response_format={"type": "json_object"}
)


# 問い合わせ --------------------------------------------

# チェイン構築
chain = prompt_with_format_instructions | model | output_parser

# 問い合わせ
recipe = chain.invoke(input={"dish": "カレー"})

# 結果確認
print(type(recipe))
print(recipe)
