"""
Title   : Langchain完全入門
Section : 2 Language Models
Theme   : 出力形式を定義した上で、結果が不適切なら修正/補正を行う
Date    : 2025/04/26
Page    : P86
"""

from langchain.chat_models import ChatOpenAI
from langchain.output_parsers import OutputFixingParser  # ←OutputFixingParserを追加
from langchain.output_parsers import PydanticOutputParser
from langchain.schema import HumanMessage
from pydantic import BaseModel, Field, field_validator


# インスタンス構築
# --- ChatOpenAIのインスタンスを作成
chat = ChatOpenAI()


# クラス定義
class Smartphone(BaseModel):
    # 出力形式
    release_date: str = Field(description="スマートフォンの発売日")
    screen_inches: float = Field(description="スマートフォンの画面サイズ(インチ)")
    os_installed: str = Field(description="スマートフォンにインストールされているOS")
    model_name: str = Field(description="スマートフォンのモデル名")

    # データ検証
    @field_validator("screen_inches")
    @classmethod
    def validate_screen_inches(cls, field):
        if field <= 0:
            raise ValueError("Screen inches must be a positive number")
        return field


# パーサー定義
# --- Startphoneクラスでエラーが出た際にエラー修正するように試みる
# --- 修正に使用する言語モデルを設定ydanticOutputParserを利用
# --- API やモデルが出力した内容を整形し、その過程で不完全/不正な場合修正を行う仕組み
parser = OutputFixingParser.from_llm(
    parser=PydanticOutputParser(pydantic_object=Smartphone), 
    llm=chat
)

# 問い合わせ
result = chat(
    [
        HumanMessage(content="Androidでリリースしたスマートフォンを1個挙げて"),
        HumanMessage(content=parser.get_format_instructions()),
    ]
)


# 結果取得
# --- 単純な質問なので正常に回答できていることを確認
# --- その上でチェックを行う
print(result.content)
parsed_result = parser.parse(result.content)

# 確認
print(f"""
      モデル名: {parsed_result.model_name}
      発売日: {parsed_result.release_date}
      画面サイズ(インチ): {parsed_result.screen_inches}
      インストールされているOS: {parsed_result.os_installed}
      """)
