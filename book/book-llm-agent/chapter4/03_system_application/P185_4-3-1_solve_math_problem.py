"""
Title   : やさしく学ぶLLMエージェント
Chapter : 4 マルチエージェント
Section : 3 マルチエージェントの活用
Theme   : 数学の問題を解かせよう
Date    : 2025/07/21
Page    : P185-201
"""

# ＜概要＞
# - ｢LLMエージェント｣と｢ユーザープロキシエージェント｣の対話を通じて数学問題を解く
# - 2つのエージェントが対話を通じて解いていくことで、単一エージェントで対処できない複雑な問題を解く

# ＜エージェント＞
# 1. LLMエージェント（生徒）
#  - 問題を回答していくエージェント
#  - ユーザープロキシエージェントが出力するプロンプトに従って解法を考える
#    --- 実際にはLLMに問い合わせてコードアイデアを得ている
#    --- 具体的なPythonコードの提供を受ける

# 2. ユーザープロキシエージェント（先生）
#  - LLMエージェントが問題を解く手助けをするエージェント
#  - 問題を解く手順や戦略を命令してLLMエージェントが問題を解けるよう導く
#    --- PythonREPL()を使ってコードを実行する
#    --- 実際にコードを実行して解いているのは先生ということになるかもしれない


# ＜学習ポイント＞
# - エージェントは実行プロセスが複雑なので、コードを見ているだけでは表面的理解と現実動作に大きな乖離が生まれる
# - 必ずデバッガーを入れて動作を確認して腹落ちさせる必要がある
#   --- かなり細かくデバッグしないと動作を追いきれない

import re
from typing import Annotated
from typing_extensions import TypedDict

from langchain_experimental.utilities import PythonREPL
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages

from IPython.display import display, Image


# 準備 ---------------------------------------------

# インスタンス定義
repl = PythonREPL()
llm = ChatOpenAI(model="gpt-4o-mini")


# 状態管理
class State(TypedDict):
    messages: Annotated[list, add_messages]
    problem: str
    first_flag: bool
    end_flag: bool


# ユーティリティ関数 ----------------------------------

# ＜ポイント＞
# - LLMエージェントがPythonプログラミングを使用することを促す
#   --- エージェントに持たせる関数


# コード部分を抜き出す関数（ユーザープロキシエージェント用）
def extract_code(input_string: str) -> str:
    """
    ```で囲まれたコード部分を抽出
    """
    pattern = r"```(.*?)```"
    match = re.findall(pattern=pattern, string=input_string, flags=re.DOTALL)

    queries = ""
    for m in match:
        query = m.replace("python", "").strip()
        queries += query + "\n"
    return queries


# 応答を抜き出す関数（LLMエージェント用）
def extract_boxed(input_string: str) -> list:
    """
    \\boxed{...} 内の回答を抽出
    """
    pattern = r"\\boxed\{.*?\}"
    matches = re.findall(pattern=pattern, string=input_string)
    return [m.replace("\\boxed{", "").replace("}", "") for m in matches]


# エージェント・プロンプト定義 ---------------------------

# ＜ポイント＞
# - 解法を3パターン設定することでLLMに選択権を委ねている
# - boxedに回答を格納する際に余計なものが入らないようにプロンプトで牽制

# プロンプト
INITIAL_PROMPT = """\
Pythonを使って数学の問題を解いてみましょう。

クエリ要件：
常に出力には'print'関数を使用し、小数ではなく分数や根号形式を使用してください。
sympyなどのパッケージを利用しても構いません。
以下のフォーマットに従ってコードを書いてください。
```python
# あなたのコード
```

まず、問題を解くための主な考え方を述べてください。
問題を解くためには以下の3つの方法から選択できます：
ケース1：問題が直接Pythonコードで解決できる場合、プログラムを書いて解決してください。必要に応じてすべての可能な配置を列挙しても構いません。
ケース2：問題が主に推論で解決できる場合、自分で直接解決してください。
ケース3：上記の2つの方法では対処できない場合、次のプロセスに従ってください：

ケース3のプロセス：
1. 問題をステップバイステップで解決する（ステップを過度に細分化しないでください）。
2. Pythonを使って問い合わせることができるクエリ（計算や方程式など）を取り出します。
3. 結果を私に教えてください。
4. 結果が正しいと思う場合は続行してください。結果が無効または予期しない場合は、クエリまたは推論を修正してください。

注意事項：
すべてのクエリが実行され、答えを得た後、答えを \\boxed{{}} に入れてください。
答え以外、例えば変数を\\boxed{{}}に入れたり、\\boxed{{}}を単体で使用しないで下さい。
\\boxed{{}}の有無で答えが出たかを管理しています。
最終的な答えが出た時以外は、\\boxed{{}}を使用しないでください。
回答が得られた場合は、シンプルに表示して下さい。
追加の出力などはしないでください。

問題文：{problem}
"""


# エージェント定義 -----------------------------------

# ＜ユーザープロキシエージェント＞
# - 開始処理と再帰処理で処理を分岐する
# - 開始処理では問題解決用のプロンプト(INITIAL_PROMPT)を読み込む
# - 再帰処理ではLLMエージェントのメッセージを受け取ってPythonコードを実行する

# ＜LLMエージェント＞
# - ユーザープロキシエージェントの指示に基づいてLLMに問い合わせる
#   --- LLMは計算プロセスを順序立てた文章で返してくれる
# - 結果を格納した"boxed"の箇所を抽出する
# - Stateクラスの形式に合わせてユーザープロキシエージェントに出力する


# ユーザープロキシエージェント
def user_proxy_agent(state: State) -> dict:
    """
    最初の入力またはコード実行を担当
    """
    if state["first_flag"]:
        message = INITIAL_PROMPT.format(problem=state["problem"])
    else:
        last_message = state["messages"][-1].content
        code = extract_code(input_string=last_message)
        if code:
            message = repl.run(command=code)
        else:
            message = "続けてください。クエリが必要になるまで問題を解き続けてください。（答えが出た場合は、\\boxed{{}} に入れてください。）"
    return {"messages": [HumanMessage(content=message)], "first_flag": False}


# LLMエージェント
def llm_agent(state: State) -> dict:
    """
    LLMに思考を進めさせ、boxedがあれば終了
    """
    message = llm.invoke(input=state["messages"])
    content = message.content
    boxed = extract_boxed(input_string=content)
    return {"messages": [message], "end_flag": bool(boxed)}


# グラフ構築 ---------------------------------------------

# ＜ポイント＞
# - 条件付エッジを設定することで再帰的な処理を実現する
# - ユーザープロキシエージェントがLLMエージェントに問題の解法を出力する
# - LLM1エージェントの出力に合わせてユーザープロキシエージェントが事前に決められてたプロンプトを出力する


# グラフ初期化
graph_builder = StateGraph(state_schema=State)

# ノード追加
graph_builder.add_node(node="llm_agent", action=llm_agent)
graph_builder.add_node(node="user_proxy_agent", action=user_proxy_agent)

# エッジ追加
graph_builder.add_edge(start_key=START, end_key="user_proxy_agent")
graph_builder.add_edge(start_key="user_proxy_agent", end_key="llm_agent")

# 条件付エッジの設定
graph_builder.add_conditional_edges(
    source="llm_agent",
    path=lambda state: state["end_flag"],
    path_map={True: END, False: "user_proxy_agent"},
)

# コンパイル
graph = graph_builder.compile()

# グラフ表示
display(Image(graph.get_graph().draw_mermaid_png()))


# 実行 -------------------------------------------------

# ＜正解＞
# - 1890円


# 質問
problem = """
問題: 
偽の金塊は、コンクリートの立方体を金色のペイントで覆うことによって作られます。
ペイントのコストは立方体の表面積に比例し、コンクリートのコストは体積に比例します。
1インチの立方体を作るコストが130円であり、
2インチの立方体を作るコストが680円であるとき、
3インチの立方体を作るコストはいくらになりますか？
"""

for event in graph.stream(input={"problem": problem, "first_flag": True}):
    for value in event.values():
        value["messages"][-1].pretty_print()
