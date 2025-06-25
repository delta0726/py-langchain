"""
Title   : LangChainとLangGraphによるRAG・AIエージェント実践入門
Chapter : 5 LangeChain Expression Language(LCEL)の徹底解説
Section : RunnablePassthrough - 入力をそのまま出力する
Theme   : Tavilyを使ったWeb検索のRAG
Date    : 2025/05/25
Page    : P121
"""

# ＜概要＞
# - 本章で使用するTavilyを使ったWeb検索のチュートリアル

import os
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_community.retrievers import TavilySearchAPIRetriever
from langchain_core.runnables import RunnablePassthrough


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
retriever = TavilySearchAPIRetriever(k=3)


# Web検索によるRAG --------------------------------------------

# ＜ポイント＞
# -「LangChainにおける明示的なデータルーティングのために必要」というのが本質

# ＜注意点＞
# - 以下の例は｢今日｣を明示的に定義していない
# - 学習時には実際の日付と、検索結果から得た問い合わせ結果の日付が異なっていた

# Chain構築
# --- contextはリトリーバーに検索させ、questionはそのまま渡す
chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | model
    | StrOutputParser()
)

# 問い合わせ
output = chain.invoke("東京の今日の天気は？")

# 結果確認
print(output)
