"""
Title   : LangChainとLangGraphによるRAG・AIエージェント実践入門
Chapter : 3 プロンプトエンジニアリング
Section : 
Theme   : プロンプトエンジニアリングの手法（Few-Shotプロンプティング）
Date    : 2025/05/11
Page    : P55-57
"""

# ＜ポイント＞
# - 質問＆回答例を複数与えることで意図した回答を得やすくする手法
# - 実装においてもプログラムの意図がわかりやすく推奨される
# - 本例のようにロールを明確にしながら例を与えることが推奨される（P56）

from openai import OpenAI

# LLMの定義
client = OpenAI()


# Zero-Shotプロンプティング --------------------------------------------

# 問い合わせ
# --- 例示なしにダイレクトに質問する
# --- True/Falseで回答を得たいが、それを明示せずに問い合わせている
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "入力がAIに関係するか回答してください。"},
        {"role": "user", "content": "ChatGPTはとても便利だ"},
    ],
)

# 結果確認
# --- 一般的な文章が出力された（意図した回答でない）
print(response.choices[0].message.content)


# Few-Shotプロンプティング -----------------------------------------------

# 問い合わせ
# --- 回答してほしいテキストの前にデモンストレーションをする
# --- assistantで回答をTrue/Falseで行うことを明示している
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "入力がAIに関係するか回答してください。"},
        {"role": "user", "content": "AIの進化はすごい"},
        {"role": "assistant", "content": "true"},
        {"role": "user", "content": "今日は良い天気だ"},
        {"role": "assistant", "content": "false"},
        {"role": "user", "content": "ChatGPTはとても便利だ"},
    ],
)

# 結果確認
print(response.choices[0].message.content)
