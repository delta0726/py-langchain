"""
Title   : Langchain完全入門
Section : 2 Language Models
Theme   : SystemMessageの役割
Date    : 2025/04/25
Page    : P58
"""

from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage


# インスタンス構築
chat = ChatOpenAI(
    model_name="gpt-4o-mini",
)

# 問い合わせ
# --- SystemMessage()は会話の最初に会話前提を明示的に指定する役割を持つ
# --- HumanMessage()で記述してもよさそうだが、指示の遵守は言語モデルにゆだねられる
result = chat(
    messages=[
        SystemMessage(
            content="あなたは親しい友人です。敬語を使わずにフランクに話してください。"
        ),
        HumanMessage(content="こんにちは"),
    ]
)

# 回答
result.content
