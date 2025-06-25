"""
Title   : Chatgpt API & Python
Section : 7 PDFからデータを抽出してグラフ化しよう
Theme   : 複数のPDFファイルからテキスト表データを抽出してcsvに変換する
Date    : 2025/05/04
Page    : P213
"""

import load_pdf
import csv

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


def main():
    # PDFのJSON変換
    # --- dataフォルダのPDFファイルを読み込んでJSON形式のデータに変換
    billing_data = load_pdf.load_all_pdfs("data")
    print("読み込みが完了しました")

    # json形式のデータをCSVファイルに書き込む
    write_to_csv(billing_data)
    print("CSVファイルへの書き込みが完了しました")


if __name__ == "__main__":
    main()
