"""
Title   : LangChainとLangGraphによるRAG・AIエージェント実践入門
Chapter : 5 LangeChain Expression Language(LCEL)の徹底解説
Section : 6 複数のRetrieverを使う方法
Theme   : ハイブリッド検索
Date    : 2025/06/29
Page    : P149
"""

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough, RunnableParallel
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain_core.documents import Document
from langchain_community.retrievers import BM25Retriever
from langchain_community.document_loaders import GitLoader


# 準備1 ----------------------------------------------

# ＜ポイント＞
# - RAG検索を行うためのリトリーバーを定義する


# 埋め込みモデルの定義
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

# DB構築
persist_directory = "./chroma_langchain"
db = Chroma(persist_directory=persist_directory, embedding_function=embeddings)

# リトリーバー定義
retriever = db.as_retriever()


# 準備2 ----------------------------------------------

# ローダー定義
loader = GitLoader(repo_path="./langchain", branch="master")

# ドキュメントのロード
documents = loader.load()


# 基本パーツの定義 ----------------------------------------

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


# 関数定義 ----------------------------------------


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


# リトリーバーの設定 ----------------------------------------

chroma_retriever = retriever.with_config(config={"run_name": "chroma_retriever"})

bm25_retriever = BM25Retriever.from_documents(documents=documents).with_config(
    {"run_name": "bm25_retriever"}
)

hybrid_retriever = (
    RunnableParallel(
        {
            "chroma_documents": chroma_retriever,
            "bm25_documents": bm25_retriever,
        }
    )
    | (lambda x: [x["chroma_documents"], x["bm25_documents"]])
    | reciprocal_rank_fusion
)


# ハイブリッド検索の実施 ----------------------------------------

# Chain構築
hybrid_rag_chain = (
    {
        "question": RunnablePassthrough(),
        "context": hybrid_retriever,
    }
    | prompt
    | model
    | output_parser
)

# 問い合わせ
hybrid_rag_chain.invoke(input="LangChainの概要を教えて")
