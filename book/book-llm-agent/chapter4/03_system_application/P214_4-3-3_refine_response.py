"""
Title   : やさしく学ぶLLMエージェント
Chapter : 4 マルチエージェント
Section : 3 マルチエージェントの活用
Theme   : 応答を洗練させよう
Date    : 2025/07/21
Page    : P214-230
"""

from typing import Annotated
from typing_extensions import TypedDict
from functools import partial
from IPython.display import display, Image

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END


# 準備 ----------------------------
# LLMの初期化
# --- 視点を変えるために同一モデルを3つに分ける
# --- 今回はLLMは変えずにロールだけ設定
llm_openai = ChatOpenAI(model="gpt-4o-mini")  # OpenAI視点
llm_anthropic = ChatOpenAI(model="gpt-4o-mini")  # Anthropic視点
llm_google = ChatOpenAI(model="gpt-4o-mini")  # Google視点


# 状態管理クラス
class State(TypedDict):
    human_message: HumanMessage
    messages: Annotated[list, add_messages]
    prev_messages: list[AIMessage]
    layer_cnt: int


# 応答統合テンプレート ---------------------------------------------

AGGREGATOR_SYSTEM_TEMPLATE = """\
最新のユーザーの質問に対して、さまざまなLLMからの回答が提供されています。
あなたの任務は、これらの回答を統合して、単一の高品質な回答を作成することです。
提供された回答に含まれる情報を批判的に評価し、一部の情報が偏っていたり誤っていたりする可能性があることを認識することが重要です。
回答を単に複製するのではなく、正確で包括的な返答を提供してください。
回答が良く構造化され、一貫性があり、最高の精度と信頼性の基準を満たすようにしてください。

{prev_messages}
"""


# エージェント関数の定義 -------------------------------------------


def agent(state: State, llm: ChatOpenAI, name: str):
    input_messages = []

    if state["prev_messages"]:
        prev_text = "\n".join(
            f"{i + 1}. {m.content}" for i, m in enumerate(state["prev_messages"])
        )
        system_msg = AGGREGATOR_SYSTEM_TEMPLATE.format(prev_messages=prev_text)
        input_messages.append(SystemMessage(system_msg))

    input_messages.append(state["human_message"])
    response = llm.invoke(input_messages)
    response.name = name

    return {"messages": [response]}


# エージェント定義
agent_openai = partial(agent, llm=llm_openai, name="openai")
agent_anthropic = partial(agent, llm=llm_anthropic, name="anthropic")
agent_google = partial(agent, llm=llm_google, name="google")

# 辞書登録
agent_dict = {
    "openai": agent_openai,
    "anthropic": agent_anthropic,
    "google": agent_google,
}


# グラフ制御用関数 -----------------------------------------


def update(state: State, num_agents: int):
    return {
        "prev_messages": state["messages"][-num_agents:],
        "layer_cnt": state["layer_cnt"] + 1,
    }


def router(state: State, num_layers: int, agent_name_list: list[str]):
    if state["layer_cnt"] < num_layers:
        return agent_name_list
    else:
        return "final_agent"


# グラフ構築 ----------------------------------------------

# パラメータ
num_layers = 3

# グラフ初期化
graph_builder = StateGraph(state_schema=State)

# ノード追加
graph_builder.add_node(
    node="update", action=partial(update, num_agents=len(agent_dict))
)
graph_builder.add_node(
    node="final_agent", action=agent_dict["openai"]
)  # 最終統合は openai に任せる

# 構造的ノード/エッジ
for name, func in agent_dict.items():
    graph_builder.add_node(node=name, action=func)
    graph_builder.add_edge(start_key=START, end_key=name)
    graph_builder.add_edge(start_key=name, end_key="update")

# 条件付エッジの設定
graph_builder.add_conditional_edges(
    source="update",
    path=partial(
        router, num_layers=num_layers, agent_name_list=list(agent_dict.keys())
    ),
    path_map=list(agent_dict.keys()) + ["final_agent"],
)

# エッジ追加
graph_builder.add_edge(start_key="final_agent", end_key=END)

# コンパイル
graph = graph_builder.compile()

# 可視化
display(Image(graph.get_graph().draw_mermaid_png()))


# 実行例 --------------------------------------------

# 質問
human_message = HumanMessage(content="マルチエージェントについて教えて")

# 状態設定
state: State = {
    "human_message": human_message,
    "messages": [],
    "prev_messages": [],
    "layer_cnt": 1,
}

# ディベート
print("#################### Layer 1 ####################")
for event in graph.stream(state):
    for value in event.values():
        if "messages" in value:
            value["messages"][-1].pretty_print()
        if "layer_cnt" in value:
            print(
                f"\n\n#################### Layer {value['layer_cnt']} ####################"
            )
