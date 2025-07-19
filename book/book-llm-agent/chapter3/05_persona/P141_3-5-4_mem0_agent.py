"""
Title   : やさしく学ぶLLMエージェント
Chapter : 3 エージェント
Section : 5 ペルソナのあるエージェント
Theme   : mem0を用いたエージェント
Date    : 2025/07/19
Page    : P141-147
"""

import os
from mem0 import MemoryClient
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain.agents import load_tools, AgentExecutor, create_react_agent

# --- 1. Mem0クライアント初期化とメモリ削除 ---
# ユーザID指定してメモリを初期化（すべて削除）
user_id = "elith_chan"
client = MemoryClient(api_key=os.environ['MEM0_API_KEY'])
client.delete_all(user_id=user_id)
print("User memories deleted.")

# --- 2. 翻訳用チェーンの準備 ---
# 翻訳プロンプトを定義し、ChatOpenAIモデルと連結
translation_message = """
Translate the following text into {language}.

text:
{text}
"""
translate_prompt = ChatPromptTemplate.from_messages([("human", translation_message)])
model = ChatOpenAI(model="gpt-4o-mini")
translate_chain = translate_prompt | model
print("Translation chain prepared.")

# --- 3. エージェント用プロンプトテンプレート定義（ペルソナ込み） ---
input_vars = ['agent_scratchpad', 'input', 'tool_names', 'tools', 'chat_history']
persona_template = """\
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
Thought:{agent_scratchpad}"""
prompt = PromptTemplate(input_variables=input_vars, template=persona_template)
print("Agent prompt template created.")

# --- 4. ツールのロードとエージェント初期化 ---
tools = load_tools(["serpapi"], llm=model)
agent = create_react_agent(model, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)
print("Agent initialized.")

# --- 5. 日本語クエリの翻訳、メモリ検索、エージェント応答 ---
query_ja = "あなたのお仕事は何ですか？"
language = "English"

# 日本語を英語に翻訳
query_en = translate_chain.invoke({"text": query_ja, "language": language}).content

# 翻訳したクエリでメモリ検索
memory = client.search(query_en, user_id=user_id)

# エージェントに入力して回答取得
response = agent_executor.invoke({"input": query_ja, "chat_history": memory})
print("Agent response:", response["output"])

# --- 6. ペルソナの特徴を英語に翻訳し、メモリに追加 ---
persona_text_ja = "私、えりすちゃんは「〜エリ！」という語尾を使います。「今日も頑張るエリ！」が口癖です。"
persona_text_en = translate_chain.invoke({"text": persona_text_ja, "language": language}).content

messages = [{"role": "user", "content": persona_text_en}]
client.add(messages, user_id=user_id)
print("Persona info added to memory.")
