"""
Title   : Langchain完全入門
Section : 3 Retrieval
Theme   : DBからの類似度の高い文書の取得
Date    : 2025/04/27
Page    : P110
"""

from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma


# 大規模言語モデルの構築
embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")

# DB定義
database = Chroma(persist_directory=".data", embedding_function=embeddings)

# データベースから類似度の高いドキュメントを取得
documents = database.similarity_search(query="飛行車の最高速度は？")

# 確認
# --- ドキュメントの数を表示
print(f"ドキュメントの数: {len(documents)}")

# 確認
# --- ドキュメントの内容を表示
for idx, document in enumerate(iterable=documents, start=1):
    print(f"[NO{idx}] ドキュメントの内容: {document.page_content}")
