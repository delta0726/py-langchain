"""
Title   : やさしく学ぶLLMエージェント
Chapter : 2 エージェント作成のための基礎知識
Section : 2 LangChain入門
Theme   : テーブル作成アプリケーション
Date    : 2025/06/25
Page    : P48-51
"""

# ＜ポイント＞
# - 生成AIでスキーマを定義して構造化データを出力させる
# - CSV出力の自作関数をLLMに密結合して確実にCSV保存させる


import csv
import os

from langchain_core.tools import tool
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.prompts import PromptTemplate
from langchain_openai.chat_models import ChatOpenAI


# 入力スキーマ定義
class CSVSaveToolInput(BaseModel):
    filename: str = Field(description="ファイル名")
    csv_text: str = Field(description="CSVのテキスト")


# 関数定義
# --- CSV保存ツール
@tool("csv-save-tool", args_schema=CSVSaveToolInput)
def csv_save(filename: str, csv_text: str) -> bool:
    """CSVテキストを 'csv/' フォルダに保存する"""
    try:
        rows = list(csv.reader(csv_text.splitlines()))
    except Exception:
        return False

    path = os.path.join("csv", filename)
    with open(path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(rows)

    return True


# 関数定義
# --- 引数の抽出
def get_tool_args(x):
    return x.tool_calls[0]


# LLMにツールを紐づける
llm = ChatOpenAI(model="gpt-4o-mini")
tools = [csv_save]
llm_with_tool = llm.bind_tools(tools=tools, tool_choice="csv-save-tool")


# プロンプトの定義
prompt = PromptTemplate.from_template(
    template="""
    {user_input}
    結果は CSV ファイルに保存してください。
    ただし、ファイル名は上記の内容から適切に決定してください。
    """
)


# Runnable の定義
runnable = prompt | llm_with_tool | get_tool_args | csv_save


# 実行例
user_input = """
フィボナッチ数列の番号と値を10番目まで表にまとめて、
CSVファイルに保存してください。
"""

# 問い合わせ
response = runnable.invoke({"user_input": user_input})
print(response)
