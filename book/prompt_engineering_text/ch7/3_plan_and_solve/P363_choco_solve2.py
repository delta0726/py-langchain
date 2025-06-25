import json
import time

from pathlib import Path
from func.plan_and_solve import plan_and_solve

BASE_DIR = Path(__file__).resolve().parent


# 関数定義
def load_text(name):
    return Path(f"{BASE_DIR}/prompts/{name}").read_text(encoding="utf-8").strip()


# プロンプト
question = load_text("question2.txt")
q = question

# 最大回数を指定して答えを得る --- (*2)
success = False
for i in range(5):
    result, response = plan_and_solve.plan_and_solve(q)
    try:
        # 結果を検算する --- (*3)
        result = result.replace("'", '"')  # 文字列のクォートを調整
        o = json.loads(result)
        print("結果:", o)
        total = o["プリン"] * 320 + o["チョコ"] * 210
        if total == (10000 - 450):
            print("=== 正解 ===")
            success = True
            break
        else:
            # 間違っていた場合に失敗例をプロンプトに埋め込む --- (*4)
            print("残念、失敗しました。")
            q = (
                f"{question}\n### 失敗例:\n"
                + "以下の応答は不正解でした。"
                + f"間違いから学んで正しいプログラムを作成してください。\n{response}"
            )
    except Exception as e:
        print("[ERROR] JSON形式のデータが出力されませんでした。\n", e)
    time.sleep(5)
    print(f"=== 再試行: {i + 2}回目 ===")
if not success:
    print("試行回数が制限回数を超えました。")
