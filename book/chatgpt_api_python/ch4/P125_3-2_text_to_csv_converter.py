"""
Title   : Chatgpt API & Python
Section : 4 独自のデータで学んだチャットボットを作ろう
Theme   : テキストデータをtxtからcsvに変換する
Date    : 2025/05/02
Page    : P125
"""

import pandas as pd
import re

"""
- 今回のような｢見出し｣と｢本文｣が存在するような構造化テキストデータの場合はCSV形式が扱いやすい
"""

def remove_newlines(text):
    """
    文字列内の改行と連続する空白を削除する関数
    """
    text = re.sub(pattern=r"\n", repl=" ", string=text)
    text = re.sub(pattern=r" +", repl=" ", string=text)
    return text


def text_to_df(data_file):
    """
    #テキストファイルを処理してDataFrameを返す関数
    """
    # テキストを格納するための空のリストを作成
    texts = []

    # 指定されたファイル（data_file）を読み込み、変数「file」に格納
    with open(data_file, "r", encoding="utf-8") as file:
        # ファイルの内容を文字列として読み込む
        text = file.read()
        # 改行2つで文字列を分割
        sections = text.split("\n\n")

        # 各セクションに対して処理を行う
        for section in sections:
            # セクションを改行で分割する
            lines = section.split("\n")
            # 「lines」リストの最初の要素を取得
            fname = lines[0]
            # 「lines」リストの2番目以降の要素を取得
            content = " ".join(lines[1:])
            # 「fname」と「content」をリストに追加
            texts.append([fname, content])

    # リストからDataFrameを作成
    df = pd.DataFrame(texts, columns=["fname", "text"])
    # 「text」列内の改行を削除
    df["text"] = df["text"].apply(remove_newlines)

    return df


if __name__ == "__main__":

    # テキストをCSV形式に変換
    df = text_to_df(data_file="text/data.txt")
    df.to_csv("text/scraped.csv", index=False, encoding="utf-8")
