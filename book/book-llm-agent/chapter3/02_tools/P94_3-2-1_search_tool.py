"""
Title   : やさしく学ぶLLMエージェント
Chapter : 3 エージェント
Section : 2 LLLMにツールを与える 
Theme   : 検索ツール
Date    : 2025/07/17
Page    : P94-97
"""

from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage
from langchain.agents import load_tools


# 準備 -------------------------------------------------------

# モデル定義
model = ChatOpenAI(model="gpt-4o-mini")

# 質問定義
question = """
株式会社Elithの住所を教えてください。
最新の公式情報として公開されているものを教えてください。
"""

# LLMが知らない知識を含む質問 ----------------------------------

# ＜ポイント＞
# - LLMの知識が追い付いていないのか、LLMのポリシーで答えないのかは不明だが正当は出ない


# 問い合わせ
result = model.invoke(input=[HumanMessage(content=question)])

# 結果確認
print(result.content)


# LLMに検索ツールを持たせて質問 ---------------------------------

# ＜ポイント＞
# - LLMに検索ツールを持たせてWeb検索をさせることで知識不足に対処する
# - LLMにツール選択と使い方の検討をさせて、その情報に基づいて実際に検索している


# ツール
# --- ツールを持たせる（今回は'serpapi'のみ）
tools = load_tools(tool_names=["serpapi"], llm=model)
model_with_tools = model.bind_tools(tools=tools)

# ツール選択
# --- 質問に対して必要なツールを選択
# --- ツールで質問の回答を得るためのパラメータ(検索キーワード)を提示
response = model_with_tools.invoke(input=[HumanMessage(content=question)])

# 結果確認
# --- コンテンツは何も入っていない
# --- 使用するツールと検索キーワードが提示されている
print(f"ContentString: {response.content}")
print(f"ToolCalls: {response.tool_calls}")

# 検索ツールで問い合わせ
search_tool = tools[0]
search_result = search_tool.invoke(input=response.tool_calls[0]["args"])

# 検索結果の確認
print(search_result)
