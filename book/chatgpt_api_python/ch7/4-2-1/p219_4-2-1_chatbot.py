"""
Title   : Chatgpt API & Python
Section : 7 PDFからデータを抽出してグラフ化しよう
Theme   : PDFファイルを読み込んで簡易チャットボットを作成する
Date    : 2025/05/05
Page    : P219
"""

from langchain.document_loaders import PyPDFLoader
from langchain_openai import OpenAIEmbeddings
from langchain.indexes import VectorstoreIndexCreator
from langchain_openai import OpenAI

"""
質問： シン・トセイの戦略の重要点は？
"""

# PDF検索システムの構築
# --- 簡易的なインメモリのベクトル検索インデックスを作成
loader = PyPDFLoader(file_path="pdf/digital_01_202107_keikaku.pdf")
embedding = OpenAIEmbeddings()
index = VectorstoreIndexCreator(embedding=embedding).from_loaders([loader])

# LLMの定義
llm = OpenAI()

# 質問
# --- ユーザーの質問を受け取る
# --- 質問文をベクトル化してPDFから抽出した文書のチャンクと類似度検索最しチャンクを抽出
# --- それらのチャンク（=コンテキスト）と質問をLLMに渡して回答生成
print("質問を入力してください")
answer = index.query(input(), llm=llm)

# 回答
# --- インデックス検索結果を要約・再構成して返している
print(answer)
