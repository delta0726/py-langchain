"""
Title   : やさしく学ぶLLMエージェント
Chapter : 3 エージェント
Section : 1 LLLMに知識を与える
Theme   : 文書検索機能を持つLLM
Date    : 2025/07/18
Page    : P91-93
"""

# ＜概要＞
# - Contextにから与える背景知識をChromaDBから取得する
# - ChromaDBの大量の文書の中から質問に近い文書を抽出してContextに与える

from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import Chroma


# Step 1: ChromaDBの作成 -----------------------------------------------------

documents = [
    Document(
        page_content=(
            "セダムはベンケイソウ科マンネングザ属で、日本にも自生しているポピュラーな多肉植物です。"
            "種類が多くて葉の大きさや形状、カラーバリエーションも豊富なので、組み合わせて寄せ植えにしたり、"
            "庭のグランドカバーにしたりして楽しむことができます。とても丈夫で育てやすく、"
            "多肉植物を初めて育てる方にもおすすめです。"
        ),
        metadata={"source": "succulent-plants-doc"},
    ),
    Document(
        page_content=(
            "熊童子はベンケイソウ科コチレドン属の多肉植物です。"
            "葉に丸みや厚みがあり、先端には爪のような突起があることから「熊の手」という愛称で人気を集めています。"
            "花はオレンジ色のベル型の花を咲かせることがあります。"
        ),
        metadata={"source": "succulent-plants-doc"},
    ),
    Document(
        page_content=(
            "エケベリアはベンケイソウ科エケベリア属の多肉植物で、メキシコなど中南米が原産です。"
            "まるで花びらのように広がる肉厚な葉が特徴で、秋には紅葉も楽しめます。"
            "品種が多く、室内でも気軽に育てられるので、人気のある多肉植物です。"
        ),
        metadata={"source": "succulent-plants-doc"},
    ),
    Document(
        page_content=(
            "ハオルチアは、春と秋に成長するロゼット形の多肉植物です。"
            "密に重なった葉が放射状に展開し、幾何学的で整った株姿になるのが魅力です。"
            "室内でも育てやすく手頃なサイズの多肉植物です。"
        ),
        metadata={"source": "succulent-plants-doc"},
    ),
]

# DB作成
vectorstore = Chroma.from_documents(documents=documents, embedding=OpenAIEmbeddings())


# Step2: RAGのためのChain構築 -----------------------------------

# ＜ポイント＞
# - ChromaDBを検索するためのRetriever(検索器)を定義する
# - プロンプトをテンプレート化しておいて、テンプレートのパラメータを事前に作成する


# プロンプト
# --- Contextのみを使って質問に答える
message_template = """
Answer this question using the provided context only.

{question}

Context:
{context}
"""

# コンポーネント定義
# --- 検索器の定義
# --- プロンプト
# --- 言語モデル
retriever = RunnableLambda(vectorstore.similarity_search).bind(k=1)
prompt = ChatPromptTemplate.from_messages(messages=[("human", message_template)])
model = ChatOpenAI(model="gpt-4o-mini")

# チェイン構築
# --- Contextはリトリーバーから取得し、Questionはオリジナルの質問を転用する
rag_chain = {"context": retriever, "question": RunnablePassthrough()} | prompt | model


# Step3: RAGによる問い合わせ -----------------------------------

# 問い合わせ
result = rag_chain.invoke("熊童子について教えてください。")

# 結果確認
print(result.content)
