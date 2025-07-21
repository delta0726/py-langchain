"""
Title   : やさしく学ぶLLMエージェント
Chapter : 4 マルチエージェント
Section : 2 マルチエージェントシステムの構築
Theme   : チャットボットの構築
Date    : 2025/07/19
Page    : P153-162
"""


# ＜概要＞
# - チャットボットの構築を題材にLangGraphの基本の構成要素を理解する


# ＜基本の構成要素＞
# - State : グラフに共通する情報を管理する要素
# - Node  : エージェントや関数による処理を担う要素
# - Edge  : ノード同士のつながりを表す要素
# - Graph : ノード・エッジから構成されるシステム全体を表す要素


# モジュールのインポート
from typing_extensions import TypedDict
from typing import Annotated

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

from IPython.display import display, Image


# 準備 ----------------------------------------------------------

# ＜Stateの定義＞
# - Stateはグラフに共通した情報を管理する要素となる
# - Stateにより特定ノードにおける処理結果を次のノードに移ったあとも参照できるようになる
# - これにより、処理結果に応じた分岐をエッジで表現することが可能となる
# - countでチャットボットとの対話した回数を記録する
# - messagesは単なるlist型ではなく、会話の履歴として扱うことを伝えている


# ＜チャットボットの定義＞
# - Stateを引数として与えて｢現在の状態の受け取り｣と｢処理後の状態伝達」を行っている
# - ペルソナはsystemメッセージを用いて"元気なエンジニア"として設定している


# モデルの定義
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)


# Stateの定義
class State(TypedDict):
    count: int
    messages: Annotated[list, add_messages]


# チャットボットの定義
def chatbot(state: State):
    system_message = SystemMessage(
        content="あなたは、元気なエンジニアです。元気に返答してください。"
    )
    messages = [llm.invoke(input=[system_message] + state["messages"])]
    count = state["count"] + 1
    return {
        "messages": messages,
        "count": count,
    }


# エージェント定義 ----------------------------------------------

# ＜ポイント＞
# - StateGraphクラスを用いてStateを元にしたグラフ構築を行う
# - インスタンスに関数を割り当てることでNodeを定義する
# - START/ENDを含めてノードをつなぎ合わせてEdgeを定義する
# - インスタンスにグラフの構成要素が揃ったらコンパイルを行う
# - コンパイルしたインスタンスはグラフとして可視化することができる


# グラフの構築
graph_builder = StateGraph(state_schema=State)
graph_builder.add_node(node="chatbot", action=chatbot)
graph_builder.add_edge(start_key=START, end_key="chatbot")
graph_builder.add_edge(start_key="chatbot", end_key=END)
graph = graph_builder.compile()


# グラフの可視化（Mermaid形式）
display(Image(data=graph.get_graph().draw_mermaid_png()))


# 実行例 -------------------------------------------------------

# ＜ポイント＞
# - Humanメッセージで質問事項を提示する
# - 初期状態をStateに与えるため辞書で状態を定義する


initial_message = HumanMessage(content="上手くデバッグができません")
initial_state = {"messages": [initial_message], "count": 0}

for event in graph.stream(input=initial_state):
    for value in event.values():
        print(f"### ターン{value['count']} ###")
        value["messages"][-1].pretty_print()
