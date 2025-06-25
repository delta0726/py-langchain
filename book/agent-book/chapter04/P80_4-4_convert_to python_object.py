"""
Title   : LangChainとLangGraphによるRAG・AIエージェント実践入門
Chapter : 4 LangChainの基礎
Section : 4 Output parser
Theme   : PydanticOutputParserを使ったPythonオブジェクトへの変換
Date    : 2025/05/16
Page    : P80
"""

# ＜ポイント＞
# - Pydanticはデータの入れ物として使うことができるクラス
# - PydanticOutputParserはJSONフォーマット専用の出力パーサー

from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate


# プロンプトの作成 ----------------------------------------------------


# クラス定義
class Recipe(BaseModel):
    ingredients: list[str] = Field(description="ingredients of the dish")
    steps: list[str] = Field(description="steps to make the dish")


# 出力パーサーを作成
# --- PydanticOutputParserはJSONフォーマットの出力例をLLMに伝える
# --- 具体的にはJSONフォーマットの例を示すプロンプトを出力する
output_parser = PydanticOutputParser(pydantic_object=Recipe)
format_instructions = output_parser.get_format_instructions()
print(format_instructions)

# プロンプト・テンプレートの作成
prompt = ChatPromptTemplate.from_messages(
    messages=[
        (
            "system",
            "ユーザーが入力した料理のレシピを考えてください。\n\n{format_instructions}",
        ),
        ("human", "{dish}"),
    ]
)

# プロンプト・テンプレートの修正
# --- 出力パーサーをプロンプトに追加
prompt_with_format_instructions = prompt.partial(
    format_instructions=format_instructions
)

# プロンプトの呼び出し
prompt_value = prompt_with_format_instructions.invoke({"dish": "カレー"})
print("=== role: system ===")
print(prompt_value.messages[0].content)
print("=== role: user ===")
print(prompt_value.messages[1].content)


# 問い合わせ ----------------------------------------------------

# LLMの定義
model = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# 問い合わせ
ai_message = model.invoke(input=prompt_value)

# 結果確認
# --- テンプレートと出力パーサーに基づいて出力されている
print(ai_message.content)

# 出力パーサーで実行
# --- クラスとして出力されている
recipe = output_parser.invoke(input=ai_message)
print(type(recipe))
print(recipe)
