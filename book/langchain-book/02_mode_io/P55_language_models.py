"""
Title   : Langchain完全入門
Section : 2 Language Models
Theme   : HumanMessageの役割
Date    : 2025/04/25
Page    : P55
"""

from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage


# インスタンス構築
chat = ChatOpenAI(
    model_name="gpt-4o-mini",  
)

# 問い合わせ
# --- メッセージは人間/AI/システムの3種類がある
# --- HumanMessage()は人間からのメッセージであることを示す
result = chat(
    messages=[
        HumanMessage(content="こんにちは！"),
    ]
)

# 回答
result.content