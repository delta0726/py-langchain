"""
Title   : Langchain完全入門
Section : 3 Retrieval
Theme   : Wikipedia Retriverを使ったテキスト取得
Date    : 2025/04/29
Page    : P142
"""

from langchain.retrievers import WikipediaRetriever

# Retrievalの定義
retriever = WikipediaRetriever(lang="ja", doc_content_chars_max=100, top_k_results=1)

# 問い合わせ1
# --- 正常に回答する
query1 = "バーボンウイスキーとは何ですか？"
documents1 = retriever.get_relevant_documents(query=query1)
print(documents1)

# 問い合わせ1
# --- 正常に回答できない
# --- キーワードが曖昧なため類似する文書の視点がズレた
query2 = "私はラーメンが好きです。ところでバーボンウイスキーとは何ですか？"
documents2 = retriever.get_relevant_documents(query=query1)
print(documents2)
