import chromadb, os, wikipediaapi, openai
from chromadb.utils import embedding_functions

# Embeddingに利用するモデルを指定 --- (*1)
embedding_model_name = "stsb-xlm-r-multilingual"
# ChromaDBを初期化してコレクションを作成 --- (*2)
os.environ["TOKENIZERS_PARALLELISM"] = "false"
embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name=embedding_model_name
)
chroma_client = chromadb.EphemeralClient()
collection = chroma_client.get_or_create_collection(
    name="test", embedding_function=embedding_fn
)


# Wikipediaの本文を取得 --- (*3)
def get_wikitext(wiki_title):
    wiki = wikipediaapi.Wikipedia("llm-wiki-search", "ja")
    wiki_file = os.path.join("./", f"__{wiki_title}.txt")
    if not os.path.exists(wiki_file):
        page = wiki.page(wiki_title)  # ページを取得
        if not page.exists():
            return f"{wiki_title}が存在しません。"
        with open(wiki_file, "w", encoding="utf-8") as f:
            f.write(page.text)  # 本文を保存
    with open(wiki_file, "r", encoding="utf-8") as f:
        text = f.read()
        print(f"=== Wikipedia: {wiki_title} ({len(text)}字) ===")
        return text


# データベースにテキストを追加 --- (*4)
def insert_text(text, chunk_size=500):
    # 文章を一定量のチャンクに分割
    chunks = []
    paragraphs = text.split("\n")
    cur = ""
    for s in paragraphs:
        cur += s + "\n"
        if len(cur) > chunk_size:
            chunks.append(cur)
            cur = ""
    if cur != "":
        chunks.append(cur)
    print(f"=== チャンク数: {len(chunks)} ===\n")
    # print('----\n'.join(chunks))
    # 文章をコレクションに追加 --- (*5)
    collection.add(
        ids=[f"{text[0:5]}{i + 1}" for i in range(len(chunks))],  # 適当にIDを付与
        documents=chunks,
    )


# データベースから類似テキストを取得 --- (*6)
def query_text(query, max_len=1500):
    # 類似する文章を検索 --- (*7)
    docs = collection.query(query_texts=[query], n_results=10, include=["documents"])
    doc_list = docs["documents"][0]
    # 結果よりmax_lenだけ抽出 --- (*8)
    doc_result = ""
    for doc in doc_list:
        if len(doc_result + doc) > max_len:
            break
        doc_result += doc.strip() + "\n-----\n"
    return doc_result


# テキストを要約する --- (*9)
def llm_summarize(text, query):
    # テキストをデータベースに追加
    insert_text(text)
    # データベースから類似テキストを取得
    doc_result = query_text(query)
    # 大規模言語モデルを使って要約する
    prompt = (
        f"### 指示:\n以下の情報を参考にして要約してください。\n"
        + f"特に「{query}」に注目してください。\n"
        + f"### 情報:\n```{doc_result}```\n"
    )
    print("=== 回答プロンプト ===\n" + prompt)
    result = call_chatgpt(prompt)
    print("=== 結果 ===\n" + result)
    return result


# ChatGPTのAPIを呼び出す関数 --- (*10)
def call_chatgpt(prompt):
    client = openai.OpenAI()
    completion = client.chat.completions.create(
        model="gpt-4.1-nano", messages=[{"role": "user", "content": prompt}]
    )
    return completion.choices[0].message.content


if __name__ == "__main__":
    # Wikipediaからテキストを取得してポイントを指定して要約 --- (*11)
    title = "横浜市"
    query = "人口の推移"
    wiki_text = get_wikitext(title)
    llm_summarize(wiki_text, query)
