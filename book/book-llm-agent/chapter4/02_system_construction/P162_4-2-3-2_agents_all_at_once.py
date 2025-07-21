"""
Title   : やさしく学ぶLLMエージェント
Chapter : 4 マルチエージェント
Section : 2 マルチエージェントシステムの構築
Theme   : 複数エージェントの接続
Date    : 2025/07/21
Page    : P162-172
"""


import functools

from typing_extensions import TypedDict
from typing import Annotated, List, Dict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages

from langchain_core.messages import SystemMessage, HumanMessage, BaseMessage
from langchain.prompts import SystemMessagePromptTemplate
from langchain_openai import ChatOpenAI

from IPython.display import display, Image


# 準備 ---------------------------------------------

# モデルの定義
llm: ChatOpenAI = ChatOpenAI(model="gpt-4o-mini", temperature=0)


# 状態の定義
class State(TypedDict):
    messages: Annotated[List[BaseMessage], add_messages]


# エージェント関数の定義 -----------------------------


def agent_with_persona(
    state: State, name: str, traits: str
) -> Dict[str, List[BaseMessage]]:
    # ペルソナを含むシステムメッセージの生成
    system_template: SystemMessagePromptTemplate = (
        SystemMessagePromptTemplate.from_template(
            "あなたの名前は{name}です。\nあなたの性格は以下のとおりです。\n\n{traits}"
        )
    )
    system_message: SystemMessage = system_template.format(name=name, traits=traits)

    # LLM 応答の生成と名前付きメッセージ化
    response: BaseMessage = llm.invoke(input=[system_message, *state["messages"]])
    named_message: HumanMessage = HumanMessage(content=response.content, name=name)

    return {"messages": [named_message]}


# 各ペルソナの定義とノード化------------------------------

kenta_traits = """\
- アクティブで冒険好き
- 新しい経験を求める
- アウトドア活動を好む
- SNSでの共有を楽しむ
- エネルギッシュで社交的"""

mari_traits = """\
- 穏やかでリラックス志向
- 家族を大切にする
- 静かな趣味を楽しむ
- 心身の休養を重視
- 丁寧な生活を好む"""

yuta_traits = """\
- バランス重視
- 柔軟性がある
- 自己啓発に熱心
- 伝統と現代の融合を好む
- 多様な経験を求める"""

kenta = functools.partial(agent_with_persona, name="kenta", traits=kenta_traits)
mari = functools.partial(agent_with_persona, name="mari", traits=mari_traits)
yuta = functools.partial(agent_with_persona, name="yuta", traits=yuta_traits)


# グラフ構築 ---------------------------------------------

# グラフ初期化
graph_builder = StateGraph(State)

# ノードの定義
graph_builder.add_node(node="kenta", action=kenta)
graph_builder.add_node(node="mari", action=mari)
graph_builder.add_node(node="yuta", action=yuta)

# エッジの追加
graph_builder.add_edge(start_key=START, end_key="kenta")
graph_builder.add_edge(start_key=START, end_key="mari")
graph_builder.add_edge(start_key=START, end_key="yuta")
graph_builder.add_edge(start_key="kenta", end_key=END)
graph_builder.add_edge(start_key="mari", end_key=END)
graph_builder.add_edge(start_key="yuta", end_key=END)

# コンパイル
graph = graph_builder.compile()

# グラフの可視化
display(Image(graph.get_graph().draw_mermaid_png()))


# 実行 -------------------------------------------------

# 質問
human_message = HumanMessage(content="休日の過ごし方について、建設的に議論してください。")

# 議論スタート
for event in graph.stream({"messages": [human_message]}):
    for value in event.values():
        value["messages"][-1].pretty_print()
