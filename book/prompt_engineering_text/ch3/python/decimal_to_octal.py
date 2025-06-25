def decimal_to_octal(n):
    # nが0以下の場合はそのまま返す
    if n <= 0:
        return '0'
    
    octal_result = ''
    
    while n > 0:
        # nを8で割った余りをmとする
        m = n % 8
        # nを8で割った商を新しいnとする
        n = n // 8
        # mを結果の先頭に追加
        octal_result = str(m) + octal_result
    
    return octal_result

# テスト
decimal_value = 42  # 10進数の値
octal_value = decimal_to_octal(decimal_value)
print(f"{decimal_value} の8進数表現は {octal_value} です。")
