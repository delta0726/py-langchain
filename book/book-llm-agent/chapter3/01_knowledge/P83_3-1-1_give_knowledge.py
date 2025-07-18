"""
Title   : やさしく学ぶLLMエージェント
Chapter : 3 エージェント
Section : 1 LLLMに知識を与える
Theme   : Contextから知識を与える
Date    : 2025/07/18
Page    : P82-85
"""

# ＜概要＞
# - Contextで与えた背景知識をもとに回答させる
# - LLMの持つ｢知識｣と｢推論能力｣のうち後者のみを使っている
# - プロンプトに背景知識を入れ込むため、大規模になると柔軟性や透明性に欠ける
# - RAGよりも手間がかからない手軽な方法と言える

from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage
from langchain_core.prompts import ChatPromptTemplate


# 準備 ------------------------------------------------------------

# モデル定義
model = ChatOpenAI(model="gpt-4o-mini")


# 単一メッセージで回答させる --------------------------------------------

# ＜ポイント＞
# - LLMはプロンプトから熊童子が妖怪か植物かが判定できない
# - 結果として可能性の高い妖怪の方を回答している


# 問い合わせ
simple_result = model.invoke(
    input=[HumanMessage(content="熊童子について教えてください。")]
)

# 結果確認
print(simple_result.content)


# 背景知識を前提に回答させる --------------------------------------------

# プロンプト定義
# --- contextをもとにquestionに回答することを明記
prompt_template = """
Answer this question using the provided context only.

{question}

Context:
{context}
"""

# プロンプト定義
# --- 質問事項
question = "熊童子について教えてください。"

# 背景知識
context = """
熊童子はベンケイソウ科コチレドン属の多肉植物です。
葉に丸みや厚みがあり、先端には爪のような突起があることから「熊の手」という
愛称で人気を集めています。
花はオレンジ色のベル型の花を咲かせることがあります。
"""


# プロンプト・テンプレート作成
prompt = ChatPromptTemplate.from_messages(messages=[("human", prompt_template)])

# チェイン構築
chain = prompt | model

# 問い合わせ
response = chain.invoke(input={"context": context, "question": question})

# 結果確認
print(response.content)
