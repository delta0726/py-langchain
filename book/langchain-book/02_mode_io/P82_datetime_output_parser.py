"""
Title   : Langchain完全入門
Section : 2 Language Models
Theme   : 出力データを構造化する
Date    : 2025/04/26
Page    : P82
"""

from langchain import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.output_parsers import DatetimeOutputParser
from langchain.schema import HumanMessage


# インスタンス構築
# --- 大規模言語モデル
# --- 出力パーサー(日付出力)
chat = ChatOpenAI(model="gpt-4o-mini")
output_parser = DatetimeOutputParser()

# プロンプト定義
prompt = PromptTemplate.from_template("{product}のリリース日を教えて")

# 問い合わせ
# --- プロンプトの後に出力パーサーのフォーマットを表示
result = chat(
    [
        HumanMessage(content=prompt.format(product="iPhone8")),
        HumanMessage(content=output_parser.get_format_instructions()),
    ]
)

# 出力結果の取得
# --- 出力データを日付型に変換して取得
print(result.content)
output = output_parser.parse(result.content)

# 出力確認
print(output)

# 参考：出力パーサーの動作
# --- プロンプトで日付変換することを指示している
print(output_parser.get_format_instructions())
