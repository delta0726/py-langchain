"""
Title   : Langchain完全入門
Section : 6 Agents - 自律的に外部と干渉して言語モデルの限界を超える
Theme   : メモリを搭載したエージェントで会話のやり取りを実現する
Date    : 2025/04/30
Page    : P229
"""

from langchain.agents import AgentType, initialize_agent
from langchain.agents.agent_toolkits import create_retriever_tool
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.retrievers import WikipediaRetriever


# 言語モデルの定義
llm = ChatOpenAI(temperature=0, model="gpt-4o-mini")

# Retriever定義
# --- Wikipediaの最も近い情報を500文字以内で取得
retriever = WikipediaRetriever(lang="ja", doc_content_chars_max=500, top_k_results=1)

# WriteFileToolを削除
tools = []
tools.append(
    create_retriever_tool(
        name="WikipediaRetriever", 
        description="受け取った単語に関するWikipediaの記事を取得できる", 
        retriever=retriever
    )
)

# メモリの初期化
# --- ConversationBufferMemory
memory = ConversationBufferMemory(
    memory_key="chat_history", 
    return_messages=True
)

# エージェント定義
# --- メモリも実装している
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION, 
    memory=memory, 
    verbose=True,
)

# エージェント実行（1回目）
prompt_1 = "スコッチウイスキーについてWikipediaで調べて日本語で概要をまとめてください。"
result_1 = agent.run(prompt_1)
print(f"1回目の実行結果: {result_1}")

# エージェント実行（2回目）
prompt_1 = "以前の指示をもう一度実行してください。"
result_2 = agent.run(prompt_1)
print(f"2回目の実行結果: {result_2}")
