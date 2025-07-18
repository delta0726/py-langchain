"""
Title   : やさしく学ぶLLMエージェント
Chapter : 2 エージェント作成のための基礎知識
Section : 2 LangChain入門 
Theme   : チャットアプリケーション
Date    : 2025/07/12
Page    : P44-46
"""

# ＜ポイント＞
# - ロールごとのメッセージはHumanMessage/AiMessage/SystemMessageで区別する
# - pretty_print()はロールを明示したうえで会話コンテンツを表示する


from langchain_openai.chat_models import ChatOpenAI
from langchain_core.messages import HumanMessage


# モデルの定義
llm = ChatOpenAI(model="gpt-4o-mini")

# 変数定義
history = []
n = 5

# 会話シナリオ
user_inputs = [
    "こんにちは！",
    "最近の天気はどうですか？",
    "おすすめの本はありますか？",
    "週末に何をするとリラックスできますか？",
    "ありがとう、またね！"
]

user_input = user_inputs[0]
for user_input in user_inputs:
    # 1 HumanMessage の作成と表示
    human_message = HumanMessage(content=user_input)
    human_message.pretty_print()
    
    # 2 会話履歴の追加
    history.append(human_message)
    
    # 3 応答の作成と表示
    ai_message = llm.invoke(input=history)
    ai_message.pretty_print()
    
    # 4 会話履歴の追加
    history.append(ai_message)
