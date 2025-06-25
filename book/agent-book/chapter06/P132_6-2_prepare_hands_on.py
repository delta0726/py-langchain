"""
Title   : LangChainとLangGraphによるRAG・AIエージェント実践入門
Chapter : 6 Advanced RAG
Section : 2 ハンズオンの準備
Theme   : Gitリポジトリからドキュメントをロードし、ChromaDBに格納する
Date    : 2025/06/09
Page    : P132-134
"""

import os
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import GitLoader
from langchain.vectorstores import Chroma


# Gitリポジトリからドキュメントをロード ----------------------------------------------

# ＜ポイント＞
# - GitHubのLangChainリポジトリをクローンして、ドキュメントを取得する
# - ファイル数が多いのでmcxファイルのみを対象とする


# 関数定義
def file_filter(file_path: str) -> bool:
    return file_path.endswith(".mdx")


# ローダー定義
loader = GitLoader(
    clone_url="https://github.com/langchain-ai/langchain",
    repo_path="./langchain",
    branch="master",
    file_filter=file_filter,
)

# ドキュメントのロード
# --- lagnchainフォルダをクローンしている
documents = loader.load()
print(len(documents))


# ドキュメントのベクトル化とデータベースの構築 ------------------------------------------

# ＜ポイント＞
# - ChromaDBを使用してドキュメントをベクトル化しデータベースを構築する
# - OpenAIの埋め込みモデルを使用する
# - 永続化ディレクトリを指定して、DBを保存する


# Chromaの永続化用ディレクトリ指定
persist_dir = "./chroma_langchain"

# 埋め込みモデルの定義
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

# DB構築
# --- DBが保存されていればロード
# --- DBが保存されていなければDB構築＆保存(永続化)
if os.path.exists(path=persist_dir):
    db = Chroma(persist_directory=persist_dir, embedding_function=embeddings)
    print("Loaded existing Chroma DB from disk")
else:
    db = Chroma.from_documents(
        documents=documents, embedding=embeddings, persist_directory=persist_dir
    )
    #
    db.persist()
    print("Built and persisted new Chroma DB")


# RAGによる問い合わせ ------------------------------------------------------

# ＜ポイント＞
# - LangChainのRAG機能を使用して、ドキュメントから情報を取得する
# - Retrieverを使用して関連するコンテキストを取得しLLMに問い合わせる

# プロンプト
prompt = ChatPromptTemplate.from_template(
    template='''\
以下の文脈だけを踏まえて質問に回答してください。

文脈: """
{context}
"""

質問: {question}
'''
)

# LLMモデル
model = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# リトリーバー定義
retriever = db.as_retriever()

# チェーン構築
chain = (
    {
        "question": RunnablePassthrough(),
        "context": retriever,
    }
    | prompt
    | model
    | StrOutputParser()
)

# 問い合わせ
chain.invoke("LangChainの概要を教えて")
