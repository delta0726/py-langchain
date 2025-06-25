"""
Title   : Langchain完全入門
Section : 2 Language Models
Theme   : キャッシュの活用
Date    : 2025/04/26
Page    : P71
"""

import time
import langchain
from langchain.cache import InMemoryCache
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage

# インスタンスの作成
#  --- LLMの構築
#  --- llm_cacheにInMemoryCacheを設定
chat = ChatOpenAI()
langchain.llm_cache = InMemoryCache()


# 1回目の処理
start = time.time()
result = chat([HumanMessage(content="こんにちは！")])
end = time.time()
print(result.content)
print(f"実行時間: {end - start}秒")

# 2回目の処理
start = time.time()
result = chat([HumanMessage(content="こんにちは！")])
end = time.time()
print(result.content)
print(f"実行時間: {end - start}秒")
