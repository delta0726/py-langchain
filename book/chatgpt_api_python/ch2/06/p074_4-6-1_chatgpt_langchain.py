"""
Title   : Chatgpt API & Python
Section : 2 開発環境やAPIの準備をしよう
Theme   : Chatgpt APIの接続テスト（langchain）
Date    : 2025/04/30
Page    : P74
"""

from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage

# LLMの定義
chat = ChatOpenAI(model_name="gpt-4o-mini")

# プロンプト
messages = [
    HumanMessage(content="Pythonについて教えてください"),
]

# 問い合わせ
response = chat(messages)

# 結果確認
print(response.content)