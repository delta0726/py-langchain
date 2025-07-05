"""
Title   : LangChainとLangGraphによるRAG・AIエージェント実践入門
Chapter : 4 LangChainの基礎
Section : 3 Prompt Template
Theme   : プロンプト・テンプレート
Date    : 2025/05/14
Page    : P74-75
"""

# ＜ポイント＞
# - ChatPromptTemplateはPromptTemplateをRole別のチャット形式に対応させたもの
#   --- system、human、assistantなどのメッセージをテンプレート化できる
#   --- ロールごとに会話を指定してもプレースホルダーの設定は可能

from langchain_core.prompts import ChatPromptTemplate


# テンプレート定義
# --- Role別に会話をテンプレート化してもプレースホルダーの指定は可能
prompt = ChatPromptTemplate.from_messages(
    messages=[
        ("system", "ユーザーが入力した料理のレシピを考えてください。"),
        ("human", "{dish}"),
    ]
)

# プロンプト作成
prompt_value = prompt.invoke(input={"dish": "カレー"})

# 結果表示
print(prompt_value)
