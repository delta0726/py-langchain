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
#   --- プロセスの簡素化に寄与する

# ＜限界＞
# - エージェントが会話の文脈や過去の相互作用を記憶できない
# - 過去の質問で提供した情報や回答に基づいて次の質問を調整することができない（一貫性が維持できない）
#   --- メモリ機能を持つエージェントを使用することで改善可能
#   --- 実際のエージェント開発ではLangGraphを用いる実装が主流


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
tools = load_tools(tool_names=["serpapi"], llm=model)
agent = create_react_agent(llm=model, tools=tools, prompt=prompt)

# エージェント実行環境の構築
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# 問い合わせ
search_response = agent_executor.invoke(
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
