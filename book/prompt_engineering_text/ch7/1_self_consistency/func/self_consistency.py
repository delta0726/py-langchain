# 自己整合性を用いて、正しい年齢を求めるプログラム
import time
import openai
import os
from dotenv import load_dotenv, find_dotenv

# 環境設定
load_dotenv(find_dotenv())
api_key = os.getenv("OPENAI_API_KEY")

# 今回解く問題を指定 --- (*1)
QUESTION = """
Q: 私が8歳のとき妹は私の半分の年齢でした。今、私は40歳です。私の妹は何歳ですか？
A:
"""
# 問題を解く助けとなるヒント --- (*2)
HINT = """
Q: 太郎は30個の飴玉のうち半分を妹に譲りました。母は10個の飴玉を妹に与えました。妹はいくつ飴玉を持っていますか？
A: 妹は太郎から30/2=15個の飴玉を譲られました。母からさらに10個もらったので、25個持っています。答えは25です。
Q: 太郎は30匹、次郎は25匹の鶏を飼育しています。毎年1匹ずつ増やします。太郎が40匹飼育しているなら次郎は何匹ですか？
A: 太郎と次郎の鶏の差は30-25=5匹です。太郎が40匹ならば経過年数は40-30=10年です。つまり、次郎の鶏は25+10=35匹です。答えは35です。
Q: エリは10才です。エリの父は35才です。エリが20才の時、お父さんは何歳ですか？
A: エリと父の年齢差は35-10=15才です。エリが20才ならば、15+20=35才です。答えは35です。
Q: 大富豪が30台の車を所有しています。半分を手放しましたが、さらに5台の車を購入しました。大富豪は何台の車を所有していますか？
A: 大富豪が所有していた30台のうち半分を手放したので30/2=15台になりましたが、さらに5台増えました。つまり、15+5=20台あります。回答は20です。
"""
# 答えを導くためのプロンプト --- (*3)
PROMPT_SELF_CONS = """
### [指示]:
以下の質問について、[専門家の答え]をまとめて最終的な結論と理由を提出してください。
### [質問]:
{question}
### [専門家の答え]:
{answers}
"""


# ChatGPTを呼び出す関数 --- (*4)
def gen_text(prompt):
    client = openai.OpenAI()
    completion = client.chat.completions.create(
        model="gpt-4.1-nano",
        max_tokens=250,  # 回答を短くする
        temperature=0.7,
        messages=[{"role": "user", "content": prompt}],
    )
    time.sleep(1)  # APIの連続呼び出しを防ぐために1秒待つ --- (*4a)
    return completion.choices[0].message.content


# 自己整合性を用いて答えを求める関数 --- (*5)
def self_consistency(question, hint, max_iter=3):
    # 暫定的なプロンプトを組み立てる --- (*6)
    prompt_q = (
        f"### Hint:\n{hint.strip()}\n"
        + f"### Question:\n上記のヒントを参考に考えてください。\n{question.strip()}"
    )
    print(f"=== 暫定プロンプト ===\n{prompt_q}")
    # 質問を複数回実行する --- (*7)
    answers = []
    for i in range(max_iter):
        answer = gen_text(prompt_q).replace("\n", "").strip()
        answers.append(answer)
        print(f"=== {i + 1}回目の回答 ===\n{answer}")
    # 最終的な答えを求めるプロンプトを組み立てる --- (*8)
    prompt_summary = PROMPT_SELF_CONS.format(
        question=question.strip(),
        answers="\n".join([f"- (選択肢{i + 1}) {a}" for i, a in enumerate(answers)]),
    )
    # プロンプトを実行して最終的な答えを得る --- (*9)
    print(f"=== 最終的な答えを得るプロンプト ===\n{prompt_summary.strip()}")
    answer = gen_text(prompt_summary)
    return answer


if __name__ == "__main__":  # メイン処理 --- (*10)
    answer = self_consistency(QUESTION, HINT)
    print("=== 最終的な答え ===\n", answer)
