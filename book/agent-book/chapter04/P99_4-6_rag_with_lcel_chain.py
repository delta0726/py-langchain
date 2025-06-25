"""
Title   : LangChainとLangGraphによるRAG・AIエージェント実践入門
Chapter : 4 LangChainの基礎
Section : 6 LangChainのRAGに関するコンポーネント
Theme   : LCELを使ったRAGのChainの実装
Date    : 2025/05/16
Page    : P93
"""


# ＜概要＞
# - 本例はLCELでRAGのワークフローのチュートリアルを確認する
# - RAGプロセスはP93と同じで、問い合わせ方法をLCELに変更している

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_community.document_loaders import GitLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai import ChatOpenAI, OpenAIEmbeddings


# 準備 ------------------------------------------

# プロンプト定義
prompt = ChatPromptTemplate.from_template(
    template='''\
以下の文脈だけを踏まえて質問に回答してください。

文脈: """
{context}
"""

質問: {question}
'''
)


# 抽出関数
def file_filter(file_path: str) -> bool:
    return file_path.endswith(".mdx")


# Gitローダーの定義
loader = GitLoader(
    clone_url="https://github.com/langchain-ai/langchain",
    repo_path="./langchain",
    branch="master",
    file_filter=file_filter,
)


# ベクターDBの構築 ---------------------------------

# ドキュメント読み込み
# --- 約3-4分かかる
raw_docs = loader.load()
print(f"Raw documents loaded: {len(raw_docs)}")

# テキスト変換
# --- チャンキング
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
docs = text_splitter.split_documents(documents=raw_docs)
print(f"Documents after splitting: {len(docs)}")

# 埋め込みモデルの定義
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

# ベクターDBの構築
db = Chroma.from_documents(documents=docs, embedding=embeddings)

# Retrieverの定義
retriever = db.as_retriever()


# 問い合わせ --------------------------------------

# ＜ポイント＞
# - チェインでRunnableMapの構文を使用している
# - 入力データを"context"と"question"というキーに分けて別々の処理を通す
# - これによりcontextでRetrieverを使用するように設定している

# LLMの定義
model = ChatOpenAI(model_name="gpt-4o-mini", temperature=0)

# チェイン構築
chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | model
    | StrOutputParser()
)

# 問い合わせ
query = "AWSのS3からデータを読み込むためのDocument loaderはありますか？"
output = chain.invoke(query)

# 結果確認
print("回答:", output)
