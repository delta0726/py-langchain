"""
Title   : Langchain完全入門
Section : 6 Agents - 自律的に外部と干渉して言語モデルの限界を超える
Theme   : 関数でToolに独自の機能を持たせてエージェントで実行する
Date    : 2025/04/30
Page    : P217
"""

import random
from langchain.agents import AgentType, Tool, initialize_agent
from langchain.chat_models import ChatOpenAI
from langchain.tools import WriteFileTool


# 言語モデルの定義
llm = ChatOpenAI(temperature=0, model="gpt-4o-mini")

# ツール定義
tools = []
tools.append(WriteFileTool(root_dir="./output/"))


# 関数定義
# --- 最小値を指定できるランダムな数字を生成する関数
def min_limit_random_number(min_number):
    return random.randint(int(min_number), 100000)


# ツールにカスタム機能を追加
# --- 関数でツールを作成
tools.append(
    Tool(
        name="Random",
        description="特定の最小値以上のランダムな数字を生成することができます。",
        func=min_limit_random_number,
    )
)

# エージェント定義
# --- ストラクチャ化された、"推論→実行→観察" という手順で動くLangChainのエージェント
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
)

# エージェント実行
result = agent.run(
    "10以上のランダムな数字を生成してrandom.txtというファイルに保存してください。"
)

# 結果確認
print(f"実行結果: {result}")
