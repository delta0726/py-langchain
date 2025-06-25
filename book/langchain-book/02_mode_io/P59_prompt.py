"""
Title   : Langchain完全入門
Section : 2 Language Models
Theme   : テンプレートの利用
Date    : 2025/04/25
Page    : P59
"""

from langchain import PromptTemplate


# インスタンス作成
# --- プロンプトをテンプレート化して質問内容を引数でコントロールする
prompt = PromptTemplate(
    template="{product}はどこの会社が開発した製品ですか？", input_variables=["product"]
)

# プロンプト出力
print(prompt.format(product="iPhone"))
print(prompt.format(product="Xperia"))
