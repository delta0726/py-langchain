"""
Title   : やさしく学ぶLLMエージェント
Chapter : 4 マルチエージェント
Section : 2 マルチエージェントシステムの構築
Theme   : 3つのエージェントから選択されたものが応答するシステム
Date    : 2025/07/21
Page    : P172-177
"""

# ＜概要＞
# - 3種類のエージェントから監督者が指名したエージェントが発言するシステムを構築する
#   --- 監督者エージェント(スーパーバイザー)を定義する
#   --- スーパーバイザーがエージェント辞書から選択する

import functools
from typing import Annotated, List, Dict, Literal
from typing_extensions import TypedDict
from pydantic import BaseModel, Field

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


# エージェントの定義と辞書化------------------------------

# ＜ポイント＞
# -


kenta_traits = """
- アクティブで冒険好き
- 新しい経験を求める
- アウトドア活動を好む
- SNSでの共有を楽しむ
- エネルギッシュで社交的
"""

mari_traits = """
- 穏やかでリラックス志向
- 家族を大切にする
- 静かな趣味を楽しむ
- 心身の休養を重視
- 丁寧な生活を好む
"""

yuta_traits = """
- バランス重視
- 柔軟性がある
- 自己啓発に熱心
- 伝統と現代の融合を好む
- 多様な経験を求める
"""

# エージェント定義
kenta = functools.partial(agent_with_persona, name="kenta", traits=kenta_traits)
mari = functools.partial(agent_with_persona, name="mari", traits=mari_traits)
yuta = functools.partial(agent_with_persona, name="yuta", traits=yuta_traits)

# エージェント辞書
member_dict = {
    "kenta": kenta_traits,
    "mari": mari_traits,
    "yuta": yuta_traits,
}


# スーパーバイザーの設定 ----------------------------------------

# ＜ポイント＞
# - エージェントを選択するスーパーバイザーを設定する
#   --- スーパーバイザーがエージェントを選んだ理由は出力されない
#   --- 適当に選んでいる可能性が高い


class RouteSchema(BaseModel):
    next: Literal["kenta", "mari", "yuta"] = Field(..., description="次に発言する人")


def supervisor(state: State) -> Dict[str, str]:
    members = ", ".join(member_dict.keys())
    traits_description = "\n".join(
        [f"**{name}**\n{traits}" for name, traits in member_dict.items()]
    )

    template = """
    あなたは以下の作業者間の会話を管理する監督者です：{members}。
    各メンバーの性格は以下の通りです。
    {traits_description}
    与えられたユーザーリクエストに対して、次に発言する人を選択してください。
    """

    # SystemMessagePromptTemplateにテンプレート文字列を渡す
    system_template = SystemMessagePromptTemplate.from_template(template=template)
    system_message = system_template.format(
        members=members, traits_description=traits_description
    )

    llm_with_format = llm.with_structured_output(RouteSchema)
    next_agent = llm_with_format.invoke([system_message] + state["messages"]).next

    return {"next": next_agent}


# グラフ構築 ---------------------------------------------

# グラフ初期化
graph_builder = StateGraph(state_schema=State)

# ノード追加
graph_builder.add_node(node="supervisor", action=supervisor)
graph_builder.add_node(node="kenta", action=kenta)
graph_builder.add_node(node="mari", action=mari)
graph_builder.add_node(node="yuta", action=yuta)

# エッジ追加
graph_builder.add_edge(start_key=START, end_key="supervisor")
graph_builder.add_conditional_edges(
    source="supervisor",
    path=lambda state: state["next"],
    path_map={"kenta": "kenta", "mari": "mari", "yuta": "yuta"},
)
for member in member_dict:
    graph_builder.add_edge(start_key=member, end_key=END)

# コンパイル
graph = graph_builder.compile()


# グラフ可視化
display(Image(graph.get_graph().draw_mermaid_png()))


# 実行 -------------------------------------------------

# 質問
human_message = HumanMessage("休日のまったりした過ごし方を教えて")

for event in graph.stream({"messages": [human_message]}):
    for value in event.values():
        if isinstance(value, dict):
            if "next" in value:
                print(f"次に発言する人: {value['next']}")
            elif "messages" in value:
                value["messages"][-1].pretty_print()
