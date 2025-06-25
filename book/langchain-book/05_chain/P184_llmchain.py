"""
Title   : Langchain完全入門
Section : 5 Chain - 複数の処理をまとめる
Theme   : Chainの基本的な流れ
Date    : 2025/04/27
Page    : P184
"""

from langchain import LLMChain, PromptTemplate
from langchain.chat_models import ChatOpenAI


# 大規模言語モデルの定義
llm = ChatOpenAI(model="gpt-4o-mini")

# プロンプトテンプレートの定義
prompt = PromptTemplate(
    template="{product}はどこの会社が開発した製品ですか？", input_variables=["product"]
)

# LLMChainの定義
# --- LLMとプロンプトをセットで管理
# --- プロンプト作成 ⇒ LLM問い合わせ ⇒ 回答取得
chain = LLMChain(llm=llm, prompt=prompt)

# LLMChainの実行
# --- predict()を実行する際に、プロンプトを予め指定した方法で実行
result = chain.predict(product="iPhone")

# 結果確認
print(result)
