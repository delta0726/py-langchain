"""
Title   : Langchain完全入門
Section : 3 Retrieval
Theme   : DBからの質問に関連する箇所を抽出してLLMに問い合わせ
Date    : 2025/04/27
Page    : P112
"""

from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.prompts import PromptTemplate
from langchain.schema import HumanMessage
from langchain.vectorstores import Chroma


# DBから質問への関連殿高いデータを取得 ----------------------------------------

# 大規模言語モデルの構築
# --- ベクトル化するための言語モデル
embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")

# DB定義
database = Chroma(persist_directory=".data", embedding_function=embeddings)

# データベースから類似度の高いドキュメントを取得
query = "飛行車の最高速度は？"
documents = database.similarity_search(query=query)

# ドキュメントの内容を格納する変数を初期化
documents_string = ""
for document in documents:
    documents_string += f"""
    ---------------------------
    {document.page_content}
    """


# DBから質問への関連殿高いデータを取得 ----------------------------------------

# 大規模言語モデルの構築
# --- 問い合わせのための言語モデル
chat = ChatOpenAI(model="gpt-4o-mini")

# プロンプトの作成
# --- テンプレートを使用して変数の基づくプロンプトを作成
prompt = PromptTemplate(
    template="""
    文章を元に質問に答えてください。 

    文章: 
    {document}

    質問: 
    {query}
    
    """,
    input_variables=["document", "query"],
)

# 問い合わせ
# --- 抽出した文章のみを使用
# --- queryはDB検索の時と同じ
result = chat(
    [HumanMessage(content=prompt.format(document=documents_string, query=query))]
)

# 確認
print(result.content)
