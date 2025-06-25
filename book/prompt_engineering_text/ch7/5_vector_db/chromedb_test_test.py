import chromadb
from chromadb.utils import embedding_functions

# Embeddingのために利用するモデル --- (*1)
embedding_model_name = 'stsb-xlm-r-multilingual'
# Embeddingを計算する関数を生成 --- (*2)
embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name=embedding_model_name)
# ChromaDBのクライアントを生成 --- (*3)
chroma_client = chromadb.EphemeralClient() # メモリ内に保存する場合
# コレクションを作成 --- (*4)
collection = chroma_client.get_or_create_collection(
    name='test',
    embedding_function=embedding_fn)
# サンプルの文章 --- (*5)
sentences = [
    '今日の天気予報によると雨が振ります。',
    'この会社はサバ缶を海外に輸出しています。',
    'Pythonを使ってEmbeddingを計算しています。',
    '空を見上げると雲が多いので傘を持っていこう。']
# 文章をコレクションに追加 --- (*6)
collection.add(
    ids=[str(i) for i in range(len(sentences))], # 適当にIDを付与
    documents=sentences)
# 類似する文章を検索 --- (*7)
query = '雨だ。どうしよう、傘がないよ'
docs = collection.query(
    query_texts=[query],
    n_results=3,
    include=['documents', 'distances', 'embedding'])
# 結果を表示 --- (*8)
docs0 = zip(
    docs['documents'][0], 
    docs['distances'][0], 
    docs['embedding'][0])
for doc, dist, emb in docs0:
    print(f'(距離:{dist:.1f}) {doc}')
