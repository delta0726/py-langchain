"""
Title   : やさしく学ぶLLMエージェント
Chapter : 4 マルチエージェント
Section : 2 マルチエージェントシステムの構築
Theme   : マルチエージェントLLMの概要
Date    : 2025/07/21
Page    : P177-185
"""

# ＜概要＞
# - マルチエージェントにツールを持たせて更に柔軟性を高める
#   --- ツールを紐づけたLLMを使用することで実現
#   --- 動作のイメージが直観的でないのでデバッガーを入れての動作確認が必須


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

# ＜ポイント＞
# - LLMにツールを紐づけることで実現


# モデルの定義
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# ツール結合
tavily_tool = TavilySearchResults(max_results=2)
llm_with_tool = llm.bind_tools(tools=[tavily_tool])


# 状態の定義
class State(TypedDict):
    messages: Annotated[list, add_messages]


# ノード関数の定義 ----------------------------------

# ＜ポイント＞
# - chatbot関数を定義してツール付LLMによる問い合わせをノードとして行う
# - ToolNodeはツールをフィールド変数として保持するためクラスで定義する
#   --- __call__を定義することでインスタンスをadd_nodeの引数とすることができる


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


# エッジ用のパーツ ----------------------------------

# ＜ポイント＞
# - chatbotノードが問い合わせをした直後に呼び出される
#   --- ツール付LLMで問い合わせする際にツールを使う必要があるかはLLMが判断する
#   --- この時点ではツールを使った問い合わせはまだ実行していない（ツール利用判断のみ）
# - ツールの呼び出しが必要かどうかを判定して次に進む経路を決める
#   --- add_conditional_edges()のpath引数として使用される
#   --- "tools"と"__end__"のどちらのに進むヘッジを選択するか決める

# ＜動作詳細＞
# - hasattr(ai_message, "tool_calls")
#   --- ai_messageが tool_callsという属性を持っているかを確認(安全対策)
# - len(ai_message.tool_calls) > 0
#   --- ツール呼び出しがあるかどうかをチェック


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

# ＜ポイント＞
# - chatbotは｢通常のLLMによる応答｣｢ツール呼び出し｣の2パターンの処理を行う


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


# 実行1：通常の応答文で回答 --------------------------------

# ＜ポイント＞
# - LLMが持つ知識のみで回答可能な普遍的な回答の質問
#   --- 一般知識でも近年の測量結果などが関係する質問はツールを呼び出してしまう
#       （例： 富士山の標高は何メートル？）


# 質問
initial_state = {"messages": [HumanMessage(content="水の化学式は何ですか？")]}

for event in graph.stream(initial_state):
    for value in event.values():
        if value and "messages" in value:
            value["messages"][-1].pretty_print()


# 実行2：ツール呼び出しによる回答 -----------------------------

# ＜ポイント＞
# - 検索による知識獲得が必要な質問


# 質問
initial_state = {"messages": [HumanMessage(content="今日の東京の天気を教えて")]}

for event in graph.stream(initial_state):
    for value in event.values():
        if value and "messages" in value:
            value["messages"][-1].pretty_print()
