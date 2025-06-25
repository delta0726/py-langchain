"""
Title   : Langchain完全入門
Section : 2 Language Models
Theme   : AIMessageの役割
Date    : 2025/04/25
Page    : P57
"""

from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, AIMessage


# インスタンス構築
chat = ChatOpenAI(
    model_name="gpt-4o-mini",
)

# 問い合わせ
# --- メッセージは人間/AI/システムの3種類がある
# --- AIMessage()はAIが過去に回答した内容を記録している
# --- content={*}はプレースホルダで｢こういう内容が入ってくる｣という表題のようなもの
result = chat(
    messages=[
        HumanMessage(content="茶碗蒸しの作り方を教えて"),
        AIMessage(content="{ChatModelからの返答である茶わん蒸しの作り方}"),
        HumanMessage(content="英語に翻訳して"),
    ]
)

# 回答
result.content
