"""
Title   : Langchain完全入門
Section : 3 Retrieval
Theme   : Wikipedia Retriverを使ったテキスト取得
Date    : 2025/04/29
Page    : P138
"""

from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.retrievers import WikipediaRetriever


# インスタンス構築
# --- 言語モデルの定義
# --- WikipediaRetrieverを初期化する
llm = ChatOpenAI()

# Retrievalの定義
retriever = WikipediaRetriever(lang="ja", doc_content_chars_max=500, top_k_results=2)

# 検索器の構築
chain = RetrievalQA.from_llm(llm=llm, retriever=retriever, return_source_documents=True)

# 検索器の実行
# --- Wikipediaで調べてきている
result = chain("バーボンウイスキーとは？")

# 情報の取得元のドキュメントを取得する
source_documents = result["source_documents"]

# 検索結果の件数を表示する
print(f"検索結果: {len(source_documents)}件")

# 返答を表示する
for document in source_documents:
    print("---------------取得したメタデータ---------------")
    print(document.metadata)
    print("---------------取得したテキスト---------------")
    print(document.page_content[:100])
print("---------------返答---------------")
print(result["result"])
