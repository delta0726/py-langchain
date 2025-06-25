"""
Title   : LangChainとLangGraphによるRAG・AIエージェント実践入門
Chapter : 2 OpenAIのチャットAPIの基礎
Section : 
Theme   : JSON形式の出力
Date    : 2025/05/06
Page    : P30
"""

# ＜ポイント＞
# - response_format引数でjson_objectを指定することでJSON出力させることができる
# - 問い合わせの中で何をJSON出力させるかを定義することが前提となる

from openai import OpenAI


# LLMの定義
client = OpenAI()

# 問い合わせ
# --- systemプロンプトにJSON形式を宣言する
# --- response_format引数を{"type": "json_object"}とする
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {
            "role": "system",
            "content": '人物一覧を次のJSON形式で出力してください。\n{"people": ["aaa", "bbb"]}',
        },
        {
            "role": "user",
            "content": "昔々あるところにおじいさんとおばあさんがいました",
        },
    ],
    response_format={"type": "json_object"},
)

# 確認
print(response.choices[0].message.content)
