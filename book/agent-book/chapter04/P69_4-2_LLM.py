"""
Title   : LangChainとLangGraphによるRAG・AIエージェント実践入門
Chapter : 4 LangChainの基礎
Section : 2 LLM/Chat Model
Theme   : LLM
Date    : 2025/05/14
Page    : P69
"""

# ＜ポイント＞
# - LangChainの｢LLM｣は1つのテキスト入力に対して、1つのテキスト出力を返す
# - temperature引数が大きいほどランダム性が高く、低いほど安定的な回答を得られる

from langchain_openai import OpenAI


# LLMの定義
model = OpenAI(model="gpt-3.5-turbo-instruct", temperature=0)

# 問い合わせ
ai_message = model.invoke(input="こんにちは")

# 結果表示
print(ai_message)
