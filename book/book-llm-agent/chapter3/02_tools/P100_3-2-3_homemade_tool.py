"""
Title   : やさしく学ぶLLMエージェント
Chapter : 3 エージェント
Section : 2 LLLMにツールを与える
Theme   : ツールを自作する
Date    : 2025/07/29
Page    : P100-107
"""

# ＜概要＞
# - ツールはPythonの関数として定義することができ、目的によりフィットした操作が可能となる
# - AgentがReActによる推論を行うことで、ツール選択や引数設定のための事前質問をすることなく実現できる

# ＜今後の課題＞
# - 本例ではツール選択はLLMが行っているが、実行トリガーは人間がプログラムを書くことで実現している
#   --- 次節ではエージェント導入によりLLMにツールの実行判断も委ねることを目指す


from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage
from langchain.tools import BaseTool
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import random


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


# ツール定義（運勢）
class GetFortuneTool(BaseTool):
    name: str = "Get_fortune"
    description: str = "特定の日付の運勢を占うツール。入力は mm月dd日 形式の文字列（例：10月22日）を指定。"

    def _run(self, date_string: str) -> str:
        return get_fortune(date_string)

    async def _arun(self, _: str) -> str:
        raise NotImplementedError("asyncは非対応です")


# ツール定義（日付取得）
class GetDateTool(BaseTool):
    name: str = "Get_date"
    description: str = "今日・明日・明後日の日付を取得する。入力は '今日', '明日', '明後日' のいずれか。"

    def _run(self, date: str) -> str:
        return get_date(date)

    async def _arun(self, _: str) -> str:
        raise NotImplementedError("asyncは非対応です")


# 3 モデル + ツール実行 ------------------------------------------------


def run_model(question: str, tools: list[BaseTool]):
    model = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    model_with_tools = model.bind_tools(tools=tools)

    # 事前問い合わせ
    # --- 質問事項に適切なツール選択と
    # --- 質問からツールにインプットする引数を決定
    response = model_with_tools.invoke([HumanMessage(content=question)])
    print("質問:", question)
    print("モデル出力:", response.content)
    print("ツール呼び出し:", response.tool_calls)

    # 問い合わせ
    # --- 複数ツールをを想定した構成
    if response.tool_calls:
        tool_name = response.tool_calls[0]["name"]
        tool_args = response.tool_calls[0]["args"]
        tool_map = {tool.name: tool for tool in tools}
        if tool_name in tool_map:
            result = tool_map[tool_name].invoke(tool_args)
            print("ツール実行結果:", result)


# 実行例
if __name__ == "__main__":
    # 特定日付の運勢を質問
    run_model(
        question="7月22日の運勢を教えてください。", tools=[GetFortuneTool()]
    )

    # 日付を質問
    run_model(question="今日の日付を教えてください。", tools=[GetDateTool()])

    # 今日の日付に基づく運勢を質問
    # --- 2つのツールを使用している
    # --- 今日の日付をGetDateToolで取得して、GetFortuneTool()を呼び出すことを想定
    # --- 実際は"今日"に反応してGetDateToolしか実行されない（複雑な推論に対応できていない）
    run_model(
        question="今日の運勢を教えてください。", tools=[GetFortuneTool(), GetDateTool()]
    )
