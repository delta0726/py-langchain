"""
Title   : LangChainとLangGraphによるRAG・AIエージェント実践入門
Chapter : 2 OpenAIのチャットAPIの基礎
Section : 
Theme   : ストリーミング出力
Date    : 2025/05/06
Page    : P29
"""

# ＜ポイント＞
# - stream引数をTrueにすると回答がストリーミング形式で逐次的に表示される
# - リアルタイム性が高まるのでチャットボットだと有用

from openai import OpenAI


# LLMの定義
client = OpenAI()

# 問い合わせ
# --- stream引数をTrueにしている
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "こんにちは！私はジョンと言います！"},
    ],
    stream=True,
)

# 確認
# --- コード全体を実行した場合には逐次的に表示される
# --- スクリプトを逐次的に実行するとストリーミングは目視できない
for chunk in response:
    content = chunk.choices[0].delta.content
    if content is not None:
        print(content, end="", flush=True)
