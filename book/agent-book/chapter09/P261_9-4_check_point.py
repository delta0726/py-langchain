"""
Title   : LangChainとLangGraphによるRAG・AIエージェント実践入門
Chapter : 9 LangGraphで作るAIエージェント実践入門
Section : 4 チェックポイント機能
Theme   : ステートの永続化と再開
Date    : 2025/06/25
Page    : P261-272
"""

# ＜ポイント＞
# - チェックポイント機能とはワークフロー実行中に特定地点でのステートを保存するメカニズムを指す
# - LangGraphでは以下のチェックポンと機能が用意されている
# - ワークフローが複雑になると実行時間も長くなるので、エラー時のリカバリやデバッグが重要となる
# - LLMは問い合わせにコストもかかるため、チェックポイント機能を活用したデータ損失回避が重要


# ＜チェックポイント機能＞
# - ステートの永続化： ワークフローの実行状態を保存して同じステートから再開
# - エラーの回復： エラーが発生した場合に直前のチェックポイントから再開
# - デバッグ：ワークフローの実行過程を追跡し、問題の原因を特定する

import operator
from typing import Annotated, Any
from pprint import pprint

from pydantic import BaseModel, Field
from langchain_core.messages import SystemMessage, HumanMessage, BaseMessage
from langchain_core.runnables import RunnableConfig
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from langgraph.checkpoint.base import BaseCheckpointSaver


# ステート定義 -------------------------------------------------------


class State(BaseModel):
    query: str
    messages: Annotated[list[BaseMessage], operator.add] = Field(default=[])


# ノード定義 --------------------------------------------------------


# メッセージ追加
def add_message(state: State) -> dict[str, Any]:
    """システムメッセージとユーザー入力を追加"""
    new_messages = []
    if not state.messages:
        new_messages.append(
            SystemMessage(content="あなたは最小限の応答をする対話エージェントです。")
        )
    new_messages.append(HumanMessage(content=state.query))
    return {"messages": new_messages}


def llm_response(state: State) -> dict[str, Any]:
    """LLMによる応答生成"""
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.5)
    ai_message = llm.invoke(state.messages)
    return {"messages": [ai_message]}


# チェックポイント表示
def show_checkpoint(checkpointer: BaseCheckpointSaver, config: RunnableConfig):
    checkpoints = checkpointer.list(config)
    for i, checkpoint in enumerate(checkpoints):
        print(f"--- チェックポイント #{i + 1} ---")
        print("■ チェックポイントデータ:")
        pprint(checkpoint.checkpoint)
        print("■ メタデータ:")
        pprint(checkpoint.metadata)
        print()

    # 最新のチェックポイントを取得して表示（任意）
    checkpoint_tuple = checkpointer.get_tuple(config)
    print("◎ 最新のチェックポイント")
    print("■ チェックポイントデータ:")
    pprint(checkpoint_tuple.checkpoint)
    print("■ メタデータ:")
    pprint(checkpoint_tuple.metadata)


# 関数定義：表示用 -------------------------------------------


def print_checkpoint_dump(checkpointer: BaseCheckpointSaver, config: RunnableConfig):
    checkpoint_tuple = checkpointer.get_tuple(config)

    print("チェックポイントデータ:")
    pprint(checkpoint_tuple.checkpoint)
    print("\nメタデータ:")
    pprint(checkpoint_tuple.metadata)


# ワークフロー構築 --------------------------------------------

# インスタンス生成
graph = StateGraph(state_schema=State)

# ノードの追加
graph.add_node(node="add_message", action=add_message)
graph.add_node(node="llm_response", action=llm_response)

# エッジの追加
graph.set_entry_point(key="add_message")
graph.add_edge(start_key="add_message", end_key="llm_response")
graph.add_edge(start_key="llm_response", end_key=END)

# チェックポイント設定と実行
checkpointer = MemorySaver()

# コンパイル
compiled = graph.compile(checkpointer=checkpointer)


# =========================
# スレッド「example-1」の会話
# =========================

print("\n============================")
print("スレッド: example-1")
print("============================")


# コンフィグ設定
config_1 = {"configurable": {"thread_id": "example-1"}}

# 問い合わせ
response_1 = compiled.invoke(
    input=State(query="私の好きなものはずんだ餅です。覚えておいてね。"), config=config_1
)

# 確認
print("応答1:", response_1["messages"][-1].content)
show_checkpoint(checkpointer=checkpointer, config=config_1)


# 問い合わせ
response_2 = compiled.invoke(
    input=State(query="私の好物は何か覚えてる？"), config=config_1
)

# 確認
print("応答2:", response_2["messages"][-1].content)
show_checkpoint(checkpointer=checkpointer, config=config_1)


# =========================
# スレッド「example-2」の会話
# =========================

print("\n============================")
print("スレッド: example-2")
print("============================")

config_2 = {"configurable": {"thread_id": "example-2"}}

response_3 = compiled.invoke(State(query="私の好物は何？"), config=config_2)
print("応答3:", response_3["messages"][-1].content)

show_checkpoint(checkpointer=checkpointer, config=config_2)
