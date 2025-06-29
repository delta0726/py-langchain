"""
Title   : LangChainとLangGraphによるRAG・AIエージェント実践入門
Chapter : 9 LangGraphで作るAIエージェント実践入門
Section : 3 ハンズオン
Theme   : エージェントを活用したQAアプリケーション
Date    : 2025/6/29
Page    : P251-260
"""

import os
import operator
from typing import Annotated, Any

from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langchain_core.runnables import ConfigurableField
from langgraph.graph import StateGraph, END
from langchain_core.tracers import LangChainTracer


# 基本設定 ------------------------------------------------------------

# 環境変数
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGSMITH_PROJECT"] = "agent-book"

# トレーサーの設定
# --- LangSmith: https://smith.langchain.com/
tracer = LangChainTracer()

# LLM 初期化
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.0)
llm = llm.configurable_fields(max_tokens=ConfigurableField(id='max_tokens'))


# ロール定義 ---------------------------------------------------------

# ＜ポイント＞
# - 回答を生成する前に、回答を担当するためのロール選択を行う
# - 事前定義できる内容は開発者が定義するほうが、LLMの生成にかかる金銭的コストが下がる
# - また、開発者が決定するほうがコントロール性も高まる


ROLES = {
    "1": {
        "name": "一般知識エキスパート",
        "description": "幅広い分野の一般的な質問に答える",
        "details": "幅広い分野の一般的な質問に対して、正確で分かりやすい回答を提供してください。"
    },
    "2": {
        "name": "生成AI製品エキスパート",
        "description": "生成AIや関連製品、技術に関する専門的な質問に答える",
        "details": "生成AIや関連製品、技術に関する専門的な質問に対して、最新の情報と深い洞察を提供してください。"
    },
    "3": {
        "name": "カウンセラー",
        "description": "個人的な悩みや心理的な問題に対してサポートを提供する",
        "details": "個人的な悩みや心理的な問題に対して、共感的で支援的な回答を提供し、可能であれば適切なアドバイスも行ってください。"
    }
}


# ステート定義 -------------------------------------------------------

# ＜ポイント＞
# - LangGraphでは各ノードが実行されるたびに｢状態(State)｣が引き継がれ更新される
# - StateクラスはAIエージェントの記憶メモ帳であり、その｢状態の入れ物｣になっている


class State(BaseModel):
    query: str = Field(..., description="ユーザーからの質問")
    current_role: str = Field(
        default="", description="選定された回答ロール"
    )
    messages: Annotated[list[str], operator.add] = Field(
        default=[], description="回答履歴"
    )
    current_judge: bool = Field(
        default=False, description="品質チェックの結果"
    )
    judgement_reason: str = Field(
        default="", description="品質チェックの判定理由"
    )


# ジャッジ定義 -------------------------------------------------------

# ＜ポイント＞
# - チェックノードで使用する
# - エージェントの評価結果をbool型とstr型で格納する


class Judgement(BaseModel):
    judge: bool = Field(default=False)
    reason: str = Field(default="")


# ノード定義 ---------------------------------------------------------

# 回答ロールの選定
def selection_node(state: State) -> dict[str, Any]:
    role_options = "\n".join([f"{k}. {v['name']}: {v['description']}" for k, v in ROLES.items()])
    prompt = ChatPromptTemplate.from_template(
        template="""
        質問を分析し、最も適切な回答担当ロールを選択してください。

        選択肢:
        {role_options}

        回答は選択肢の番号（1、2、または3）のみを返してください。

        質問: {query}
        """
    )
    chain = prompt | llm.with_config(configurable={"max_tokens": 1}) | StrOutputParser()
    role_number = chain.invoke({"role_options": role_options, "query": state.query}).strip()
    return {"current_role": ROLES[role_number]["name"]}

# 選定ロールに基づいて回答
def answering_node(state: State) -> dict[str, Any]:
    role_details = "\n".join([f"- {v['name']}: {v['details']}" for v in ROLES.values()])
    prompt = ChatPromptTemplate.from_template(
        template="""
        あなたは{role}として回答してください。
        以下の質問に対して、あなたの役割に基づいた適切な回答を提供してください。

        役割の詳細:
        {role_details}

        質問: {query}

        回答:
        """
    )
    chain = prompt | llm | StrOutputParser()
    answer = chain.invoke(input={
        "role": state.current_role,
        "role_details": role_details,
        "query": state.query
    })
    return {"messages": [answer]}


# 回答の品質をチェック
def check_node(state: State) -> dict[str, Any]:
    prompt = ChatPromptTemplate.from_template(
        template="""
        以下の回答の品質をチェックし、問題がある場合は'False'、問題がない場合は'True'を回答してください。
        また、その判断理由も説明してください。

        ユーザーからの質問: {query}
        回答: {answer}"""
    )
    chain = prompt | llm.with_structured_output(Judgement)
    result: Judgement = chain.invoke({"query": state.query, "answer": state.messages[-1]})
    return {"current_judge": result.judge, "judgement_reason": result.reason}



# ワークフロー構築 --------------------------------------------

# インスタンス生成
workflow = StateGraph(state_schema=State)

# ノードの追加
workflow.add_node(node="selection", action=selection_node)
workflow.add_node(node="answering", action=answering_node)
workflow.add_node(node="check", action=check_node)

# エッジの追加
# --- 出発点をselectionノードに設定
workflow.set_entry_point(key="selection")
workflow.add_edge(start_key="selection", end_key="answering")
workflow.add_edge(start_key="answering", end_key="check")

# 条件付エッジの追加
workflow.add_conditional_edges(
    source="check",
    path=lambda state: state.current_judge,
    path_map={True: END, False: "selection"}
)

# コンパイル
compiled = workflow.compile()


# 実行例 ------------------------------------------------------

# 質問提示
initial_state = State(query="生成AIについて教えてください")

# 同期実行
# --- 逐次的に処理を実行
result = compiled.invoke(
    input=initial_state,
    config={"callbacks": [tracer]}
    )


# 非同期実行
# --- 並列的に処理を実行
# result = await compiled.ainvoke(initial_state)
# print(result["messages"][-1])


# 結果確認
print(result["messages"][-1])
