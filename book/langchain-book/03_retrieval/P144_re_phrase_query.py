"""
Title   : Langchain完全入門
Section : 3 Retrieval
Theme   : Wikipedia Retriverを使ったテキスト取得
Date    : 2025/04/29
Page    : P144
"""

from langchain.chat_models import ChatOpenAI
from langchain.retrievers import WikipediaRetriever, RePhraseQueryRetriever
from langchain import LLMChain
from langchain.prompts import PromptTemplate


# インスタンス構築
llm = ChatOpenAI(temperature=0)

# Retrievalの定義
retriever = WikipediaRetriever(lang="ja", doc_content_chars_max=500)

# プロンプトの定義
prompt = PromptTemplate(
    input_variables=["question"],
    template="""
    以下の質問からWikipediaで検索するべきキーワードを抽出してください。
    質問: {question}
    """
    )

# Chainの定義
# --- プロンプトとLLMをセットにする
llm_chain = LLMChain(llm=llm, prompt=prompt)

# Retriverの構築
re_phrase_query_retriever = RePhraseQueryRetriever(
    llm_chain=llm_chain, 
    retriever=retriever
    )

# 問い合わせ
query = "私はラーメンが好きです。ところでバーボンウイスキーとは何ですか？"
documents = re_phrase_query_retriever.get_relevant_documents(query=query)

# 結果確認
print(documents)
