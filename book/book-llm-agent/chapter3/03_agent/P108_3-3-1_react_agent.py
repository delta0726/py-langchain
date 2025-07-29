"""
Title   : やさしく学ぶLLMエージェント
Chapter : 3 エージェント
Section : 3 複雑なワークフローで推論するエージェント
Theme   : エージェントによるReActアプローチ
Date    : 2025/07/29
Page    : P108-115
"""

# ＜概要＞
# - langchainのAgent機能を用いてエージェントによるツール実行を実現する
# - AgentExecutorを用いることでLLMがツールの選択と実行を行う
#   --- ｢P100_3-2-3_homemade_tool.py｣で実行できなかった"今日の運勢"に対応できる

# ＜ReActアプローチ＞
# - ReActは"Reasoning and Acting"の略で、LLMが推論と行動を同時に行うアプローチ
# - "Think, Act, Observe"のサイクルを繰り返すことで、複雑なタスクを解決する
#    --- 複雑な問題を小さなステップに分解し、逐次的に解決する
#    --- LLMが自らの推論過程を考慮して説明しながら行動を決定する

import random
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from langchain.tools import BaseTool
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage
from langchain.agents import AgentExecutor, create_react_agent
from langchain import hub


# 1 ツールロジックの定義 ------------------------------------------------

# ＜ポイント＞
# - ツールのロジック部分は関数として定義する


# 運勢を占う関数
def get_fortune(date_string="1月1日"):
    try:
        # 年を補完して変換
        date = datetime.strptime("2025年" + date_string, "%Y年%m月%d日")
    except ValueError:
        return "無効な日付形式です。'X月X日'の形式で入力してください。"

    fortunes = ["大吉", "中吉", "小吉", "吉", "末吉", "凶", "大凶"]
    weights = [1, 3, 3, 4, 3, 2, 1]
    random.seed(date.month * 100 + date.day)
    fortune = random.choices(population=fortunes, weights=weights)[0]

    return f"{date.month}月{date.day}日の運勢は【{fortune}】です。"


# 日付を返す関数（今日・明日・明後日のみ対応）
def get_date(keyword=["今日", "明日", "明後日"][0]):
    date_now = datetime.now(ZoneInfo("Asia/Tokyo"))
    date_map = {"今日": 0, "明日": 1, "明後日": 2}
    if keyword in date_map:
        return (date_now + timedelta(days=date_map[keyword])).strftime("%m月%d日")
    return "サポートしていません"


# 2 ツール構築 --------------------------------------------------------

# ＜ポイント＞
# - ツールはクラスでラップすることで定義する
# - ツールの名前(name)と概要(description)を定義、LLMはこの情報に基づきツール選択を行う
# - _runメソッドを定義すると最低限の動作が可能なツールとなる


# ツールクラス：運勢占い
class Get_fortune(BaseTool):
    name: str = "Get_fortune"
    description: str = "特定の日付の運勢を占う。入力は 'date_string' で、'mm月dd日' 形式の文字列（例：10月22日）。"

    def _run(self, date_string: str) -> str:
        return get_fortune(date_string)

    async def _arun(self, query: str) -> str:
        raise NotImplementedError("非同期実行はサポートしていません。")


# ツールクラス：日付取得
class Get_date(BaseTool):
    name: str = "Get_date"
    description: str = (
        "今日、明日、明後日の日付を取得。入力は '今日', '明日', '明後日' のいずれか。"
    )

    def _run(self, date_keyword: str) -> str:
        return get_date(date_keyword)

    async def _arun(self, query: str) -> str:
        raise NotImplementedError("非同期実行はサポートしていません。")


# 3 ReActエージェントの作成 -------------------------------------------------

# ＜ポイント＞
# - Chapter3-2-3で解けなかった"今日の運勢"についてエージェントに質問する
# - 特にロジックを組んでいないのに、エージェントの活用で実行できている
# - デバッグを入れてエージェントの動作を検証すること
#   --- エージェントの処理はデバッガーが入らないことが確認できる

# ＜エージェントの試行プロセス＞
# I need to check today's date so that I can get the fortune for today.
# Action: Get_date
# Action Input: 今日  07月29日I now know that today's date is July 29th. I will use this date to get the fortune for today.
# Action: Get_fortune
# Action Input: 07月29日  7月29日の運勢は【末吉】です。I now know the fortune for today.
# Final Answer: 今日の運勢は【末吉】です。


# プロンプトの取得
# --- ReAct専用のプロンプト
# --- https://smith.langchain.com/hub/hwchase17/react
prompt = hub.pull(owner_repo_commit="hwchase17/react")
print(prompt.template)

# エージェント構築
model = ChatOpenAI(model="gpt-4o-mini")
tools = [Get_date(), Get_fortune()]
agent = create_react_agent(llm=model, tools=tools, prompt=prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# 問い合わせ
response = agent_executor.invoke(
    {"input": [HumanMessage(content="今日の運勢を教えてください。")]}
)

# 結果確認
print(response)
