from pathlib import Path
from func.self_consistency import self_consistency

BASE_DIR = Path(__file__).resolve().parent


# 関数定義
def load_text(name):
    return (
        Path(f"{BASE_DIR}/prompts/self_consistency/{name}")
        .read_text(encoding="utf-8")
        .strip()
    )


# プロンプト
question = load_text(name="question.txt")
hint = load_text(name="hint.txt")

# 問い合わせ
answer = self_consistency(question, hint)
print("=== 最終的な答え ===\n" + answer)
