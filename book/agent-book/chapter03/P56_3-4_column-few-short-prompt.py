"""
Title   : LangChainとLangGraphによるRAG・AIエージェント実践入門
Chapter : 3 プロンプトエンジニアリング
Section : 
Theme   : Few-Shotプロンプティングの表記方法
Date    : 2025/05/11
Page    : P56
"""

# ＜ポイント＞
# - 1つのプロンプトで例示を列挙する方法と、ロールを明示しながら列挙する方法がある
# - プログラムが複雑になりやすい個所なので、スッキリ管理する方法を明確にしておくとよい

from openai import OpenAI

# LLMの定義
client = OpenAI()


# 方法1: プロンプトの中で例を作成する ----------------------------------

# プロンプト定義
prompt = """\
入力がAIに関係するか回答してください。

Q: AIの進化はすごい
A: true
Q: 今日は良い天気だ
A: false
Q: ChatGPTはとても便利だ
A: 
"""

# 問い合わせ
# --- ユーザープロンプトの中で与える
response = client.completions.create(
    model="gpt-3.5-turbo-instruct",
    prompt=prompt,
)

# 結果確認
print(response.choices[0].text)


# 方法2: ロールを明示しながら与える --------------------------------------

# 問い合わせ
# --- システムプロンプトの中で例を提示する
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "入力がAIに関係するか回答してください。"},
        {"role": "system", "name": "example_user", "content": "AIの進化はすごい"},
        {"role": "system", "name": "example_assistant", "content": "true"},
        {"role": "system", "name": "example_user", "content": "今日は良い天気だ"},
        {"role": "system", "name": "example_assistant", "content": "false"},
        {"role": "user", "content": "ChatGPTはとても便利だ"},
    ],
)

# 結果確認
print(response.choices[0].message.content)


# 参考：例をスッキリ管理する工夫 --------------------------------

# 質問＆回答の管理
# --- 長くなるのであればJSONファイルで管理
few_shot_examples = [
    {"user": "AIの進化はすごい", "assistant": "true"},
    {"user": "今日は良い天気だ", "assistant": "false"},
    {"user": "ChatGPTはとても便利だ", "assistant": "true"},
]

# メッセージ構築
messages = [{"role": "system", "content": "入力がAIに関係するか回答してください。"}]
for ex in few_shot_examples[:-1]:  # 最後は質問用に分けておく
    messages.append({"role": "user", "content": ex["user"]})
    messages.append({"role": "assistant", "content": ex["assistant"]})

# 最後のテスト入力
messages.append({"role": "user", "content": few_shot_examples[-1]["user"]})

# 出力
print(messages)
