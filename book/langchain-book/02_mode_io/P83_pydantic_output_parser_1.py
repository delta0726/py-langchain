"""
Title   : Langchain完全入門
Section : 2 Language Models
Theme   : 出力データの構造を定義して出力検証も行う
Date    : 2025/04/26
Page    : P83
"""

from langchain.chat_models import ChatOpenAI
from langchain.output_parsers import PydanticOutputParser
from langchain.schema import HumanMessage
from pydantic import BaseModel, Field, field_validator


# インスタンス構築
chat = ChatOpenAI()


# 出力形式をクラスで定義
# --- Pydanticモデルはデータ検証を行うためのクラス（BaseModelを継承）
# --- 型ヒントで変数定義した上でメタデータ(追加情報)を設定している
# --- @field_validatorはクラスに適用されるため、@classmethodを使ってクラスを受け取れるようにしておく
class Smartphone(BaseModel):
    # 必要項目の列挙（型指定）
    release_date: str = Field(description="スマートフォンの発売日")
    screen_inches: float = Field(description="スマートフォンの画面サイズ(インチ)")
    os_installed: str = Field(description="スマートフォンにインストールされているOS")
    model_name: str = Field(description="スマートフォンのモデル名")

    @field_validator("screen_inches")
    @classmethod
    def validate_screen_inches(cls, field):
        # ← screen_inchesが0以下の場合はエラーを返す
        if field <= 0:
            raise ValueError("Screen inches must be a positive number")
        return field


# パーサー定義
# --- PydanticOutputParserをSmartPhoneモデルで初期化する
parser = PydanticOutputParser(pydantic_object=Smartphone)

# 問い合わせ
# --- 質問内容
# --- 回答フォーマットを指定する
result = chat(
    [
        HumanMessage(content="Androidでリリースしたスマートフォンを1個挙げて"),
        HumanMessage(content=parser.get_format_instructions()),
    ]
)

# 結果取得
# --- PydanticOutputParserを使って、文章をパースする
# --- validate_screen_inches()のチェックなどを行う
parsed_result = parser.parse(result.content)


# 確認
print(f"""
      モデル名: {parsed_result.model_name}
      発売日: {parsed_result.release_date}
      画面サイズ(インチ): {parsed_result.screen_inches}
      インストールされているOS: {parsed_result.os_installed}
      """)

# ＜検証＞
# - 回答フォーマット
print(parser.get_format_instructions())
