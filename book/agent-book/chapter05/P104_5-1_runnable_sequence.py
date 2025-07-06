"""
Title   : LangChainとLangGraphによるRAG・AIエージェント実践入門
Chapter : 5 LangeChain Expression Language(LCEL)の徹底解説
Section : RunnableとRunnableSequence（LCELの最も基本的な構成要素）
Theme   : Runnableの実行方法 - invoke/stream/batch
Date    : 2025/06/04
Page    : P104-106
"""

# ＜概要＞
# - LCELの基本実行はプロンプト/モデル/出力パーサーの3つを連結すること
# - 上記の3つのメソッドは全てinvoke()で実行することができる
# - 各オブジェクトはRunnableを基底クラスを持ち、LCELはこれを利用して実行している

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI


# コンポーネント定義 ------------------------------------------

# プロンプト
prompt = ChatPromptTemplate.from_messages(
    messages=[
        ("system", "ユーザーが入力した料理のレシピを考えてください。"),
        ("human", "{dish}"),
    ]
)

# モデル
model = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# 出力パーサー
output_parser = StrOutputParser()


# コンポーネントごとにinvokeを実行 -----------------------------

# ＜ポイント＞
# - LangChainのコンポーネントは全てinvoke()を実行することができる
# - コンポーネントごとに実行される内容は異なる

# プロンプト
# --- メッセージのオブジェクトを抽出する
prompt_value = prompt.invoke(input={"dish": "カレー"})
print(prompt_value)

# LLMモデル
# --- 問い合わせを実行する
ai_message = model.invoke(input=prompt_value)
print(ai_message)

# 出力パーサー
# --- 問い合わせ結果を抽出する
output = output_parser.invoke(input=ai_message)
print(output)


# Chainによる問い合わせ --------------------------------------

# ＜ポイント＞
# - チェインは各コンポーネントをRunnableSequenceに統合している
# - チェインに対しても通常形式(invoke)を適用することができる
# - 同様にストリーミング形式(stream)/バッチ形式(batch)にも対応


# チェーン構築
chain = prompt | model | output_parser

# 問い合わせ
# --- 通常形式
output = chain.invoke({"dish": "カレー"})
print(output)


# 問い合わせ
# --- ストリーミング形式（逐次的に出力）
for chunk in chain.stream({"dish": "カレー"}):
    print(chunk, end="", flush=True)

# 問い合わせ
# --- バッチ形式（複数処理を一括で実行）
outputs = chain.batch([{"dish": "カレー"}, {"dish": "うどん"}])
print(outputs)
