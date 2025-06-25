"""
Title   : Langchain完全入門
Section : 2 Language Models
Theme   : 文章の続きを予測する（対話ではない）
Date    : 2025/04/25
Page    : P70
"""

from langchain.llms import OpenAI

# インスタンス構築
# --- 高価なモデルなので実行しない
# llm = OpenAI(model="gpt-3.5-turbo-instruct")
llm = OpenAI(model="not-available")

# 問い合わせ
# --- chat()で質問することが多いが、今回はllmインスタンスに直接入力する
# --- 与えたテキストの続きを生成させる
# --- stop引数で終点を指定することが可能（今回は｢。｣が出たら終了）
result = llm(
    "美味しいラーメンを",
    stop="。",
)

# 回答
print(result)
