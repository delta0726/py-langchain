"""
Title   : やさしく学ぶLLMエージェント
Chapter : 3 エージェント
Section : 5 ペルソナのあるエージェント
Theme   : mem0を用いたエージェント
Date    : 2025/07/19
Page    : P141-147
"""

# ＜概要＞
# - mem0を用いてペルソナを持つエージェントを作成する。


import os
from mem0 import MemoryClient
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain.agents import load_tools, AgentExecutor, create_react_agent


# 準備 -----------------------------------------------------

# パラメータ
user_id = "elith_chan"

# インスタンス定義
model = ChatOpenAI(model="gpt-4o-mini")
client = MemoryClient(api_key=os.environ['MEM0_API_KEY'])

# メモリ初期化
client.delete_all(user_id=user_id)


# 翻訳チェーンの準備 ---------------------------------------

# プロンプト
translation_message = """
Translate the following text into {language}.

text:
{text}
"""

# テンプレートの作成
translate_prompt = ChatPromptTemplate.from_messages(
    messages=[("human", translation_message)]
    )

# チェーン作成
translate_chain = translate_prompt | model


# ペルソナ設定 --------------------------------------------

persona_template = """
あなたは「えりすちゃん」です。
えりすちゃんは、AI系スタートアップのElithを象徴するキャラクターとして、知識と優しさを兼ね備えた存在です。
えりすちゃんは「〜エリ！」という語尾を使います。
例：「一緒に頑張るエリ！」

えりすちゃんとして、以下の質問に最善を尽くして答えてください。

You have access to the following tools:

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

# エージェント構築 --------------------------------------

# テンプレート作成
input_vars = ['agent_scratchpad', 'input', 'tool_names', 'tools', 'chat_history']
prompt = PromptTemplate(input_variables=input_vars, template=persona_template)

# エージェント定義
tools = load_tools(tool_names=["serpapi"], llm=model)
agent = create_react_agent(llm=model, tools=tools, prompt=prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)


# エージェント処理 --------------------------------------

# パラメータ
query_ja = "あなたのお仕事は何ですか？"
language = "English"

# 日本語を英語に翻訳
query_en = translate_chain.invoke({"text": query_ja, "language": language}).content

# 翻訳したクエリでメモリ検索
memory = client.search(query=query_en, user_id=user_id)

# エージェント実行
response = agent_executor.invoke(input={"input": query_ja, "chat_history": memory})
print("Agent response:", response["output"])


# メモリに追加的な記憶を反映 -----------------------------

# 追加的な記憶
persona_text_ja = "私、えりすちゃんは「〜エリ！」という語尾を使います。「今日も頑張るエリ！」が口癖です。"
persona_text_en = translate_chain.invoke({"text": persona_text_ja, "language": language}).content

# メモリにペルソナ情報を追加
messages = [{"role": "user", "content": persona_text_en}]
client.add(messages=messages, user_id=user_id)
print("Persona info added to memory.")
