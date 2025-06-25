from pprint import pprint
from pathlib import Path
from func.plan_and_solve import plan_and_solve


BASE_DIR = Path(__file__).resolve().parent


# 関数定義
def load_text(name):
    return Path(f"{BASE_DIR}/prompts/{name}").read_text(encoding="utf-8").strip()


# プロンプト
question = load_text("question.txt")

# 問い合わせ
ans = plan_and_solve(question)

# 確認
pprint(question)
pprint(ans)