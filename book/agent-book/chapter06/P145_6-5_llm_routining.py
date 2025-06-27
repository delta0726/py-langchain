"""
Title   : LangChainとLangGraphによるRAG・AIエージェント実践入門
Chapter : 6 Advanced RAG
Section : 5 複数のRetrieverを使う方法
Theme   : LLMによるルーティーング
Date    : 2025/06/09
Page    : P145
"""

# ＜ポイント＞
# - 複数のRetrieverを使用する場合、LLMによるルーティングが有効
# - ルーティーングは、ユーザーの質問に基づいて適切なRetrieverを選択するプロセス


from typing import Any
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from pydantic import BaseModel, Field
from langchain_core.documents import Document
from langchain_community.retrievers import TavilySearchAPIRetriever
from enum import Enum


# 準備 ----------------------------------------------

# 埋め込みモデルの定義
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

# DB構築
persist_directory = "./chroma_langchain"
db = Chroma(persist_directory=persist_directory, embedding_function=embeddings)

# リトリーバー定義
retriever = db.as_retriever()


# 関数定義 -----------------------------------------


# ルーティングされたリトリーバーの定義
def routed_retriever(inp: dict[str, Any]) -> list[Document]:
    question = inp["question"]
    route = inp["route"]

    if route == Route.langchain_document:
        return langchain_document_retriever.invoke(question)
    elif route == Route.web:
        return web_retriever.invoke(question)

    raise ValueError(f"Unknown route: {route}")


# 基本パーツの定義 ----------------------------------------

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
model = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# 出力パーサー
output_parser = StrOutputParser()


# リトリーバーの設定 ----------------------------------------

langchain_document_retriever = retriever.with_config(
    config={"run_name": "langchain_document_retriever"}
)

web_retriever = TavilySearchAPIRetriever(k=3).with_config(
    config={"run_name": "web_retriever"}
    )


# ルーティン処理 ----------------------------------------


class Route(str, Enum):
    langchain_document = "langchain_document"
    web = "web"


class RouteOutput(BaseModel):
    route: Route


route_prompt = ChatPromptTemplate.from_template(template="""\
質問に回答するために適切なRetrieverを選択してください。

質問: {question}
""")

route_chain = (
    route_prompt | model.with_structured_output(schema=RouteOutput) | (lambda x: x.route)
)


# クエリ生成のプロンプト構築 ----------------------------

# プロンプト
query_generation_prompt = ChatPromptTemplate.from_template(template="""\
質問に対してベクターデータベースから関連文書を検索するために、
3つの異なる検索クエリを生成してください。
距離ベースの類似性検索の限界を克服するために、
ユーザーの質問に対して複数の視点を提供することが目標です。

質問: {question}
""")


# クエリ生成の出力形式定義
class QueryGenerationOutput(BaseModel):
    queries: list[str] = Field(..., description="検索クエリのリスト")


# チェーン構築
query_generation_chain = (
    query_generation_prompt
    | model.with_structured_output(schema=QueryGenerationOutput)
    | (lambda x: x.queries)
)


# RRFによる問い合わせ ----------------------------------------

# RRFのChain構築
route_rag_chain = (
    {
        "question": RunnablePassthrough(),
        "route": route_chain,
    }
    | RunnablePassthrough.assign(context=routed_retriever)
    | prompt
    | model
    | output_parser
)


# 問い合わせ
route_rag_chain.invoke(input="LangChainの概要を教えて")
route_rag_chain.invoke(input="東京の今日の天気は？")
