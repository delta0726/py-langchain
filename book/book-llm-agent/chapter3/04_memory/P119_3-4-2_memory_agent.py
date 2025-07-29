"""
Title   : やさしく学ぶLLMエージェント
Chapter : 3 エージェント
Section : 4 記憶を持つエージェント
Theme   : LLMエージェントへの記憶の実装
Date    : 2025/07/19
Page    : P119-128
"""


# ＜概要＞
# - プロンプトに過去のチャット履歴を渡すことでLLMエージェントに記憶を持たせる
#   --- トークン数の制限に直面しやすい
#   --- 会話履歴が増えると検索効率も潜在的に下がり、LLMコストも上昇
# - コンバセーショナルバッファを使用すると最近の会話履歴のみを保持し、古い履歴は削除される
#   ---長期的な記憶、複雑な文脈に対応できない

from langchain_core.prompts import PromptTemplate
from langchain.memory import ChatMessageHistory
from langchain_openai import ChatOpenAI
from langchain.agents import load_tools, AgentExecutor, create_react_agent
from langchain_core.runnables.history import RunnableWithMessageHistory


# プロンプトテンプレートの定義 -----------------------------------------

# ＜ポイント＞
# - ReActエージェントのプロンプトテンプレートを定義する
# - {chat_history}をプロンプト内に追加している
#   --- プロンプトで記憶を参照できるようにする
# - {agent_scratchpad}はエージェントの思考過程を記録するための変数
#   --- これにより、エージェントがどのように結論に至ったかを追跡できる


template = """
Answer the following questions as best you can. You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Previous conversation history: {chat_history}
Question: {input}
Thought:{agent_scratchpad}
"""

# テンプレートの作成
input_variables = ["agent_scratchpad", "input", "tool_names", "tools"]
prompt = PromptTemplate(input_variables=input_variables, template=template)


# 関数定義：チャット履歴の管理 ------------------------------------------

# ＜ポイント＞
# - セッションごとにチャット履歴を管理するための関数を定義する
# - チャット履歴自体はstoreという辞書で管理する
# - 辞書にセッションIDをキーとして、ChatMessageHistoryオブジェクトを格納する
#   --- セッションIDで会話内容/会話主体を区別する

# チャット履歴を管理する辞書
store = {}


def get_by_session_id(session_id: str) -> ChatMessageHistory:
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]


# エージェントの構築 ------------------------------------------------

# ＜ポイント＞
# - agent_executorをRunnableWithMessageHistoryでラップして、チャット履歴を管理できるようにする
# - {input}と{chat_history}をラッパーで指定することで情報伝達している


# エージェント定義
model = ChatOpenAI(model="gpt-4o-mini")
tools = load_tools(tool_names=["serpapi"], llm=model)
agent = create_react_agent(llm=model, tools=tools, prompt=prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# 履歴付きラッパー
agent_with_chat_history = RunnableWithMessageHistory(
    runnable=agent_executor,
    get_session_history=get_by_session_id,
    input_messages_key="input",
    history_messages_key="chat_history",
)


# 実行例：セッション1 --------------------------------------------------

# ＜ポイント＞
# - デバッグしてもエージェント内の処理はトレースできない


print("\n--- Session 1: Step 1 ---")
response1 = agent_with_chat_history.invoke(
    input={
        "input": "株式会社Elithの住所を教えてください。最新の公式情報として公開されているものを教えてください。"
    },
    config={"configurable": {"session_id": "test-session1"}},
)

print("\n--- Session 1: Step 2 ---")
response2 = agent_with_chat_history.invoke(
    input={"input": "先ほど尋ねた会社は何の会社ですか？"},
    config={"configurable": {"session_id": "test-session1"}},
)

# 履歴の表示
print("\n=== Chat History: Session 1 ===")
for msg in get_by_session_id(session_id="test-session1").messages:
    print(f"{msg.type}: {msg.content}")


# 実行例：セッション2 --------------------------------------------------

# ＜ポイント＞
# - セッションを変えると過去のチャット履歴が参照されない
#   --- 住所検索のプロセスでWeb検索していないので以下の質問に回答することができない

print("\n--- Session 2: Step 1 ---")
response3 = agent_with_chat_history.invoke(
    {"input": "先ほど尋ねた会社は何の会社ですか？"},
    config={"configurable": {"session_id": "test-session2"}},
)

# 履歴の表示
print("\n--- Session 2: Step 2 ---")
for msg in get_by_session_id(session_id="test-session2").messages:
    print(f"{msg.type}: {msg.content}")
