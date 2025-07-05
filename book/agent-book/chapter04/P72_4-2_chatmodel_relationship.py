"""
Title   : LangChainとLangGraphによるRAG・AIエージェント実践入門
Chapter : 4 LangChainの基礎
Section : 2 LLM/Chat Model
Theme   : チャットモデルの継承関係
Date    : 2025/05/25
Page    : P71-72
"""

# ＜概要＞
# - LangChainの継承関係を理解しておくと使いこなしの上で役に立つ


# ＜ポイント＞
# - Runuableを継承したBaseLanguageModelがLangChainにおける一番親クラスになる
# - BaseLanguageModelは｢BaseLLM｣と｢BaseChatModel｣によって継承されている
# - 言語モデルごとにBaseLLMを継承したライブラリが作成されている