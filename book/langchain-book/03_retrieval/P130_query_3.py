"""
Title   : Langchain完全入門
Section : 3 Retrieval
Theme   : RetrivalQAを使ったシステム構築
Date    : 2025/04/29
Page    : P130
"""

from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma


# インスタンス構築
# --- チャットモデル
# --- 埋め込みモデル
llm = ChatOpenAI(model="gpt-4o-mini")
embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")

# データベースの定義
# --- 埋め込みモデルを指定して類似度検索に対応
database = Chroma(persist_directory=".data", embedding_function=embeddings)

# モデル構築
# --- データベースをRetrieverに変換
# --- RetrievalQAの構築
retriever = database.as_retriever()
qa = RetrievalQA.from_llm(llm=llm, retriever=retriever, return_source_documents=True)

# 質問を入力して結果を取得
result = qa("飛行車の最高速度を教えて")

# 結果を表示
print(result["result"])
print(result["source_documents"])
