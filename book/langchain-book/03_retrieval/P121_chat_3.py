"""
Title   : Langchain完全入門
Section : 3 Retrieval
Theme   : ChainlitにPDFを与えてDB作成後に質問して回答を得る
Date    : 2025/04/29
Page    : P121
"""

import os
import uuid
import chainlit as cl
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import PyMuPDFLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.prompts import PromptTemplate
from langchain.schema import HumanMessage
from langchain.text_splitter import SpacyTextSplitter
from langchain.vectorstores import Chroma


"""
<Chatlitの起動>
- 当ファイルのカレントディレクトリでターミナルを起動
- chainlit run .\P121_chat_3.py
- PDF：pdf/sampleを登録
- 質問：飛行車の最高速度は？
"""

# モデル構築
# --- 文章をベクトルに変換して類似度比較できるようにするモデル
# --- 回答生成用のチャットモデル
embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")
chat = ChatOpenAI(model="gpt-4o-mini")

# プロンプト定義
# --- 変数を使用したテンプレート
prompt = PromptTemplate(
    template="""文章を元に質問に答えてください。 

文章: 
{document}

質問: {query}
""",
    input_variables=["document", "query"],
)

# 分割器の定義
text_splitter = SpacyTextSplitter(chunk_size=300, pipeline="ja_core_news_sm")


# Chainlitのルーティーン -------------------------------------------


@cl.on_chat_start
async def on_chat_start():
    files = None
    while files is None:
        files = await cl.AskFileMessage(
            content="PDFを選択してください",
            accept=["application/pdf"],
            max_size_mb=20,
            raise_on_timeout=False,
        ).send()

    file = files[0]

    # 仮保存されているファイルパスを取得
    uploaded_file_path = file.path

    # ファイルが存在するかチェック
    if not os.path.exists(uploaded_file_path):
        raise FileNotFoundError(f"ファイルが存在しません: {uploaded_file_path}")

    # ファイルの読み込み
    documents = PyMuPDFLoader(file_path=uploaded_file_path).load()
    splitted_documents = text_splitter.split_documents(documents=documents)

    # データベース作成
    database = Chroma(embedding_function=embeddings)
    database.add_documents(documents=splitted_documents)
    cl.user_session.set(key="database", value=database)

    await cl.Message(
        content=f"`{file.name}` の読み込みが完了しました。質問を入力してください。"
    ).send()


@cl.on_message
async def on_message(input_message):
    # ユーザーのメッセージ取得
    user_message = input_message.content
    print(f"入力されたメッセージ: {user_message}")

    # DB処理
    # --- セッションからデータベースを取得
    # --- 類似文書を検索
    database = cl.user_session.get("database")
    documents = database.similarity_search(user_message)

    # 類似文書をまとめて1つの文字列にする
    documents_string = "\n".join(
        f"---------------------------\n{doc.page_content}" for doc in documents
    )

    # 問い合わせ
    # --- プロンプトの作成
    # --- 回答結果の取得
    formatted_prompt = prompt.format(document=documents_string, query=user_message)
    result = chat([HumanMessage(content=formatted_prompt)])

    # モデルからの回答を送信
    await cl.Message(content=result.content).send()
