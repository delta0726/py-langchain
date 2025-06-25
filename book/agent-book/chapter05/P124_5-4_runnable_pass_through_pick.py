"""
Title   : LangChainとLangGraphによるRAG・AIエージェント実践入門
Chapter : 5 LangeChain Expression Language(LCEL)の徹底解説
Section : RunnablePassthrough - 入力をそのまま出力する
Theme   : pickによるリトリーバーの検索結果の一部の取得
Date    : 2025/05/25
Page    : P122
"""

# ＜概要＞
# - pickを使ってリトリーバーの検索結果の一部を出力に含める

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
prompt = ChatPromptTemplate.from_template('''\
以下の文脈だけを踏まえて質問に回答してください。

文脈: """
{context}
"""

質問: {question}
''')

# LLMモデル
model = ChatOpenAI(model_name="gpt-4o-mini", temperature=0)

# 検索リトリーバー
retriever = TavilySearchAPIRetriever(k=3)


# RunnableParallelを使う記法 -----------------------------------

# Chain構築
chain = (
    RunnableParallel(
        steps__={
            "question": RunnablePassthrough(),
            "context": retriever,
        }
    )
    .assign(answer=prompt | model | StrOutputParser())
    .pick(keys=["context", "answer"])
)

# 問い合わせ
output = chain.invoke("東京の今日の天気は？")

# 結果確認
print(output)