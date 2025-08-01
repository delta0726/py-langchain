"""
Title   : やさしく学ぶLLMエージェント
Chapter : 3 エージェント
Section : 5 ペルソナのあるエージェント
Theme   : ペルソナ付与のためのメモリ技術
Date    : 2025/08/02
Page    : P134-140
"""

# ＜概要＞
# - ペルソナを効果的に維持するためには、対話のコンテキストを忘れずに管理し続けることが重要
# - メモリ技術を活用することで、エージェントはユーザのペルソナを記憶し、対話の一貫性を保つことができる
# - Mem0を利用して、ユーザのペルソナ情報を記憶し、翻訳機能を組み合わせて多言語対応を実現する

# ＜Mem0ライブラリ＞
# - LangChainなどのLLMベースのアプリケーションに｢永続的な記憶｣を提供するサービス
# - ローカルにない「記憶の保存・検索・共有」機能をAPI経由で外部に委ねている
# - RAGによるベクトル検索によるメモリ検索が可能となる
# - 日本語には十分対応できない可能性があるため、英語に翻訳してから登録する

import os
from mem0 import MemoryClient
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate


# 準備 -----------------------------------

# 共通設定
user_id = "elith_chan"
language = "English"


# インスタンス定義
# --- LLM Model
# --- Mem0
model = ChatOpenAI(model="gpt-4o-mini")
client = MemoryClient(api_key=os.environ["MEM0_API_KEY"])


# 翻訳器の構築 -----------------------------------

# ＜ポイント＞
# - Mem0の翻訳機能を利用するため、ペルソナ情報を英語に翻訳して登録する
#   --- ここでは、LLMを利用して翻訳器を作成する


# プロンプト
# --- 翻訳タスク
message = """
Translate the following text into {language}.
Output only the translated text without any additional information.

text:
{text}
"""

# テンプレートの作成
prompt = ChatPromptTemplate.from_messages(messages=[("human", message)])

# チェーン作成
translate_chain = prompt | model


# 翻訳器の定義
def translate(text: str, language: str = "English") -> str:
    """翻訳チェーンで翻訳"""
    return translate_chain.invoke({"text": text, "language": language}).content


# Mem0を活用したペルソナ管理 -----------------------------------

# ＜ポイント＞
# - Mem0を利用してペルソナ情報を英語に翻訳して登録する
# - 入力した文章や会話の中から保存すべき記憶を抽出して、項目ごとに自動整理して保存している
# - Mem0のメモリは属性情報を整理した辞書形式で保存されている


# メモリ初期化
client.delete_all(user_id=user_id)
user_memories = client.get_all(user_id=user_id)
print(user_memories)

# ペルソナ設定
text = """
私の名前は「えりすちゃん」です。
私は、AI系スタートアップのElithに所属しています。
私はElithを象徴するキャラクターとして、知識と優しさを兼ね備えた存在です。
"""

# 翻訳
text_en = translate(text=text, language=language)
print(text_en)

# メモリに登録
messages = [
    {"role": "user", "content": text_en},
]
client.add(messages=messages, user_id=user_id, output_format="v1.1")

# メモリの利用
user_memories = client.get_all(user_id=user_id)
print(user_memories)


# メモリ情報の検索 ------------------------------------------

# ＜ポイント＞
# - searchメソッドを利用して、特定の情報を検索する
# - 質問事項に関連するメモリ情報が辞書形式で返される


# 質問事項を翻訳
query_ja = "あなたのお仕事は何ですか？"
query_en = translate(text=query_ja, language=language)
print(query_en)

# メモリ検索
search_results = client.search(query=query_en, user_id=user_id)
print(search_results)


# メモリ情報に対しての質問 -----------------------------------

# ＜ポイント＞
# - 抽出したメモリ情報をコンテキストとしてプロンプトに与える
# - メモリ情報を基にした質問応答を行う


# 関数定義
def extract_memory_context(search_result, separator="\n") -> str:
    memories = (
        search_result.get("memories")
        if isinstance(search_result, dict)
        else search_result
    )
    return separator.join(m.get("content", "") for m in memories if m.get("content"))


# メモリ情報の抽出
memory_context = extract_memory_context(search_result=search_results)


# プロンプト定義
human_prompt = """
Answer the question based only on the provided memory.

Memory:
{context}

Question: 
{question}
"""


# 応答プロンプトの定義（LLM による自然な回答）
answer_prompt = ChatPromptTemplate.from_messages(
    messages=[
        ("system", "You are a helpful assistant."),
        ("human", human_prompt),
    ]
)

# チェーン構築
answer_chain = answer_prompt | model

# 応答の生成
response = answer_chain.invoke(
    input={"context": memory_context, "question": query_en}
).content

# 結果を表示
print(response)
