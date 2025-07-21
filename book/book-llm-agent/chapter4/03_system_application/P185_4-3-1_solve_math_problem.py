"""
Title   : やさしく学ぶLLMエージェント
Chapter : 4 マルチエージェント
Section : 3 マルチエージェントの活用
Theme   : 数学の問題を解かせよう
Date    : 2025/07/21
Page    : P185-201
"""

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


repl = PythonREPL()
llm = ChatOpenAI(model="gpt-4o-mini")


class State(TypedDict):
    messages: Annotated[list, add_messages]
    problem: str
    first_flag: bool
    end_flag: bool


# ユーティリティ関数 ----------------------------------


def extract_code(input_string: str) -> str:
    """```で囲まれたコード部分を抽出"""
    pattern = r"```(.*?)```"
    match = re.findall(pattern, input_string, flags=re.DOTALL)

    queries = ""
    for m in match:
        query = m.replace("python", "").strip()
        queries += query + "\n"
    return queries


def extract_boxed(input_string: str) -> list:
    """\\boxed{...} 内の回答を抽出"""
    pattern = r"\\boxed\{.*?\}"
    matches = re.findall(pattern, input_string)
    return [m.replace("\\boxed{", "").replace("}", "") for m in matches]


# エージェント定義 -----------------------------------

# エージェント・プロンプト
INITIAL_PROMPT = """\
Pythonを使って数学の問題を解いてみましょう。

クエリ要件：
常に出力には'print'関数を使用し、小数ではなく分数や根号形式を使用してください。
sympyなどのパッケージを利用しても構いません。
以下のフォーマットに従ってコードを書いてください。
```python
# あなたのコード
```

まず、問題を解くための主な考え方を述べてください。問題を解くためには以下の3つの方法から選択できます：
ケース1：問題が直接Pythonコードで解決できる場合、プログラムを書いて解決してください。必要に応じてすべての可能な配置を列挙しても構いません。
ケース2：問題が主に推論で解決できる場合、自分で直接解決してください。
ケース3：上記の2つの方法では対処できない場合、次のプロセスに従ってください：
1. 問題をステップバイステップで解決する（ステップを過度に細分化しないでください）。
2. Pythonを使って問い合わせることができるクエリ（計算や方程式など）を取り出します。
3. 結果を私に教えてください。
4. 結果が正しいと思う場合は続行してください。結果が無効または予期しない場合は、クエリまたは推論を修正してください。

すべてのクエリが実行され、答えを得た後、答えを \\boxed{{}} に入れてください。
答え以外、例えば変数を\\boxed{{}}に入れたり、\\boxed{{}}を単体で使用しないで下さい。
\\boxed{{}}の有無で答えが出たかを管理しています。最終的な答えが出た時以外は、\\boxed{{}}を使用しないでください。
回答が得られた場合は、シンプルに表示して下さい。追加の出力などはしないでください。

問題文：{problem}
"""


# ユーザープロキシエージェント
def user_proxy_agent(state: State) -> dict:
    """最初の入力またはコード実行を担当"""
    if state["first_flag"]:
        message = INITIAL_PROMPT.format(problem=state["problem"])
    else:
        last_message = state["messages"][-1].content
        code = extract_code(last_message)
        if code:
            message = repl.run(code)
        else:
            message = "続けてください。クエリが必要になるまで問題を解き続けてください。（答えが出た場合は、\\boxed{{}} に入れてください。）"
    return {"messages": [HumanMessage(message)], "first_flag": False}


# LLMエージェント
def llm_agent(state: State) -> dict:
    """LLMに思考を進めさせ、boxedがあれば終了"""
    message = llm.invoke(state["messages"])
    content = message.content
    boxed = extract_boxed(content)
    return {"messages": [message], "end_flag": bool(boxed)}


# グラフ構築 ---------------------------------------------

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

# 質問
problem = """\
問題: 偽の金塊は、コンクリートの立方体を金色のペイントで覆うことによって作られます。
ペイントのコストは立方体の表面積に比例し、コンクリートのコストは体積に比例します。
1インチの立方体を作るコストが130円であり、2インチの立方体を作るコストが680円であるとき、
3インチの立方体を作るコストはいくらになりますか？
"""

for event in graph.stream({"problem": problem, "first_flag": True}):
    for value in event.values():
        value["messages"][-1].pretty_print()
