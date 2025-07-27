"""
Title   : LangChainとLangGraphによるRAG・AIエージェント実践入門
Chapter : 7 LangSmithを使ったRAGアプリケーションの評価
Section : 4 Ragasによる合成テストデータの生成
Theme   : langchainフォルダの作成
Date    : 2025/06/29
Page    : P161
"""

from langchain_community.document_loaders import GitLoader


# 抽出関数
def file_filter(file_path: str) -> bool:
    return file_path.endswith(".mdx")

# ローダー定義
loader = GitLoader(
    clone_url="https://github.com/langchain-ai/langchain",
    repo_path="./langchain",
    branch="langchain==0.2.13",
    file_filter=file_filter,
)

# ドキュメントのロード
documents = loader.load()
