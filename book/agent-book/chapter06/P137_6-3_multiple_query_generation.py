"""
Title   : LangChainとLangGraphによるRAG・AIエージェント実践入門
Chapter : 6 Advanced RAG
Section : 3 複数の検索クエリの生成
Theme   : 複数の仮回答に基づいてHyDEを行う
Date    : 2025/06/09
Page    : P134-138
"""

# ＜概要＞
# - 仮説的な回答を複数作成して適切なドキュメントが含まれやすくする方法もある
# - ユーザーの質問に対して、複数の視点から検索クエリを生成ことで安定性が期待できる

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from pydantic import BaseModel, Field


# RAGパーツの準備 ----------------------------------------

# モデル定義
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

# DB構築
persist_directory = "./chroma_langchain"
db = Chroma(persist_directory=persist_directory, embedding_function=embeddings)

# リトリーバー定義
retriever = db.as_retriever()


# 出力パーサーの準備
# --- 仮説的な回答を格納
class QueryGenerationOutput(BaseModel):
    queries: list[str] = Field(..., description="検索クエリのリスト")


# LLMパーツの定義 ----------------------------------------

# プロンプト
prompt = ChatPromptTemplate.from_template('''\
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


# 関数定義：ログ確認 --------------------------------------


def log_queries(queries):
    print("生成された検索クエリ（multi-query）:")
    for i, q in enumerate(queries):
        print(f"  [{i + 1}] {q}")
    return queries


def log_docs(nested_docs):
    print("🔍 検索されたドキュメント一覧（クエリごと）:")
    for query_idx, docs in enumerate(nested_docs):
        print(f"クエリ {query_idx + 1} に対する検索結果:")
        for doc_idx, doc in enumerate(docs):
            content = getattr(doc, "page_content", str(doc))  # 安全にアクセス
            print(f"  --- Doc {doc_idx + 1} ---\n{content[:200]}...\n")
    return nested_docs


# クエリ生成のプロンプト構築 ----------------------------

# ＜ポイント＞
# - ユーザーの質問に対して、複数の視点から検索クエリを生成する
# - 使用意図を伝えることで適切な回答を得やすくする

# プロンプト
query_generation_prompt = ChatPromptTemplate.from_template(
    template="""\
    質問に対してベクターデータベースから関連文書を検索するために、
    3つの異なる検索クエリを生成してください。
    距離ベースの類似性検索の限界を克服するために、
    ユーザーの質問に対して複数の視点を提供することが目標です。

    質問: {question}
"""
)

# チェーン構築
query_generation_chain = (
    query_generation_prompt
    | model.with_structured_output(schema=QueryGenerationOutput)
    | (lambda x: x.queries)
    | RunnableLambda(log_queries)
)

# 仮説的な回答をラップしたChainを定義 ----------------------

multi_query_rag_chain = (
    {
        "question": RunnablePassthrough(),
        "context": query_generation_chain | retriever.map() | RunnableLambda(log_docs),
    }
    | prompt
    | model
    | output_parser
)


# 問い合わせ
multi_query_rag_chain.invoke(input="LangChainの概要を教えて")
