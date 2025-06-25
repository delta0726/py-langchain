"""
Title   : LangChainとLangGraphによるRAG・AIエージェント実践入門
Chapter : 3 プロンプトエンジニアリング
Section : 
Theme   : プロンプトエンジニアリングの手法（Zero-Shotプロンプティング）
Date    : 2025/05/11
Page    : P54
"""

# ＜ポイント＞
# - 質問＆回答例を全く与えずにタスク指示だけでLLMに問い合わせる手法
# - 軽量かつ何度も試すことができ直感的でもある
# - 回答の安定性に揺らぎが出やすいためシステム実装には不向き

from openai import OpenAI

# LLMの定義
client = OpenAI()

# 問い合わせ
# --- 例示なしにダイレクトに質問する（Zero-Shotプロンプティング）
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {
            "role": "system",
            "content": "入力をポジティブ・ネガティブ・中立のどれかに分類してください。",
        },
        {
            "role": "user",
            "content": "ChatGPTはとても便利だ",
        },
    ],
)

# 結果確認
print(response.choices[0].message.content)
