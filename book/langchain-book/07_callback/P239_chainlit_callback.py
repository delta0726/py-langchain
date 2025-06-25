"""
Title   : Langchain完全入門
Section : 7 Callbacks - さまざまなイベント発生時に処理を行う
Theme   : 
Date    : 2025/04/30
Page    : P239
"""


import chainlit as cl
from langchain.agents import AgentType, initialize_agent, load_tools
from langchain.chat_models import ChatOpenAI

"""
<Chatlitの起動>
- 当ファイルのカレントディレクトリでターミナルを起動
- chainlit run .\P239_chainlit_callback.py
"""


# 言語モデルの定義
llm = ChatOpenAI(temperature=0, model="gpt-4o-mini")

# ツール定義
tools = load_tools(tool_names=["serpapi"])

# エージェント定義
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
)


@cl.on_chat_start
async def on_chat_start():
    await cl.Message(content="Agentの初期化が完了しました").send()


@cl.on_message
async def on_message(input_message):
    # Agentを実行する
    result = agent.run(
        input_message,
        callbacks=[
            cl.LangchainCallbackHandler()
        ],
    )
    await cl.Message(content=result).send()
