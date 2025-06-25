"""
Title   : LangChainとLangGraphによるRAG・AIエージェント実践入門
Chapter : 2 OpenAIのチャットAPIの基礎
Section : 
Theme   : JSON形式の出力
Date    : 2025/05/06
Page    : P31
"""

# ＜ポイント＞
# - 画像のURLかBase64でエンコードされたデータをLLMに与えることができる
# - 画像の内容を問いかけて応答を得ることができる

from openai import OpenAI


# LLMの定義
client = OpenAI()

# URLの指定
image_url = "https://raw.githubusercontent.com/yoshidashingo/langchain-book/main/assets/cover.jpg"

# 問い合わせ
# --- systemプロンプトにJSON形式を宣言する
# --- response_format引数を{"type": "json_object"}とする
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "画像を説明してください。"},
                {"type": "image_url", "image_url": {"url": image_url}},
            ],
        }
    ],
)

# 結果確認
print(response.choices[0].message.content)
