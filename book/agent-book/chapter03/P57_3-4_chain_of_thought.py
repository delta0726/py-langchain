"""
Title   : LangChainとLangGraphによるRAG・AIエージェント実践入門
Chapter : 3 プロンプトエンジニアリング
Section : 
Theme   : Few-Shotプロンプティングの方法
Date    : 2025/05/11
Page    : P57
"""

# ＜ポイント＞
# - Chain-of-Thoughtはプロセスを踏んで考えることを明示するプロンプトの書き方
# - ｢ステップ・バイ・ステップで考えてください｣と指示すればよい
# - LCELのChainやデザインパターンやワークフローでも多用される

# ＜LLMの欠点＞
# - 論理的プロセスを経ずに質問文の流れ(雰囲気)に近い回答をしてしまう
# - Chain-of-thoughtを指示することで論理的思考を行わせることができる

from openai import OpenAI

# LLMの定義
client = OpenAI()


# 方法1: 1ステップで回答 -------------------------------------------

# 問い合わせ
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "回答だけ一言で出力してください。"},
        {"role": "user", "content": "10 + 2 * 3 - 4 * 2"},
    ],
)

# 結果確認
# --- 10（不正解）
print(response.choices[0].message.content)


# 方法2: Chain-of-thoughtで回答 ----------------------------------

# 問い合わせ
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "ステップバイステップで考えてください。"},
        {"role": "user", "content": "10 + 2 * 3 - 4 * 2"},
    ],
)

# 結果確認
# --- 8と回答（正解）
print(response.choices[0].message.content)


# ＜レスポンス＞
# 計算をステップバイステップで行います。
#
# 1. **掛け算を先に計算します。**
#    - \(2 * 3 = 6\)
#    - \(4 * 2 = 8\)
#
# 2. **計算結果を式に代入します。**
#    - 元の式は \(10 + 2 * 3 - 4 * 2\) なので、代入後は \(10 + 6 - 8\) になります。
#
# 3. **足し算を計算します。**
#    - \(10 + 6 = 16\)
#
# 4. **引き算を計算します。**
#    - \(16 - 8 = 8\)
