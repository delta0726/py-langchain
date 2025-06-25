"""
Title   : Langchain完全入門
Section : 4 Memory - 過去の対話を短期/長期で記憶する
Theme   : 会話履歴を持たない単独の会話
Date    : 2025/04/27
Page    : P150
"""

from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage


# 言語モデルの定義
chat = ChatOpenAI(model="gpt-4o-mini")

# 問い合わせ
# --- 会話履歴のリスト(最低でもHumanMessageが1つ必要)
result = chat(
    [
        HumanMessage(content="茶碗蒸しを作るのに必要な食材を教えて"),
    ]
)

# 結果確認
print(result.content)
