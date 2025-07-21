"""
Title   : やさしく学ぶLLMエージェント
Chapter : 4 マルチエージェント
Section : 2 マルチエージェントシステムの構築
Theme   : マルチエージェントLLMの概要
Date    : 2025/07/21
Page    : P177-185
"""

from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, ToolMessage
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from typing_extensions import TypedDict
from typing import Annotated, Literal
from IPython.display import display, Image
import json


# 準備 ---------------------------------------------

# モデルの定義
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# ツール結合
tavily_tool = TavilySearchResults(max_results=2)
llm_with_tool = llm.bind_tools([tavily_tool])


# 状態の定義
class State(TypedDict):
    messages: Annotated[list, add_messages]


# ノード関数の定義 ----------------------------------


# チャットボットノード
def chatbot(state: State):
    messages = [llm_with_tool.invoke(state["messages"])]
    return {"messages": messages}


# ツールノード
class ToolNode:
    def __init__(self, tools: list) -> None:
        self.tools_by_name = {tool.name: tool for tool in tools}

    def __call__(self, state: State):
        if messages := state.get("messages", []):
            message = messages[-1]
        else:
            raise ValueError("入力にメッセージが見つかりません")

        tool_messages = []
        for tool_call in message.tool_calls:
            tool_result = self.tools_by_name[tool_call["name"]].invoke(
                tool_call["args"]
            )
            tool_messages.append(
                ToolMessage(
                    content=json.dumps(tool_result, ensure_ascii=False),
                    name=tool_call["name"],
                    tool_call_id=tool_call["id"],
                )
            )
        return {"messages": tool_messages}


tool_node = ToolNode([tavily_tool])


# ルーティング関数
def route_tools(state: State) -> Literal["tools", "__end__"]:
    if messages := state.get("messages", []):
        ai_message = messages[-1]
    else:
        raise ValueError("stateにツールに関するメッセージが見つかりません")

    if hasattr(ai_message, "tool_calls") and len(ai_message.tool_calls) > 0:
        return "tools"
    return "__end__"


# グラフ構築 ---------------------------------------------

# グラフ初期化
graph_builder = StateGraph(state_schema=State)

# ノード追加
graph_builder.add_node(node="chatbot", action=chatbot)
graph_builder.add_node(node="tools", action=tool_node)

# エッジ追加
graph_builder.add_edge(start_key=START, end_key="chatbot")
graph_builder.add_conditional_edges(
    source="chatbot", path=route_tools, path_map=["tools", "__end__"]
)
graph_builder.add_edge(start_key="tools", end_key="chatbot")

# コンパイル
graph = graph_builder.compile()

# グラフ可視化
display(Image(graph.get_graph().draw_mermaid_png()))


# 実行 -------------------------------------------------

# 質問
initial_state = {"messages": [HumanMessage("今日の東京の天気を教えて")]}

for event in graph.stream(initial_state):
    for value in event.values():
        if value and "messages" in value:
            value["messages"][-1].pretty_print()
