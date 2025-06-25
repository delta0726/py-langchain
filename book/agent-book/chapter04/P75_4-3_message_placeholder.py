"""
Title   : LangChainとLangGraphによるRAG・AIエージェント実践入門
Chapter : 4 LangChainの基礎
Section : 3 Prompt Template
Theme   : メッセージ・プレースホルダー
Date    : 2025/05/14
Page    : P74
"""

# ＜ポイント＞
# - プレースホルダとは後から値や文字を入力できるように一時的に格納する値や文字を指す
# - MessagesPlaceholderはチャット履歴をプレースホルダとして格納する
#   --- 過去の記憶に基づくチャットを行う場合の標準的なソリューション

from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder


# テンプレート定義
# --- MessagesPlaceholderのvariable_nameでチャット履歴を受け取る
prompt = ChatPromptTemplate.from_messages(
    messages=[
        ("system", "You are a helpful assistant."),
        MessagesPlaceholder(variable_name="chat_history", optional=True),
        ("human", "{input}"),
    ]
)

# プロンプト呼び出し
prompt_value = prompt.invoke(
    input={
        "chat_history": [
            HumanMessage(content="こんにちは！私はジョンと言います！"),
            AIMessage(content="こんにちは、ジョンさん！どのようにお手伝いできますか？"),
        ],
        "input": "私の名前が分かりますか？",
    }
)

# 結果表示
print(prompt_value)
