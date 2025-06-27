"""
Title   : LangChainとLangGraphによるRAG・AIエージェント実践入門
Chapter : 6 Advanced RAG
Section : 4 検索後の工夫（Cohereのリランクモデルの導入）
Theme   : 
Date    : 2025/06/09
Page    : P143
"""

# ＜ポイント＞
# - 1つの検索結果の順にについてもリランクするのが有効な場合がある


from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from pydantic import BaseModel, Field
from langchain_core.documents import Document
from typing import Any
from langchain_cohere import CohereRerank
from langchain_core.documents import Document
from pydantic import BaseModel, Field


# 準備 ----------------------------------------------

# ＜ポイント＞
# - RAG検索を行うためのリトリーバーを定義する


# 埋め込みモデルの定義
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

# DB構築
persist_directory = "./chroma_langchain"
db = Chroma(persist_directory=persist_directory, embedding_function=embeddings)

# リトリーバー定義
retriever = db.as_retriever()


# 基本パーツの定義 ----------------------------------------

# ＜ポイント＞
# - 検索したクエリ結果を集約するためのパーツ


# プロンプト
prompt = ChatPromptTemplate.from_template(template='''\
以下の文脈だけを踏まえて質問に回答してください。

文脈: """
{context}
"""

質問: {question}
''')


# LLMモデル
model = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# 出力パーサー
output_parser = StrOutputParser()


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
    | model.with_structured_output(QueryGenerationOutput)
    | (lambda x: x.queries)
)


# 関数定義 -----------------------------------------

# リランクモデル
def rerank(inp: dict[str, Any], top_n: int = 3) -> list[Document]:
    question = inp["question"]
    documents = inp["documents"]

    cohere_reranker = CohereRerank(model="rerank-multilingual-v3.0", top_n=top_n)
    return cohere_reranker.compress_documents(documents=documents, query=question)


# リランクによる問い合わせ ----------------------------------------

# リランクのChain構築
rerank_rag_chain = (
    {
        "question": RunnablePassthrough(),
        "documents": retriever,
    }
    | RunnablePassthrough.assign(context=rerank)
    | prompt | model | output_parser
)


# 問い合わせ
rerank_rag_chain.invoke(input="LangChainの概要を教えて")
