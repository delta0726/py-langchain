import time
import openai
import os
from dotenv import load_dotenv, find_dotenv
from pathlib import Path

# 環境設定
load_dotenv(find_dotenv())
api_key = os.getenv('OPENAI_API_KEY')


# プロンプトの取得 ----------------------------------------

# 関数定義
# --- プロンプトの読み込み
def load_text(name):
    return (
        Path(f'prompts/self_consistency/{name}')
        .read_text(encoding='utf-8')
        .strip()
    )


# プロンプト取得
# --- 今回解く問題を指定
# --- 問題を解く助けとなるヒント
# --- 答えを導くためのプロンプト
QUESTION = load_text(name='question.txt')
HINT = load_text(name='hint.txt')
PROMPT_SELF_CONS = load_text(name='prompt_self_cons.txt')


# メイン処理の関数群 ---------------------------------------------


# ChatGPTを呼び出す関数
# --- トークン数を指定して回答を短くする
# --- APIの連続呼び出しを防ぐために1秒待つ
def gen_text(prompt):
    client = openai.OpenAI(api_key=api_key)
    completion = client.chat.completions.create(
        model='gpt-4.1-nano',
        max_tokens=250,
        temperature=0.7,
        messages=[{'role': 'user', 'content': prompt}],
    )
    time.sleep(1)
    return completion.choices[0].message.content


# 自己整合性を用いて答えを求める関数
# --- 暫定的なプロンプトを組み立てる
def self_consistency(question, hint, max_iter=3):
    prompt_q = (
        f'### Hint:\n{hint.strip()}\n'
        + f'### Question:\n上記のヒントを参考に考えてください。\n{question.strip()}\n'
    )
    print(f'=== 暫定プロンプト ===\n{prompt_q}')
    # 質問を複数回実行する --- (*7)
    answers = []
    for i in range(max_iter):
        answer = gen_text(prompt_q).replace('\n', '').strip()
        answers.append(answer)
        print(f'=== {i + 1}回目の回答 ===\n{answer}\n')
    # 最終的な答えを求めるプロンプトを組み立てる --- (*8)
    prompt_summary = PROMPT_SELF_CONS.format(
        question=question.strip(),
        answers='\n'.join(
            [f'- (選択肢{i + 1}) {a}' for i, a in enumerate(answers)]
        ),
    )
    # プロンプトを実行して最終的な答えを得る --- (*9)
    print(f'=== 最終的な答えを得るプロンプト ===\n{prompt_summary.strip()}\n')
    answer = gen_text(prompt_summary)
    return answer


if __name__ == '__main__':
    answer = self_consistency(question=QUESTION, hint=HINT)
    print('=== 最終的な答え ===\n', answer)
