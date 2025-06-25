# 価格設定
price_pudding = 320
price_choco = 210
total_amount = 9550  # 支払額からお釣りを引いた合計金額

# 解を格納する変数
solutions = []

# 二重ループで全探索
for num_pudding in range(0, total_amount // price_pudding + 1):
    for num_choco in range(0, total_amount // price_choco + 1):
        total_price = (price_pudding * num_pudding) + (price_choco * num_choco)
        if total_price == total_amount:
            solutions.append((num_pudding, num_choco))

# 結果の出力
for pudding, choco in solutions:
    print(f"プリン {pudding}個、チョコ {choco}個")