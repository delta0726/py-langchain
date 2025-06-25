"""
Title   : Langchain完全入門
Section : 3 Retrieval
Theme   : コサイン類似度による文章の類似性の確認
Date    : 2025/04/26
Page    : P94
"""

from langchain.embeddings import OpenAIEmbeddings
from numpy import dot
from numpy.linalg import norm


# インスタンス構築
embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")


# 文字列のベクトル化 ---------------------------------------

# 質問をベクトル化
text = "飛行車の最高速度は？"
query_vector = embeddings.embed_query(text=text)

# 確認
print(f"ベクトル化された質問: {query_vector[:5]}")
print(f"ベクトルの長さ: {len(query_vector)}")


# 文字列の類似度の比較 -------------------------------------

# 質問のベクトル化
text_1 = "飛行車の最高速度は時速150キロメートルです。"
text_2 = "鶏肉を焼くときは、皮目から焼くとパリッと仕上がります。"
document_1_vector = embeddings.embed_query(text=text_1)
document_2_vector = embeddings.embed_query(text=text_2)

# ベクトルの類似度を計算
# --- ベクトルの内積
# --- 各ベクトルのノルム（長さ）
# --- コサイン類似度
numerator_1 = dot(query_vector, document_1_vector)
denominator_1 = norm(query_vector) * norm(document_1_vector)
cos_sim_1 = numerator_1 / denominator_1

numerator_2 = dot(query_vector, document_2_vector)
denominator_2 = norm(query_vector) * norm(document_2_vector)
cos_sim_2 = numerator_2 / denominator_2

# 確認
print(f"ドキュメント1と質問の類似度: {cos_sim_1}")
print(f"ドキュメント2と質問の類似度: {cos_sim_2}")
