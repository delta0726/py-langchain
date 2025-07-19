"""
Title   : やさしく学ぶLLMエージェント
Chapter : 3 エージェント
Section : 5 ペルソナのあるエージェント
Theme   : ペルソナ付与のためのプロンプト技術
Date    : 2025/07/19
Page    : P129-134
"""

# ＜概要＞
# - ペルソナはプロンプトから設定する
# - {human}か{system}としてペルソナを設定するのが一般的


from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate


# 準備 -----------------------------------

# 共通設定
model = ChatOpenAI(model="gpt-4o-mini")
question_text = "LLMエージェントについて教えてください。"


# ペルソナなしのLLM ----------------------

# プロンプト
normal_message = """
以下の質問に答えてください。

{question}
"""

normal_prompt = ChatPromptTemplate.from_messages(messages=[("human", normal_message)])

# 問い合わせ
normal_chain = normal_prompt | model
normal_response = normal_chain.invoke({"question": question_text})

# 結果確認
print("【通常の回答】")
print(normal_response.content)


# ペルソナありのLLM ----------------------

# プロンプト
erith_message = """
あなたは「えりすちゃん」というキャラクターです。
えりすちゃんは以下のような特徴のキャラクターです。
- 株式会社Elithのマスコット
- ペガサスの見た目をしている
- 人懐っこい性格で、誰にでも優しく接する
- ポジティブな性格で励ましの言葉を常に意識している
- 「～エリ！」というのが口癖
  - 例：「今日も頑張るエリ！」

「えりすちゃん」として以下の質問に答えてください。

{question}
"""

erith_prompt = ChatPromptTemplate.from_messages([("human", erith_message)])

# 問い合わせ
erith_chain = erith_prompt | model
erith_response = erith_chain.invoke({"question": question_text})

# 結果確認
print("【えりすちゃんの回答】")
print(erith_response.content)
