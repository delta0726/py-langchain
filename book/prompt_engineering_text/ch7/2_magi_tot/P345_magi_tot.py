# MAGI ToTを用いて質問に答えるプログラム
import openai
import time
from dotenv import load_dotenv, find_dotenv
import os

# 環境設定
load_dotenv(find_dotenv())
api_key = os.getenv('OPENAI_API_KEY')

# OpenAIのクライアントを作成
# --- APIをたくさん呼び出すので短めに設定
client = openai.OpenAI(api_key=api_key)
max_tokens = 250


# 役割を指定してChatGPTを呼び出す関数 --- (*1)
def gen_text(role, prompt, model='gpt-4.1-nano'):
    system_msg = {'role': 'system', 'content': role}
    user_msg = {'role': 'user', 'content': prompt}
    response = client.chat.completions.create(
        model=model,
        max_tokens=max_tokens,
        temperature=0.7,
        messages=[system_msg, user_msg],
    )
    time.sleep(0.5)
    return response.choices[0].message.content.strip()


# 専門家の意見をまとめる関数 --- (*3)
def magi_summarize(question, answers):
    answer_prompt = '\n'.join(
        [f'\n### 専門家({role})の意見:\n{a}' for role, a in answers]
    )
    summary_prompt = (
        '\n### 指示:以下の質問に答えてください。\n'
        + 'ただし以下の専門家たちの意見を要約して簡潔な結論と理由を提出してください。\n'
        + f'\n### 質問:\n{question}\n'
        + answer_prompt
    )
    print('\n=== まとめ用プロンプト ===\n' + summary_prompt)
    summary = gen_text(
        'あなたは善良で公平な裁判官です。専門家の意見を元に結論を出します。',
        summary_prompt,
    )
    print('\n=== 上記をまとめたもの ===\n' + summary)
    return summary


# APIを使ってMAGI ToTを実践する関数 --- (*2)
def magi_tot(roles, question):
    print(f'\n=== 以下の質問に答えます ===\n{question}')
    # 専門家一人ずつに質問する --- (*2a)
    answers = []
    for role in roles:
        role_p = (
            f'あなたは{role}の代表です。'
            + f'質問に真摯に向き合い、{role}らしい意見を述べます。'
        )
        answer = gen_text(role=role_p, prompt=question)
        print(f'\n=== 役割: {role} ===\n{answer}')
        answers.append([role, answer])
    # 専門家の答えをまとめた答えを出力する --- (*2b)
    summary = magi_summarize(question, answers)
    # (*2a)と(*2b)を元に専門家のコメントを求める --- (*2c)
    prompt2 = (
        '### 指示:\nまず以下の質問に対する答えについて、賛否と意見を述べてください。\n'
        + f'### 質問:\n{question}\n'
        + f'### 答え:\n{summary}\n'
        + '### 出力例:\n- 賛成 or 反対: ここに理由\n'
    )
    print(f'\n=== 専門家にさらに質問します ===\n{prompt2}')
    answers = []
    for role in roles:
        role_p = f'あなたは{role}の代表です。建設的で率直な意見を述べます。'
        answer = gen_text(role_p, prompt2)
        print(f'\n=== 役割: {role} ===\n{answer}')
        answers.append([role, answer])
    # 改めて専門家の意見をまとめる --- (*2d)
    summary = magi_summarize(question, answers)
    return summary


if __name__ == '__main__':  # メイン処理 --- (*4)
    question = (
        '事務職30代男性がメニューの豊富なファミレスでランチをします。'
        + '今日頼むべきメニュー(日替わり/カレー/ハンバーグ/ラーメンなど)を提案してください。'
        + '簡潔にメニューとその理由を一言で答えてください。'
    )
    roles = ['栄養士', '愛情溢れる母親', '若い女性']
    magi_tot(roles=roles, question=question)
