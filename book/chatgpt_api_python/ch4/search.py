import pandas as pd
from openai import OpenAI

import numpy as np
from util import distances_from_embeddings

# LLMの定義
client = OpenAI()


def create_context(question, df, max_len=1800):
    """
    質問と学習データを比較して、コンテキストを作成する関数
    """

    # 質問をベクトル化
    q_embeddings = (
        client.embeddings.create(input=question, model="text-embedding-3-small")
        .data[0]
        .embedding
    )

    # 類似度計算
    # --- 質問と学習データのコサイン類似度を計算
    # ---「distances」という列に類似度を格納
    df["distances"] = distances_from_embeddings(
        query_embedding=q_embeddings,
        embeddings=df["embeddings"].apply(eval).apply(np.array).values,
        distance_metric="cosine",
    )

    # 変数定義
    # --- コンテキストを格納するためのリスト
    # --- コンテキストの現在の長さ
    returns = []
    cur_len = 0

    # 学習データを類似度順にソートし、トークン数の上限までコンテキストに
    # 追加する
    for _, row in df.sort_values("distances", ascending=True).iterrows():
        # テキストの長さを現在の長さに加える
        cur_len += row["n_tokens"] + 4

        # テキストが長すぎる場合はループを終了
        if cur_len > max_len:
            break

        # コンテキストのリストにテキストを追加する
        returns.append(row["text"])

    # コンテキストを結合して返す
    return "\n\n###\n\n".join(returns)


def answer_question(question, conversation_history):
    """
    コンテキストに基づいて質問に答える関数
    """

    # 学習データの読み込み
    df = pd.read_csv("text/embeddings.csv", encoding="UTF8")

    # 関係個所の取得
    # --- 類似度の近い文章を抽出
    context = create_context(question=question, df=df, max_len=200)

    # 会話準備
    # --- プロンプトを作成
    # --- 会話の履歴に追加
    prompt = f"あなたはとあるホテルのスタッフです。コンテキストに基づいて、お客様からの質問に丁寧に答えてください。コンテキストが質問に対して回答できない場合は「わかりません」と答えてください。\n\nコンテキスト: {context}\n\n---\n\n質問: {question}\n回答:"
    conversation_history.append({"role": "user", "content": prompt})

    # 問い合わせ
    try:
        # ChatGPTからの回答を生成
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=conversation_history,
            temperature=1,
        )

        # ChatGPTからの回答を返す
        return response.choices[0].message.content.strip()
    except Exception as e:
        # エラーが発生した場合は空の文字列を返す
        print(e)
        return ""
