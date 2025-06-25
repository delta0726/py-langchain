from sentence_transformers import SentenceTransformer, util

# モデルを使用してEmbedingを計算する --- (*1)
model = SentenceTransformer("stsb-xlm-r-multilingual")
# より手軽なモデルで試したい場合は下記を使用 --- (*1a)
# model = SentenceTransformer('all-MiniLM-L6-v2')

# サンプルの文章 --- (*2)
sentences = [
    "今日の天気予報によると雨が振ります。",
    "この会社はサバ缶を海外に輸出しています。",
    "Pythonを使ってEmbeddingを計算しています。",
    "空を見上げると雲が多いので傘を持っていこう。",
]

# 文章をEmbeddingに変換 --- (*3)
embeddings = model.encode(sentences)

# それぞれの類似度を計算 --- (*4)
cosine_scores = util.cos_sim(embeddings, embeddings)

# 結果を表示 --- (*4)
result = []
for i, sentence in enumerate(sentences):
    # 最初の文との類似度を取得 --- (*5)
    score = cosine_scores[0][i]
    embedding = embeddings[i]
    result.append({"score": score, "sentence": sentence})
    print("文章:", sentence)
    print("Embedding:", embedding[:5], "...")
    print("類似度:", score)
    print("---------")

# 最初の文と近い順に表示 --- (*5)
result = list(sorted(result, key=lambda x: x["score"], reverse=True))

print("=== 最初の文と近い順に表示 ===")
for e in result:
    print(f"(類似度:{e['score']:.3f}) {e['sentence']}")
