"""
Title   : Langchain完全入門
Section : 5 Chain - 複数の処理をまとめる
Theme   : 会話履歴の記憶を持たせたChainの構築
Date    : 2025/04/27
Page    : P187
"""

from langchain.chains import ConversationChain
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory


#  言語モデルの定義
llm = ChatOpenAI()

# メモリ定義
# --- 会話履歴をためて、次のやりとりに活かすためのメモリを用意
memory = ConversationBufferMemory(return_messages=True)


# LLMChainの定義
# --- 言語モデルとメモリをセットで管理
chain = ConversationChain(memory=memory, llm=llm)
