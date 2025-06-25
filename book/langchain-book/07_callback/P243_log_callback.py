"""
Title   : Langchain完全入門
Section : 7 Callbacks - さまざまなイベント発生時に処理を行う
Theme   : コールバックを使って特定処理の前後でログ取得を行う
Date    : 2025/04/30
Page    : P243
"""

from langchain.callbacks.base import BaseCallbackHandler
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage


# Callbackを作成する
# --- ***CallbackHandlerという名前にするのが慣例
# --- on_chat_model_start()は実行され、on_chain_start()は実行されない
class LogCallbackHandler(BaseCallbackHandler):
    def on_chat_model_start(self, serialized, messages, **kwargs):
        print("Chat modelsの実行を開始します....")
        print(f"入力: {messages}")

    def on_chain_start(self, serialized, inputs, **kwargs):
        print("Chainの実行を開始します....")
        print(f"入力: {inputs}")


# LLMの設定
chat = ChatOpenAI(
    model="gpt-4o-mini",
    callbacks=[LogCallbackHandler()],
)

# 問い合わせ
result = chat.invoke(
    [
        HumanMessage(content="こんにちは！"),
    ]
)

# 結果確認
print(result.content)
