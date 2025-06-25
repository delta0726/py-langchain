"""
Title   : Langchain完全入門
Section : 3 Retrieval
Theme   : PDF生データのテキスト分割
Date    : 2025/04/27
Page    : P105
"""

from langchain.document_loaders import PyMuPDFLoader
from langchain.text_splitter import SpacyTextSplitter

# PDFの読み込み
loader = PyMuPDFLoader(file_path="pdf/sample.pdf")
documents = loader.load()

# インスタンス構築
# --- ja_core_news_smを使用
# --- 300文節以内にまとめる
text_splitter = SpacyTextSplitter(chunk_size=300, pipeline="ja_core_news_sm")

# ドキュメントを分割
splitted_documents = text_splitter.split_documents(documents=documents)

# 確認
print(f"分割前のドキュメント数: {len(documents)}")
print(f"分割後のドキュメント数: {len(splitted_documents)}")
