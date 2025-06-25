"""
Title   : Langchain完全入門
Section : 6 Agents - 自律的に外部と干渉して言語モデルの限界を超える
Theme   : URLアクセスというToolを持ったエージェント
Date    : 2025/04/27
Page    : P200
"""

from langchain.agents import AgentType, initialize_agent, load_tools
from langchain.chat_models import ChatOpenAI

"""
<エージェントの必要性>
今回はURLも明示されているので｢requestsで取得 → JSON整形してLLMに渡す｣で十分
ただし、requestsのコードを書かずにエージェントが処理する点が特筆すべき点
"""

# 言語モデルの定義
# --- temperatureを0に設定して出力の多様性を抑制(0-2で設定)
llm = ChatOpenAI(temperature=0, model="gpt-4o-mini")

# ← LangChainに用意されているToolを読み込む
tools = load_tools(
    tool_names=["requests_all"], 
    allow_dangerous_tools=True
    )


# Agentの初期化
# --- Agentが使用することができるToolの配列を設定
# --- Agentが使用する言語モデルを指定
agent = initialize_agent(
    tools=tools, llm=llm, 
    agent=AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION, 
    verbose=True
)

# エージェント実行
result = agent.run(
    """
    以下のURLにアクセスして東京の天気を調べて日本語で答えてください。
    https://www.jma.go.jp/bosai/forecast/data/overview_forecast/130000.json
    """
)

# 結果確認
print(f"実行結果: {result}")
