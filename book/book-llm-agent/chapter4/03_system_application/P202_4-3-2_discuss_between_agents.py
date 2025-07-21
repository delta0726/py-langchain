"""
Title   : やさしく学ぶLLMエージェント
Chapter : 4 マルチエージェント
Section : 3 マルチエージェントの活用
Theme   : 議論させてみよう
Date    : 2025/07/21
Page    : P202-214
"""

import functools
from typing import Annotated
from typing_extensions import TypedDict

from pydantic import BaseModel, Field

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages

from IPython.display import display, Image


# 準備 -------------------------------------------

# LLM定義
llm = ChatOpenAI(model="gpt-4o-mini")


# State定義
class State(TypedDict):
    messages: Annotated[list, add_messages]
    debate_topic: str
    judged: bool
    round: int


# エージェント定義 -------------------------------


# Cotエージェント
def cot_agent(state: State):
    """CoTエージェント：議題に対してステップバイステップで考える"""
    system_prompt = (
        "与えられた議題に対し、ステップバイステップで考えてから回答してください。"
        "議題：{debate_topic}"
    )
    system_message = SystemMessage(
        system_prompt.format(debate_topic=state["debate_topic"])
    )
    content = llm.invoke([system_message]).content
    message = HumanMessage(content=content, name="CoT")
    return {"messages": [message]}


# ディベーターエージェント
def debater(state: State, name: str, position: str):
    """
    ディベーターエージェント
    - name: キャラクター名
    - position: 肯定側 or 否定側の立場文
    """
    system_prompt = (
        "あなたはディベーターです。ディベート大会へようこそ。"
        "私たちの目的は正しい答えを見つけることですので、お互いの視点に完全に同意する必要はありません。"
        "ディベートのテーマは以下の通りです：{debate_topic}"
        "\n\n{position}"
    )
    system_message = SystemMessage(
        system_prompt.format(debate_topic=state["debate_topic"], position=position)
    )
    content = llm.invoke([system_message, *state["messages"]]).content
    message = HumanMessage(content=content, name=name)
    return {"messages": [message]}


# ディベーターの定義 -----------------------------------------

# 肯定側
affirmative_debator = functools.partial(
    debater,
    name="Affirmative_Debater",
    position=(
        "あなたは肯定側です。あなたの見解を簡潔に述べてください。"
        "否定側の意見が与えられた場合は、それに反対して理由を簡潔に述べてください。"
    ),
)

# 否定側
negative_debator = functools.partial(
    debater,
    name="Negative_Debater",
    position=(
        "あなたは否定側です。肯定側の意見に反対し、あなたの理由を簡潔に説明してください。"
    ),
)


# Judge ----------------------------------------------------


class JudgeSchema(BaseModel):
    judged: bool = Field(..., description="勝者が決まったかどうか")
    answer: str = Field(description="議題に対する結論とその理由")


def judger(state: State):
    """
    司会者エージェント：両者の回答を評価して勝者を判定
    判定できなければ次ラウンドへ
    """
    system_prompt = (
        "あなたは司会者です。"
        "ディベート大会に2名のディベーターが参加します。"
        "彼らは{debate_topic}について自分の回答を発表し、それぞれの視点について議論します。"
        "各ラウンドの終わりに、あなたは両者の回答を評価していき、ディベートの勝者を判断します。"
        "判定が難しい場合は、次のラウンドで判断してください。"
    )
    system_message = SystemMessage(
        system_prompt.format(debate_topic=state["debate_topic"])
    )

    llm_with_format = llm.with_structured_output(JudgeSchema)
    res = llm_with_format.invoke([system_message, *state["messages"]])

    messages = []
    if res.judged:
        messages.append(HumanMessage(res.answer))
    return {"messages": messages, "judged": res.judged}


# Round Monitor --------------------------------------------------


def round_monitor(state: State, max_round: int):
    round_num = state["round"] + 1
    if state["round"] < max_round:
        return {"round": round_num}
    else:
        return {
            "messages": [
                HumanMessage(
                    "最終ラウンドなので、勝者を決定し、議題に対する結論とその理由を述べてください。"
                )
            ],
            "round": round_num,
        }


round_monitor = functools.partial(round_monitor, max_round=3)


# Graph構築 ----------------------------------------------------

# グラフ初期化
graph_builder = StateGraph(state_schema=State)

# ノード追加
graph_builder.add_node(node="cot_agent", action=cot_agent)
graph_builder.add_node(node="affirmative_debator", action=affirmative_debator)
graph_builder.add_node(node="negative_debator", action=negative_debator)
graph_builder.add_node(node="round_monitor", action=round_monitor)
graph_builder.add_node(node="judger", action=judger)

# エッジ追加
graph_builder.add_edge(start_key=START, end_key="cot_agent")
graph_builder.add_edge(start_key="cot_agent", end_key="affirmative_debator")
graph_builder.add_edge(start_key="affirmative_debator", end_key="negative_debator")
graph_builder.add_edge(start_key="negative_debator", end_key="round_monitor")
graph_builder.add_edge(start_key="round_monitor", end_key="judger")

# 条件付エッジの設定
graph_builder.add_conditional_edges(
    source="judger",
    path=lambda state: state["judged"],
    path_map={True: END, False: "affirmative_debator"},
)

# コンパイル
graph = graph_builder.compile()

# Graph可視化
display(Image(graph.get_graph().draw_mermaid_png()))


# 実行例 ----------------------------------------------

# 質問とパラメータ
inputs = {
    "messages": [],
    "debate_topic": "戦争は必要か？",
    "judged": False,
    "round": 0,
}

# ディベート
for event in graph.stream(inputs):
    for value in event.values():
        try:
            value["messages"][-1].pretty_print()
        except Exception:
            pass
