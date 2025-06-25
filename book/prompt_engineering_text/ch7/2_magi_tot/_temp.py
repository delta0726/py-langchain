import json

# 初長さ
A_initial_length = 20  # cm
rate = 1.25  # cm per minute

# Aが燃え尽きる時間
time_A = A_initial_length / rate  # 分

# Aが燃え尽きるときの長さは0cm
A_final_length = 0

# Bの長さはAの3/2倍
B_length = (3/2) * A_initial_length  # cm

# Bの燃え尽きる時間はAの燃え尽きる時間の3/2倍
time_B = time_A * (3/2)  # 分

# 出力はJSON形式
result = {
    "Bの長さ": f"{B_length}cm",
    "Bが燃え尽きるまでの時間": f"{time_B}分"
}

print(json.dumps(result, ensure_ascii=False))