"""
Title   : LangChainとLangGraphによるRAG・AIエージェント実践入門
Chapter : 4 LangChainの基礎
Section : 5 Chain - LangChain Expression Language(LCEL)の概要
Theme   : promptとmodelの連鎖
Date    : 2025/06/02
Page    : P85
"""

# ＜ポイント＞
# - LCELはLangChainの処理をチェーン形式でパイプ(|)でつなげて記述する記法
# - 一連のワークフローをChainオブジェクトとしてパッケージ化することができる
# - Chainオブジェクトに対して問い合わせを実行する

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI


# プロンプト定義
prompt = ChatPromptTemplate.from_messages(
    messages=[
        ("system", "ユーザーが入力した料理のレシピを考えてください。"),
        ("human", "{dish}"),
    ]
)

# モデル定義
model = ChatOpenAI(model_name="gpt-4o-mini", temperature=0)

# Chain構築
chain = prompt | model

# 問い合わせ
# --- Chainオブジェクトに対して問い合わせを行うことができる
ai_message = chain.invoke(input={"dish": "カレー"})

# 結果確認
print(ai_message.content)
