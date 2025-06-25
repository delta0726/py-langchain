"""
Title   : Langchain完全入門
Section : 2 Language Models
Theme   : テンプレートを活用した問い合わせ
Date    : 2025/04/25
Page    : P62
"""

from langchain import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage


# 言語モデル構築
chat = ChatOpenAI(model="gpt-4o-mini")

# プロンプト構築
prompt = PromptTemplate(
    template="{product}はどこの会社が開発した製品ですか？",
    input_variables=["product"],
)

# 問い合わせ
# --- テンプレートに基づいて質問
result = chat(
    [
        HumanMessage(content=prompt.format(product="iPhone")),
    ]
)

# 確認
print(result.content)
