"""
Title   : やさしく学ぶLLMエージェント
Chapter : 2 エージェント作成のための基礎知識
Section : 2 LangChain入門
Theme   : Plan-and-Solveチャットボット
Date    : 2025/07/18
Page    : P51-58
"""

# ＜ポイント＞
# - 特殊なプロンプトテンプレート
# - 分岐やループを含む複雑なワークフローの実装

# ＜Plan-and-Sloveとは＞
# - 与えられたタスクを解く前に問題解決のための計画を策定する
# - その後、計画に沿ってタスクを解くことで、無計画に解くよりも高い性能が得られる
# - プロンプト内で指示することもできるが、ここでは構造的な仕組みを作る

from langchain_openai import ChatOpenAI
from langchain_core.prompts import (
    PromptTemplate,
    ChatPromptTemplate,
    MessagesPlaceholder,
)
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_openai.output_parsers.tools import PydanticToolsParser
from pydantic import BaseModel, Field


# 準備 --------------------------------------------------------------

# モデル定義
llm = ChatOpenAI(model="gpt-4o-mini")


# Pydantic モデルの定義 ----------------------------------------------

# ＜概要＞
# - ActionItem: 個別のタスクを管理
# - Plan: ActionItemをまとめたもので計画全体を記述
# - ActionResult: 個別タスクを実行した際のアウトプット


class ActionItem(BaseModel):
    action_name: str = Field(description="アクション名")
    action_description: str = Field(description="アクションの詳細")


class Plan(BaseModel):
    problem: str = Field(description="問題の説明")
    actions: list[ActionItem] = Field(description="実行すべきアクションリスト")


class ActionResult(BaseModel):
    thoughts: str = Field(description="検討内容")
    result: str = Field(description="結果")


# アクション実行計画 ------------------------------------------------

ACTION_PROMPT = """\
問題をアクションプランに分解して解いています。
これまでのアクションの結果と、次に行うべきアクションを示すので、
実際にアクションを実行してその結果を報告してください。

# 問題
{problem}

# アクションプラン
{action_items}

# これまでのアクションの結果
{action_results}

# 次のアクション
{next_action}
"""

# プロンプト
action_prompt = PromptTemplate.from_template(template=ACTION_PROMPT)

# LLM
llm_action = llm.bind_tools(tools=[ActionResult], tool_choice="ActionResult")

# ツールパーサー
# --- Action Result
action_parser = PydanticToolsParser(tools=[ActionResult], first_tool_only=True)

# チェイン
action_runnable = action_prompt | llm_action | action_parser


# アクション・ループ --------------------------------------------------


def action_loop(action_plan: Plan):
    problem = action_plan.problem
    actions = action_plan.actions
    action_items = "\n".join([f"* {action.action_name}" for action in actions])

    action_results = []
    action_results_str = ""

    for i, action in enumerate(actions):
        print("=" * 20)
        print(f"[{i + 1}/{len(actions)}]以下のアクションを実行します。")
        print(action.action_name)

        next_action = f"* {action.action_name}\n{action.action_description}"
        response = action_runnable.invoke(
            input={
                "problem": problem,
                "action_items": action_items,
                "action_results": action_results_str,
                "next_action": next_action,
            }
        )

        action_results.append(response)
        action_results_str += f"* {action.action_name}\n{response.result}\n"

        print("-" * 10 + "検討内容" + "-" * 10)
        print(response.thoughts)
        print("-" * 10 + "結果" + "-" * 10)
        print(response.result)

    return AIMessage(action_results_str)


# Plan-and-Solve 分岐ルート ------------------------------------------


# 
plan_parser = PydanticToolsParser(tools=[Plan], first_tool_only=True)


def router(ai_message: AIMessage):
    if ai_message.response_metadata["finish_reason"] == "tool_calls":
        return plan_parser | action_loop
    else:
        return ai_message


# 実行計画の全体像 -----------------------------------------------------

# ＜ポイント＞
# - Plan-and-Sloveのプロセスを定義して処理プロセスはPlanに格納する
# - 処理プロセスを格納した状態でrouterを呼び出す


PLAN_AND_SOLVE_PROMPT = """\
ユーザの質問が複雑な場合は、アクションプランを作成し、その後に1つずつ実行する Plan-and-Solve 形式をとります。
これが必要と判断した場合は、Plan ツールによってアクションプランを保存してください。
"""

# プロンプト
# --- システムメッセージでPlan-and-Sloveのコンセプトを説明
# --- メッセージプレースホルダーでユーザー質問を受取る
chat_prompt = ChatPromptTemplate.from_messages(
    messages=[
        SystemMessage(PLAN_AND_SOLVE_PROMPT),
        MessagesPlaceholder(variable_name="history"),
    ]
)

# ツールパーサー
# --- LLMにPlanで定義したスキーマで出力するように要請
llm_plan = llm.bind_tools(tools=[Plan])

# チェイン
# --- planning_runnable.invoke()で実行されることでLLM Planが出力される
# --- AIMessageとしてrouterに渡される
planning_runnable = chat_prompt | llm_plan | router


# 使用例: チャットボット -----------------------------------------------

# 変数定義
# --- 履歴管理
# --- 質問管理
history = []
user_inputs = [
    "新しくプログラミング学習を始めたいです。どんな手順で進めていけば良いですか？",
    "生成AIを活用して中小企業の業務効率化を行いたいです。どんなステップで導入すべきでしょうか？",
]

i = 0
user_input = user_inputs[i]
for i, user_input in enumerate(user_inputs):
    print(f"\n========== 質問 {i + 1} ==========")

    # 1. ユーザー入力の表示と追加
    human_message = HumanMessage(content=user_input)
    human_message.pretty_print()
    history.append(human_message)

    # 2. Plan-and-Solveの実行
    ai_message = planning_runnable.invoke(input={"history": history})
    ai_message.pretty_print()
    history.append(ai_message)
