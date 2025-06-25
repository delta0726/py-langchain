"""
Title   : LangChainとLangGraphによるRAG・AIエージェント実践入門
Chapter : 4 LangChainの基礎
Section : 6 LangChainのRAGに関するコンポーネント
Theme   : LangChainのRAG関連のパーツ紹介
Date    : 2025/05/16
Page    : P93
"""

# ＜概要＞
# - 本例はLangChainが提供するRAGの一連のワークフローをチュートリアルしている
# - 実際は｢ベクターDBの構築｣と｢問い合わせ｣は分割されるのが一般的

# ＜RAGの使いどころ＞
# - LLMが過去に基づくため最新の情報を知らない
# - 本来はLLMが知らないことでもベクターDB内の文章を検索させることで回答が可能となる
# - LLMにはトークン数に制限があるため質問文章を大きくできないことのソリューションとなる
# - RAGはベクターDBの構築から検索までの一連のワークフローを指す

# ＜LangChainのRAGに関するコンポーネント＞
# - 1.Document loader      : データソースからドキュメントを読み込む
# - 2.Document transformer : ドキュメントに何らかの変換をかける
# - 3.Embedding model      : ドキュメントをベクトル化する
# - 4.Vector store         : ベクトル化したドキュメントの保存先
# - 5.Retriever            : 問い合わせたテキストと関連するドキュメントを検索する

from langchain_community.document_loaders import GitLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma


# 1.Document loader ---------------------------------

# ＜ポイント＞
# - LangChainが提供するローダーを使ってドキュメントを読み込む
# - PDFやHTMLからドキュメントを読み込むこともある（こちらの方が直感的）


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

# ドキュメントの読み込み
raw_docs = loader.load()
print(len(raw_docs))


# 2.Document transformer ----------------------------

# ＜ポイント＞
# - 読み込んだドキュメントは様々な前処理をするのが一般的（チャンキングなど）
# - LLMに入力するトークン数を削減したり、LLMが正確な回答を導きやすくするための工夫を施す
# - 基本的に文章を分割するためチャンク数は増える

# テキスト分割
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
docs = text_splitter.split_documents(raw_docs)
print(len(docs))


# 3.Embedding model ---------------------------------

# ＜ポイント＞
# - エンベディングとは自然言語の文字をベクトル情報に変換する処理のことを指す
# - この変換処理には埋め込みモデル専用のLLMを使用する
# - この時点で人間は理解不能な情報となる
# - 高次元のベクトルのためコサイン類似度などの空間距離をもって類似性を測定する

# 埋め込みモデルの定義
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

# 動作確認
# --- 短い文章を埋め込みモデルでベクトルに変換
query = "AWSのS3からデータを読み込むためのDocument loaderはありますか？"
vector = embeddings.embed_query(query)

# 結果確認
# --- 1536次元のベクトル情報に変換された
print(len(vector))
print(vector)


# 4.Vector store -----------------------------------

# ＜ポイント＞
# - 指定したドキュメントを埋め込みモデルでベクターDBに変換する
# - 今回はChromaDBに変換したが他にも多くのDB形式が存在する

# ベクターDBに変換
db = Chroma.from_documents(documents=docs, embedding=embeddings)


# 5.Retriever ---------------------------------------

# ＜ポイント＞
# - リトリーバを使ってベクターDBに問い合わせを行う

# リトリーバの定義
retriever = db.as_retriever()

# 問い合わせ
query = "AWSのS3からデータを読み込むためのDocument loaderはありますか？"
context_docs = retriever.invoke(input=query)

# 結果確認
print(f"len = {len(context_docs)}")

# ドキュメント確認
first_doc = context_docs[0]
print(f"metadata = {first_doc.metadata}")
print(first_doc.page_content)
