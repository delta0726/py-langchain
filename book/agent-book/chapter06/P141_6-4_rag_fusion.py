"""
Title   : LangChainとLangGraphによるRAG・AIエージェント実践入門
Chapter : 6 Advanced RAG
Section : 4 検索後の工夫（RAG-Fusion）
Theme   : 検索したクエリ結果の並び替えの工夫
Date    : 2025/06/09
Page    : P141
"""

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from pydantic import BaseModel, Field
from langchain_core.documents import Document


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


# 関数定義 -----------------------------------------

# ＜ポイント＞
# - RRF(Reprocal Rank Fusion)は各検索クエリをスコアの大きさに基づいて並び替える
# - スコアは1/(順位+ｋ)で計算され、kは60などの値が使用される


# RRF処理
def reciprocal_rank_fusion(
    retriever_outputs: list[list[Document]],
    k: int = 60,
) -> list[str]:
    # 各ドキュメントのコンテンツ (文字列) とそのスコアの対応を保持する辞書を準備
    content_score_mapping = {}

    # 検索クエリごとにループ
    for docs in retriever_outputs:
        # 検索結果のドキュメントごとにループ
        for rank, doc in enumerate(docs):
            content = doc.page_content

            # 初めて登場したコンテンツの場合はスコアを0で初期化
            if content not in content_score_mapping:
                content_score_mapping[content] = 0

            # (1 / (順位 + k)) のスコアを加算
            content_score_mapping[content] += 1 / (rank + k)

    # スコアの大きい順にソート
    ranked = sorted(content_score_mapping.items(), key=lambda x: x[1], reverse=True)  # noqa
    return [content for content, _ in ranked]


# 基本パーツの定義 ----------------------------------------

# ＜ポイント＞
# - 検索したクエリ結果を集約するための仕組み


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


# クエリ生成のプロンプト構築 ----------------------------


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


# クエリ生成の出力形式定義
class QueryGenerationOutput(BaseModel):
    queries: list[str] = Field(..., description="検索クエリのリスト")


# チェーン構築
query_generation_chain = (
    query_generation_prompt
    | model.with_structured_output(QueryGenerationOutput)
    | (lambda x: x.queries)
)


# RRFによる問い合わせ ----------------------------------------


# RRFのChain構築
rag_fusion_chain = (
    {
        "question": RunnablePassthrough(),
        "context": query_generation_chain | retriever.map() | reciprocal_rank_fusion,
    }
    | prompt
    | model
    | output_parser
)


# 問い合わせ
rag_fusion_chain.invoke(input="LangChainの概要を教えて")
