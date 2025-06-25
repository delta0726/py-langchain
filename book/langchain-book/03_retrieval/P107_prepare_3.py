"""
Title   : Langchain完全入門
Section : 3 Retrieval
Theme   : PDF生データをテキスト分割してDB化
Date    : 2025/04/27
Page    : P107
"""

import os
import shutil

from langchain.document_loaders import PyMuPDFLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import SpacyTextSplitter
from langchain.vectorstores import Chroma


# PDFの読み込み
loader = PyMuPDFLoader(file_path="pdf/sample.pdf")
documents = loader.load()

# PDFの分割
text_splitter = SpacyTextSplitter(chunk_size=300, pipeline="ja_core_news_sm")
splitted_documents = text_splitter.split_documents(documents=documents)

# 言語モデルの構築
# --- ベクトル化するための言語モデル
embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")

# DB削除
# --- 複数実行すると同じデータが重複登録される
if os.path.exists(path=".data"):
    shutil.rmtree(".data")

# DB構築
# --- ベクトル化するためのモデルを指定
database = Chroma(persist_directory=".data", embedding_function=embeddings)

# DB格納
database.add_documents(documents=splitted_documents)

# 確認
print("データベースの作成が完了しました。")
