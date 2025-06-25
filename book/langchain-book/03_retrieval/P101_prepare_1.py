"""
Title   : Langchain完全入門
Section : 3 Retrieval
Theme   : PDFファイルの読み込み
Date    : 2025/04/27
Page    : P101
"""

from langchain.document_loaders import PyMuPDFLoader


# PDFの読み込み
loader = PyMuPDFLoader(file_path="pdf/sample.pdf")
documents = loader.load()

# データ確認
# --- ドキュメントの数を確認する
# --- 1つめのドキュメントの内容/メタデータを確認する
print(f"ドキュメントの数: {len(documents)}")
print(f"1つめのドキュメントの内容: {documents[0].page_content}")
print(f"1つめのドキュメントのメタデータ: {documents[0].metadata}")
