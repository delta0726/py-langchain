"""
Title   : LangChainとLangGraphによるRAG・AIエージェント実践入門
Chapter : 4 LangChainの基礎
Section : 6 LangChainのRAGに関するコンポーネント
Theme   : RAGの役割と限界
Date    : 2025/07/06
Page    : P90-92
"""

# ＜RAGの概要＞
# - RAGはLLMがベクターDBを検索することで回答するための仕組みの総称
# - プロンプトのcontextに背景知識をインプットするのはトークン/精度の両面で限界がある
# - ベクターDBはテキストを数値配列に変換しているので人間には判読不能


# ＜RAGの限界＞
# - 質問に対するすべての知識をRAGでインプットするのは非現実的
# - エージェントと統合してWEB検索の外部ツールで知識を補強するのも一案
