"""
Title   : LangChainとLangGraphによるRAG・AIエージェント実践入門
Chapter : 4 LangChainの基礎
Section : 3 Prompt Template
Theme   : マルチモーダルで画像について問い合わせ
Date    : 2025/05/16
Page    : P77
"""

# ＜ポイント＞
# - マルチモーダルとは、テキストだけでなく画像や音声など複数の形式のデータを同時に扱うこと
#   --- LLMはテキスト以外にも画像や音声などのデータを入力として受け取ることができる

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI


# プロンプト定義
prompt = ChatPromptTemplate.from_messages(
    messages=[
        (
            "user",
            [
                {"type": "text", "text": "画像を説明してください。"},
                {"type": "image_url", "image_url": {"url": "{image_url}"}},
            ],
        ),
    ]
)

# プロンプト作成
image_url = "https://raw.githubusercontent.com/yoshidashingo/langchain-book/main/assets/cover.jpg"
prompt_value = prompt.invoke({"image_url": image_url})

# 問い合わせ
model = ChatOpenAI(model="gpt-4o", temperature=0)
ai_message = model.invoke(input=prompt_value)

# 結果確認
print(ai_message.content)
