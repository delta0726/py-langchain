"""
Title   : Langchain完全入門
Section : 5 Chain - 複数の処理をまとめる
Theme   : 特定機能に特化したChains
Date    : 2025/04/27
Page    : P190
"""

from langchain.chains import LLMChain, LLMRequestsChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate


# 言語モデルの定義
llm = ChatOpenAI()

# プロンプトテンプレートの定義
prompt = PromptTemplate(
    input_variables=["requests_result", "query"],
    template="""
    以下の文章を元に質問に答えてください。
    文章: {requests_result}
    質問: {query}""",
)

# LLMChainの定義
llm_chain = LLMChain(llm=llm, prompt=prompt, verbose=True)

# LLMChainの定義
# ← LLMRequestsChainを初期化
# ← llm_chainにはLLMChainを指定
chain = LLMRequestsChain(llm_chain=llm_chain)

# 問い合わせ
# --- URLを実行すると天気予報の情報がJSONで取得可能
result = chain(
    {
        "url": "https://www.jma.go.jp/bosai/forecast/data/overview_forecast/130000.json",
        "query": "東京の天気について教えて",
    }
)

# 確認
print(result)
