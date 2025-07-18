"""
Title   : やさしく学ぶLLMエージェント
Chapter : 3 エージェント
Section : 3 複雑なワークフローで推論するエージェント
Theme   : エージェントによるWeb検索
Date    : 2025/07/17
Page    : P115-117
"""

# ＜概要＞
# - エージェントを使ってserpapiでWeb検索で回答を得る
# - ツール選択や引数設定のための事前質問をすることなく実現できている
#   --- エージェントはプロセスの簡素化に寄与する


from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage
from langchain.agents import AgentExecutor, create_react_agent
from langchain.agents import load_tools
from langchain import hub


# プロンプトの取得
# --- ReAct専用のプロンプト
# --- https://smith.langchain.com/hub/hwchase17/react
prompt = hub.pull("hwchase17/react")
print(prompt.template)


# エージェント構築
model = ChatOpenAI(model="gpt-4o-mini")
search_tools = load_tools(tool_names=["serpapi"], llm=model)
search_agent = create_react_agent(llm=model, tools=search_tools, prompt=prompt)
search_agent_executor = AgentExecutor(
    agent=search_agent, tools=search_tools, verbose=True
)

# 問い合わせ
search_response = search_agent_executor.invoke(
    {
        "input": [
            HumanMessage(
                content="株式会社Elithの住所を教えてください。最新の公式情報として公開されているものを教えてください。"
            )
        ]
    }
)

# 結果確認
print(search_response)
