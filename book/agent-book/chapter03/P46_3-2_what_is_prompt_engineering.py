"""
Title   : LangChainとLangGraphによるRAG・AIエージェント実践入門
Chapter : 3 プロンプトエンジニアリング
Section : 
Theme   : プロンプトエンジニアリングとは
Date    : 2025/05/07
Page    : P46-47
"""

# ＜ポイント＞
# - プロンプトエンジニアリングとは、LLMから意図した回答を引き出すためのテクニックやノウハウの集積である
# - 階層的な問い合わせ、議論を収斂させる問い合わせ、出力形式の明示、などで実現する
# - プログラムの仕組みで対応するため、LCELやデザインパターンとセットで考える

from openai import OpenAI

# LLMの定義
client = OpenAI()

# 問い合わせ
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "user", "content": "プロンプトエンジニアリングとは"},
    ],
)

# 結果表示
print(response.choices[0].message.content)


# 問い合わせ（要約版）
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "質問に100文字程度で答えてください。"},
        {"role": "user", "content": "プロンプトエンジニアリングとは"},
    ],
)


# 結果表示
print(response.choices[0].message.content)
