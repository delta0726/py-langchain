"""
Title   : LangChainとLangGraphによるRAG・AIエージェント実践入門
Chapter : 4 LangChainの基礎
Section : 1 LangChainの概要
Theme   : メッセージ・プレースホルダー
Date    : 2025/05/14
Page    : P74
"""

import os

os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_PROJECT"] = "agent-book"
