"""
Title   : LangChainとLangGraphによるRAG・AIエージェント実践入門
Chapter : 4 LangChainの基礎
Section : 3 Prompt Template
Theme   : LangSmithのプロンプト
Date    : 2025/05/25
Page    : P76
"""

# ＜ポイント＞
# - LangSmithはプロンプトやソースコードを別途管理する仕組み
#   --- 他にもプロンプトのバージョン管理や、プロンプトの実行履歴を確認することができる
#   --- LangChainと連携することでプロンプトが簡素化され管理しやすくなる

from langsmith import Client


# LLMの定義
client = Client()

# プロンプト取得
# --- LangSmithに登録されているプロンプトを取得
# --- パラメータを指定してプロンプトを呼び出し
prompt = client.pull_prompt(prompt_identifier="oshima/recipe")
prompt_value = prompt.invoke({"dish": "カレー"})

# 結果確認
print(prompt_value)
