"""
Title   : Langchain完全入門
Section : 6 Agents - 自律的に外部と干渉して言語モデルの限界を超える
Theme   : URLアクセスとGoogle検索のToolを持ったエージェントで結果をテキスト出力
Date    : 2025/04/27
Page    : P209
"""

from langchain.agents import AgentType, initialize_agent, load_tools
from langchain.chat_models import ChatOpenAI
from langchain.tools.file_management import WriteFileTool


# 言語モデルの定義
llm = ChatOpenAI(temperature=0, model="gpt-4o-mini")

# ツール定義
# --- serpapi: Google検索などができるツール
# --- requests_get: HTTPでGETリクエストを送るためのツール
tools = load_tools(
    tool_names=["requests_get", "serpapi"], llm=llm, allow_dangerous_tools=True
)

# ←ファイル書き込みできるToolを追加
tools.append(WriteFileTool(root_dir="./output/"))

# エージェント初期化
# --- ストラクチャ化された、"推論→実行→観察" という手順で動くLangChainのエージェント
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
)

# エージェント処理
result = agent.run(
    "北海道の名産品を調べて日本語でhokkaido.txtというファイルに保存してください。"
)

# 結果確認
print(f"実行結果: {result}")
