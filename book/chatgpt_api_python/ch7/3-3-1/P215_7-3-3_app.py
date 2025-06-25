"""
Title   : Chatgpt API & Python
Section : 7 PDFからデータを抽出してグラフ化しよう
Theme   : 複数のPDFファイルからテキスト表データを抽出したデータでグラフ作成
Date    : 2025/05/05
Page    : P215
"""

import load_pdf
import csv
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.ticker import FuncFormatter


def write_to_csv(billing_data):
    # CSVファイル名
    csv_file = "output/invoices.csv"

    # ヘッダーを決定（JSONのキーから）
    header = billing_data[0].keys()

    # CSVファイルを書き込みモードで開き、データを書き込む
    with open(csv_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=header)
        writer.writeheader()
        writer.writerows(billing_data)


def draw_graph(filename):
    # invoices.csvファイルからpandasのDataFrameに読み込み（数値のカンマ区切りに対応）
    df = pd.read_csv("output/invoices.csv", thousands=",")

    # 日付のフォーマットを変換
    df["日付"] = pd.to_datetime(
        df["日付"].str.replace("年", "-").str.replace("月", "-").str.replace("日", ""),
        format="%Y-%m-%d",
    )

    # グラフを描画
    fig, ax = plt.subplots()
    ax.bar(df["日付"], df["請求金額（合計）"])
    ax.set_xlabel("date")
    ax.set_ylabel("price")
    ax.set_xticks(df["日付"])
    ax.set_xticklabels(df["日付"].dt.strftime("%Y-%m-%d"), rotation=45)

    # y軸の最小値を0に設定
    ax.set_ylim(0, max(df["請求金額（合計）"]) + 100000)

    # 縦軸のラベルを元の数字のまま表示
    ax.get_yaxis().set_major_formatter(FuncFormatter(lambda x, p: format(int(x), ",")))

    plt.tight_layout()
    plt.show()


def main():
    # データ取得
    # --- PDFからテキストデータを抽出してJSONに変換
    # --- LLMを活用して表項目を分類
    billing_data = load_pdf.load_all_pdfs("data")
    print("読み込みが完了しました")

    # データ保存
    # --- JSON形式のデータをCSVファイルに書き込む
    write_to_csv(billing_data)
    print("CSVファイルへの書き込みが完了しました")

    # グラフ作成
    # --- 必ずしもデータが扱いやすい形式でないので変換が必要
    draw_graph(filename="output/invoices.csv")


if __name__ == "__main__":
    main()
