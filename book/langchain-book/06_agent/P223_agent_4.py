"""
Title   : Langchain完全入門
Section : 6 Agents - 自律的に外部と干渉して言語モデルの限界を超える
Theme   : 関数でToolに独自の機能を持たせてエージェントで実行する
Date    : 2025/04/30
Page    : P223
"""

from langchain.agents import AgentType, Tool, initialize_agent
from langchain.agents.agent_toolkits import create_retriever_tool
from langchain.chat_models import ChatOpenAI
from langchain.retrievers import WikipediaRetriever
from langchain.tools import WriteFileTool


# 言語モデルの定義
llm = ChatOpenAI(temperature=0, model="gpt-4o-mini")

# ツール定義
tools = []
tools.append(WriteFileTool(root_dir="./output"))

# Retriever定義
# --- Wikipediaの最も近い情報を500文字以内で取得
retriever = WikipediaRetriever(lang="ja", doc_content_chars_max=500, top_k_results=1)

# ツールにカスタム機能を追加
tools.append(
    create_retriever_tool(
        name="WikipediaRetriever",
        description="受け取った単語に関するWikipediaの記事を取得できる",
        retriever=retriever,
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
    "スコッチウイスキーについてWikipediaで調べて概要を日本語でwhiskey.txtというファイルに保存してください。"
)

# 結果確認
print(f"実行結果: {result}")
