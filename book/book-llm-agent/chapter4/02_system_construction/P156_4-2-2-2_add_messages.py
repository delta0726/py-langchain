"""
Title   : やさしく学ぶLLMエージェント
Chapter : 4 マルチエージェント
Section : 2 マルチエージェントシステムの構築
Theme   : add_messagesを活用したチャット履歴の管理
Date    : 2025/08/03
Page    : P156
"""


# ＜概要＞
# - add_messagesを使うことでチャット履歴を安全かつ意図どおりに拡張させることができる

from langchain.schema import HumanMessage
from langchain_core.messages import AIMessage
from langgraph.graph.message import add_messages
from pprint import pprint


# 単独メッセージ -----------------------------------------

# ＜ポイント＞
# - メッセージ単位ごとにリストに格納される
#   --- 単発のメッセージはリストに1つのHumanMessageやAIMessageのオブジェクトを格納する

# メッセージ定義
human_messages = [HumanMessage(content="こんにちは")]
ai_message = [AIMessage(content="こんにちは！")]

# 確認
pprint(human_messages)
pprint(ai_message)


# メッセージ追加 -----------------------------------------

# ＜ポイント＞
# - リストにメッセージを追加していくことでチャット履歴を管理することができる
#   --- add_messagesを使うことでチャット履歴を安全かつ直観的に管理することができる

# メッセージの追加
messages = add_messages(human_messages, ai_message)

# 確認
pprint(messages)
