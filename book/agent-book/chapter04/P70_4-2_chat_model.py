"""
Title   : LangChainとLangGraphによるRAG・AIエージェント実践入門
Chapter : 4 LangChainの基礎
Section : 2 LLM/Chat Model
Theme   : Chat Model
Date    : 2025/05/14
Page    : P70
"""

# ＜ポイント＞
# - LangChainの｢ChatModel｣は単独のLLMではなく、複数のメッセージをやり取りすることができる
#   --- これは、AIが過去の会話の記憶を持つことを意味する
# - 会話の主体をSystemMessage, HumanMessage, AIMessageの3つのメッセージで定義する
# - AIMessageを使うことでAIの会話をユーザー側でコントロールすることができる

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

# LLMの定義
model = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# メッセージ
messages = [
    SystemMessage(content="You are a helpful assistant."),
    HumanMessage(content="こんにちは！私はジョンと言います"),
    AIMessage(content="こんにちは、ジョンさん！どのようにお手伝いできますか？"),
    HumanMessage(content="私の名前がわかりますか？"),
]

# 問い合わせ
ai_message = model.invoke(input=messages)

# 結果表示
print(ai_message.content)
