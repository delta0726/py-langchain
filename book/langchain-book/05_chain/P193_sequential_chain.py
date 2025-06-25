"""
Title   : Langchain完全入門
Section : 5 Chain - 複数の処理をまとめる
Theme   : 複数のタスク(Chain)をまとめて1つのChainを作る
Date    : 2025/04/27
Page    : P193
"""

from langchain.chains import LLMChain, SimpleSequentialChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate


# 言語モデルの定義
llm = ChatOpenAI(model="gpt-4o-mini")

# LLMChainの定義
# --- 記事を書くLLMChainを作成
write_article_chain = LLMChain(
    llm=llm,
    prompt=PromptTemplate(
        template="{input}についての記事を書いてください。",
        input_variables=["input"],
    ),
)

# LLMChainの定義
# --- 翻訳するLLMChainを作成
translate_chain = LLMChain(
    llm=llm,
    prompt=PromptTemplate(
        template="以下の文章を英語に翻訳してください。\n{input}",
        input_variables=["input"],
    ),
)

# Chainをまとめる
# --- SimpleSequentialChainを作成
# --- 実行順序に基づいてChainを指定
sequential_chain = SimpleSequentialChain(
    chains=[
        write_article_chain,
        translate_chain,
    ]
)

# 問い合わせ
result = sequential_chain.invoke("エレキギターの選び方")

# 確認
print(result)
