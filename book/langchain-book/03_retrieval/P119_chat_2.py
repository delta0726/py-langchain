"""
Title   : Langchain完全入門
Section : 3 Retrieval
Theme   : Chainlitで独自文書に基づく回答を得る
Date    : 2025/04/29
Page    : P119
"""

import chainlit as cl
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.prompts import PromptTemplate
from langchain.schema import HumanMessage
from langchain.vectorstores import Chroma

"""
<Chatlitの起動>
- 当ファイルのカレントディレクトリでターミナルを起動
- chainlit run .\P119_chat_2.py
- 質問：飛行車の最高速度は？
"""


# 準備 ---------------------------------------------------------

# モデル構築
# --- 文章をベクトルに変換して類似度比較できるようにするモデル
# --- 回答生成用のチャットモデル
embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")
chat = ChatOpenAI(model="gpt-4o-mini")

# プロンプト作成
# --- 変数を使用したテンプレート
prompt = PromptTemplate(
    template="""文章を元に質問に答えてください。 

文章: 
{document}

質問: {query}
""",
    input_variables=["document", "query"],
)


# DB接続
database = Chroma(persist_directory="./.data", embedding_function=embeddings)


# Chainlit ------------------------------------------------------

# プロンプト作成
# --- 変数を使用したテンプレート
@cl.on_chat_start
async def on_chat_start():
    await cl.Message(content="準備ができました！メッセージを入力してください！").send()


# ユーザー入力への応答
@cl.on_message
async def on_message(input_message):
    # 入力されたメッセージ(input_message)を受け取る
    print("入力されたメッセージ: " + input_message.content)
    user_message = input_message.content

    # DBから類似文書を検索
    documents = database.similarity_search(user_message)

    # 類似文書の格納
    documents_string = ""
    for document in documents:
        documents_string += f"""
    ---------------------------
    {document.page_content}
    """

    # 問い合わせ
    result = chat(
        [
            HumanMessage(
                content=prompt.format(document=documents_string, query=user_message)
            )
        ]
    )

    # 回答表示
    await cl.Message(content=result.content).send()
