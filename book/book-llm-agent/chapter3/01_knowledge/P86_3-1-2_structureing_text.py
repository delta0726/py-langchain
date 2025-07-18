"""
Title   : やさしく学ぶLLMエージェント
Chapter : 3 エージェント
Section : 1 LLLMに知識を与える
Theme   : 文書の構造化（DB化）
Date    : 2025/07/18
Page    : P85-90
"""

# ＜概要＞
# - 背景知識をより体系的に管理してLLMに与えるためには文書のDB管理が必要となる
# - 同時に、大量の文書から必要な情報を抽出するための検索性も必要なる
# - DocumentクラスとChromaDBを使った文書のDB化を行う
# - このプロセスはRAGによる検索の橋渡しとなる

# ＜ChromaDBとは＞
# - ChromaDBはベクトル検索とセマンティック検索に特化したDB
#   --- ベクトル検索は単語類似性で検索し、セマンティック検索は意味に基づいて検索する

from langchain_core.documents import Document
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings


# Step 1: Documentの定義 ------------------------------------------

# ＜ポイント＞
# - Documentクラスはテキストデータ(page_content)とメタデータ(metadata)で構成される
# - metaデータには、ソース/ページ/著者/日付などが格納される


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


# Step 2: ChromaDBの構築 -----------------------------------------

# ＜ポイント＞
# - LLMでエンベディングして自然言語をベクトル情報に変換してDB格納
# - 今回はメモリ上に仮想DBとして作成している

# DB構築
# --- ベクトルストア型のDBを作成
vectorstore = Chroma.from_documents(documents=documents, embedding=OpenAIEmbeddings())


# Step 3: 類似検索 ------------------------------------------------

# ＜ポイント＞
# - ベクトル検索で単語類似度に基づいて文書を検索する
# - 距離スコアが小さいものが類似性が高い回答となる


# 類似文書の取得
# --- スコアなし
# --- スコア付き
results = vectorstore.similarity_search(query="熊童子")
results_with_score = vectorstore.similarity_search_with_score(query="熊童子")

# 結果表示
for i, (doc, score) in enumerate(results_with_score):
    print(f"[{i + 1}] Score: {score:.4f}\nContent: {doc.page_content}\n")
