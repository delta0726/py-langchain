"""
Title   : LangChainとLangGraphによるRAG・AIエージェント実践入門
Chapter : 5 LangeChain Expression Language(LCEL)の徹底解説
Section : RunnablePassthrough - 入力をそのまま出力する
Theme   : assignによるリトリーバーの検索結果の取得
Date    : 2025/06/08
Page    : P123
"""

# ＜概要＞
# - assignを使ってリトリーバーの検索結果を出力に含める

import os
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_community.retrievers import TavilySearchAPIRetriever
from langchain_core.runnables import RunnablePassthrough
from langchain_core.runnables import RunnableParallel


# 環境設定
load_dotenv()
api_key = os.getenv("TAVILY_API_KEY")


# コンポーネント定義 ------------------------------------------

# プロンプト
prompt = ChatPromptTemplate.from_template(
    template='''\
以下の文脈だけを踏まえて質問に回答してください。

文脈: """
{context}
"""

質問: {question}
'''
)

# LLMモデル
model = ChatOpenAI(model_name="gpt-4o-mini", temperature=0)


# 検索リトリーバー
# --- 検索結果を上位3件だけ取得
retriever = TavilySearchAPIRetriever(k=3)


# 辞書型による自動変換を活用した記法 ------------------------------

# ＜ポイント＞
# - 辞書を使うことでRunnableParallelに自動変換されている
# - 並列処理の明示性がないため初心者には何をやっているか判別しにくい
# - 記法としての柔軟性も劣る

# Chain構築
chain = {
    "question": RunnablePassthrough(),
    "context": retriever,
} | RunnablePassthrough.assign(answer=prompt | model | StrOutputParser())

# 問い合わせ
output = chain.invoke(input="東京の今日の天気は？")

# 結果確認
print(output)


# RunnableParallelを使う記法 -----------------------------------

# ＜ポイント＞
# - RunnableParallelを使って並列処理を明示的に行っている
# - assign()で新しいフィールド(answer)を既存データに追加している
# - Chainの再利用性が高い記法

# Chain構築
chain = RunnableParallel(
    steps__={"question": RunnablePassthrough(), "context": retriever}
).assign(answer=prompt | model | StrOutputParser())


# 問い合わせ
output = chain.invoke(input="東京の今日の天気は？")

# 結果確認
print(output)
