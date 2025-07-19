"""
Title   : やさしく学ぶLLMエージェント
Chapter : 3 エージェント
Section : 5 ペルソナのあるエージェント
Theme   : ペルソナ付与のためのメモリ技術
Date    : 2025/07/19
Page    : P134-140
"""

import os
from mem0 import MemoryClient
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate


# --- 初期化 ---

user_id = "elith_chan"
language = "English"

# Mem0 クライアントの初期化
client = MemoryClient(api_key=os.environ["MEM0_API_KEY"])

# モデル・プロンプトの準備
message = """
Translate the following text into {language}.

text:
{text}
"""
prompt = ChatPromptTemplate.from_messages([("human", message)])
model = ChatOpenAI(model="gpt-4o-mini")
translate_chain = prompt | model


# --- ヘルパー関数 ---


def translate(text: str, language: str = "English") -> str:
    """翻訳チェーンで翻訳"""
    return translate_chain.invoke({"text": text, "language": language}).content


# --- ユーザのメモリ初期化 ---

client.delete_all(user_id=user_id)

user_memories = client.get_all(user_id=user_id)
print(user_memories)


# --- 翻訳して登録 ---

text = """
私の名前は「えりすちゃん」です。
私は、AI系スタートアップのElithに所属しています。
私はElithを象徴するキャラクターとして、知識と優しさを兼ね備えた存在です。
"""
print(translate(text, language))

text = """
私の名前は「えりすちゃん」です。
私は、AI系スタートアップのElithに所属しています。
私はElithを象徴するキャラクターとして、知識と優しさを兼ね備えた存在です。
Elithのことを世の中に発信することが私の仕事です。
"""
text_en = translate(text, language)

messages = [
    {"role": "user", "content": text_en},
]
client.add(messages, user_id=user_id, output_format="v1.1")

user_memories = client.get_all(user_id=user_id)
print(user_memories)


# --- クエリを翻訳して検索 ---

query_ja = "あなたのお仕事は何ですか？"
query_en = translate(query_ja, language)

client.search(query_en, user_id=user_id)
