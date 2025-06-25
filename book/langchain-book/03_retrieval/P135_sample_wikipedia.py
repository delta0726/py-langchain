"""
Title   : Langchain完全入門
Section : 3 Retrieval
Theme   : RetrivalQAを使ったシステム構築
Date    : 2025/04/29
Page    : P135
"""


from langchain.retrievers import WikipediaRetriever


# WikipediaRetrieverを定義
# --- retriverを切り替えることで情報源を変更
retriever = WikipediaRetriever(lang="ja")

# 検索
documents = retriever.get_relevant_documents(query="大規模言語モデル")
print(f"検索結果: {len(documents)}件")

# 結果確認
for document in documents:
    print("---------------取得したメタデータ---------------")
    print(document.metadata) #← メタデータを表示する
    print("---------------取得したテキスト---------------")
    print(document.page_content[:100]) #← テキストの先頭100文字を表示する