"""
Title   : LangChainとLangGraphによるRAG・AIエージェント実践入門
Chapter : 6 Advanced RAG
Section : 3 検索クエリの工夫
Theme   : 単一の仮回答に基づいてHyDEを行う
Date    : 2025/05/25
Page    : P134-136
"""

# ＜ポイント＞
# - RAGはユーザーの質問に対して埋め込みベルトるの類似度が高いドキュメントを検索
# - しかし、実際に検索したいのは回答に類似するドキュメント
# - そこで、HyDEは仮説的な回答を生成し、その回答に基づいて検索クエリを生成する

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.runnables import RunnableLambda
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma


# RAGパーツの準備 ----------------------------------------

# ＜ポイント＞
# - ChromaDBを指定してRAGをリトリーバーを設定する
# - LLMモデルは埋め込みモデルを使用する

# モデルの定義
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

# DB定義
persist_directory = "./chroma_langchain"
db = Chroma(persist_directory=persist_directory, embedding_function=embeddings)

# リトリーバー定義
retriever = db.as_retriever()


# LLMパーツの定義 ----------------------------------------

# ＜ポイント＞
# - メインの質問を受けてLLMモデルに回答を問う


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


# チェイン構築：仮説的な回答 --------------------------------

# ＜ポイント＞
# - HyDEはLLMが一般知識の中で正解を導き出せる際に効果を発揮する

# プロンプト
hypothetical_prompt = ChatPromptTemplate.from_template(
    template="""\
次の質問に回答する一文を書いてください。

質問: {question}
"""
)

# チェーン定義
hypothetical_chain = hypothetical_prompt | model | output_parser


# チェイン構築：HyDEによる検索 ------------------------------

# ＜ポイント＞
# - 仮説的な回答をもとにRAGで検索することでDBの内容に準じた回答が得られる
# - HyDEを行うための仮説的な質問の回答をモニタリングする
# - 今回は、仮説に近い文章がDBから引用されていることが確認できる


# ログ関数
def log_context(x):
    print("context に投げ込まれた仮想質問:", x)
    return x


# HyDEチェーンの構築
hyde_rag_chain = (
    {
        "question": RunnablePassthrough(),
        "context": hypothetical_chain | RunnableLambda(func=log_context) | retriever,
    }
    | prompt
    | model
    | output_parser
)

# 問い合わせ
hyde_rag_chain.invoke(input="LangChainの概要を教えて")
