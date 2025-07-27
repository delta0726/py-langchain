"""
Title   : LangChainとLangGraphによるRAG・AIエージェント実践入門
Chapter : 7 LangSmithを使ったRAGアプリケーションの評価
Section : 3 LangSmithとRagasを使ったオフライン評価の構成例
Theme   : Ragasとは
Date    : 2025/06/29
Page    : P158
"""


# ＜Ragasとは＞
# - Githubでオープンソースとして公開されているRAGの評価フレームワーク
# - 回答結果だけでなく、検索結果についても評価できるのが特徴
# - RAGの評価のためのデータセット生成機能も持つ
# - LangSmithにも類似した機能が実装されている


# ＜評価指標＞
# 1. Faithfulness（忠実度）
# 2. Answer Relevancy（回答の関連性）
# 3. Context Precision（コンテキストの精度）
# 4. Context Recall（コンテキストの再現率）


# ＜Faithfulness（忠実度）＞
# - 生成物が事実に基づいて回答を生成しているかを評価する指標
# - ハルシネーションを起こしていないかを評価する重要な指標


# ＜Answer Relevancy（回答の関連性）＞
# - 生成物が質問に対して適切かどうかを評価する指標
# - 質問の答えとして的を得ているか


# ＜Context Precision（コンテキストの精度）＞
# - 質問のコンテキスト（文脈）に沿った情報の検索精度を評価する指標
# - 余計な情報を含まず、回答に関する純度が高いと精度が高いと評価する


# ＜Context Recall（コンテキストの再現率）＞
# - 質問のコンテキスト（文脈）に沿った情報の検索再現率を評価する指標
# - 質問に対して必要な情報をすべて網羅できているかどうか


# ＜参考資料＞
# https://zenn.dev/umi_mori/books/llm-rag-langchain-python/viewer/rag-accuracy-ragas
