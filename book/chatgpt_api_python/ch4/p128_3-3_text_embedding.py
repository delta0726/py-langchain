"""
Title   : Chatgpt API & Python
Section : 4 独自のデータで学んだチャットボットを作ろう
Theme   : 学習データをエンベティングする
Date    : 2025/05/02
Page    : P128
"""

import pandas as pd
import tiktoken
from get_embedding import get_embedding


# パラメータ設定
embedding_model = "text-embedding-3-small"
embedding_encoding = "cl100k_base"
max_tokens = 1500


# 前処理 -------------------------------------------------------

# データ取得
df = pd.read_csv("text/scraped.csv")

# データ加工
# --- トークン数の追加
# --- tokenizerはテキストをトークン(単語・記号などの単位)に分解するオブジェクト
df.columns = ["title", "text"]
tokenizer = tiktoken.get_encoding(encoding_name=embedding_encoding)
df["n_tokens"] = df.text.apply(lambda x: len(tokenizer.encode(x)))


# 関数定義 -----------------------------------------------------


# 文をトークン数でチャンク分割する関数
def split_into_many(text, max_tokens=500):
    sentences = text.split("。")
    n_tokens = [len(tokenizer.encode(" " + sentence)) for sentence in sentences]

    chunks, tokens_so_far, chunk = [], 0, []
    for sentence, token in zip(sentences, n_tokens):
        if token > max_tokens:
            continue
        if tokens_so_far + token > max_tokens:
            chunks.append("。".join(chunk) + "。")
            chunk, tokens_so_far = [], 0
        chunk.append(sentence)
        tokens_so_far += token + 1

    if chunk:
        chunks.append("。".join(chunk) + "。")
    return chunks


# 行ごとに分割またはそのまま保持する処理
def process_row(row):
    if pd.isnull(row["text"]):
        return []
    if row["n_tokens"] > max_tokens:
        return split_into_many(row["text"], max_tokens=max_tokens)
    return [row["text"]]


# 補助関数 ----------------------------------------------------


# トークン数の計算関数
def count_tokens(text):
    return len(tokenizer.encode(text))


# 埋め込み取得関数
def compute_embedding(text):
    return get_embedding(text, model=embedding_model)


# メイン処理 ---------------------------------------------------

# テキストをチャンクごとに展開
df_chunks = df.apply(process_row, axis=1).explode().dropna().to_frame(name="text")

# トークン数と埋め込みの追加
df_chunks["n_tokens"] = df_chunks["text"].apply(count_tokens)
df_chunks["embeddings"] = df_chunks["text"].apply(compute_embedding)


# 保存
df_chunks.to_csv("text/embeddings.csv", index=False)
