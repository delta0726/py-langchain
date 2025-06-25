from pathlib import Path
from func.magi_tot import magi_tot

BASE_DIR = Path(__file__).resolve().parent


# 関数定義
def load_text(name):
    return (
        Path(f'{BASE_DIR}/prompts/{name}').read_text(encoding='utf-8').strip()
    )


# プロンプト
question = load_text(name='question.txt')

# 専門家を指定
roles = ['不動産の専門家', '経営コンサルタント', '賢い母親']

# 議論開始
magi_tot.max_tokens = 350
magi_tot(roles, question)
