"""
Title   : Langchain完全入門
Section : 2 Language Models
Theme   : 問い合わせの出力形式のコントロール
Date    : 2025/04/25
Page    : P65
"""

from langchain.chat_models import ChatOpenAI
from langchain.output_parsers import CommaSeparatedListOutputParser
from langchain.schema import HumanMessage


# インスタンス構築
# --- 出力パーサー（カンマ区切りデータをリスト化）
# --- 言語モデル
output_parser = CommaSeparatedListOutputParser()
chat = ChatOpenAI(model="gpt-4o-mini")

# 事前確認
# --- 出力パーサーのフォーマット確認
# --- 出力形式はインスタンス定義の段階で決定している（カンマ区切りデータをリスト化）
print(output_parser.get_format_instructions())
output_parser.get_format_instructions

# 問い合わせ
# --- 1回で質問しても同様の回答が得れそうだが、別けることでシナリオの柔軟性が増す
# --- プログラムとしても明示性が高まる
result = chat(
    [
        HumanMessage(content="Appleが開発した代表的な製品を3つ教えてください"),
        HumanMessage(content=output_parser.get_format_instructions()),
    ]
)

# 結果取得
# --- 出力結果を解析してリスト形式に変換する
output = output_parser.parse(result.content)
print(result.content)
print(output)

# 確認
for item in output:
    print("代表的な製品 => " + item)
