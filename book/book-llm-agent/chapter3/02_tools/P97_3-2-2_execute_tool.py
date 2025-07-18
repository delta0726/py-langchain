"""
Title   : やさしく学ぶLLMエージェント
Chapter : 3 エージェント
Section : 2 LLLMにツールを与える
Theme   : プログラム実行ツール
Date    : 2025/07/18
Page    : P97-100
"""

# ＜概要＞
# - LLMは数値演算を直接的に行うわけではないので基本的にできない
# - その場合はPythonなどの演算機能でツール経由で利用することで解決する


from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage
from langchain_experimental.tools.python.tool import PythonREPLTool

# 質問内容
question = """
以下をPythonで実行した場合の結果を教えてください。
print(1873648 + 9285928 + 3759182 + 2398597)
"""

# モデル定義
model = ChatOpenAI(model="gpt-4o-mini")

# ツールをモデルにバインド
# --- PythonREPLはLangChainが提供するPythonコードを動的に実行するツール
python_tool = PythonREPLTool()
model_with_tools = model.bind_tools(tools=[python_tool])

# モデルに質問を送信
# --- ツール呼び出しを含む応答が返る
response = model_with_tools.invoke(input=[HumanMessage(content=question)])

# 結果確認
# --- コンテンツは何も入っていない
# --- 使用するツールと検索キーワードが提示されている
print(f"[LLM Output] content: {response.content}")
print(f"[LLM Output] tool_calls: {response.tool_calls}")

# ツール実行
# --- 事前に得たツール選択とインプット情報に基づいてLLMが処理を実行
tool_args = response.tool_calls[0]["args"]
result = python_tool.invoke(tool_args)
print(f"[Python Execution Result] {result}")

# 正解値（人間による確認用）
expected = 1873648 + 9285928 + 3759182 + 2398597
print(f"[Expected Answer] {expected}")
