import os
import openai
import wikipediaapi


# テキストをチャンクに分割 --- (*1)
def split_text(text, chunk_size=2000):
    chunks = []
    text = text.replace("。", "。\n")
    cur = ""
    for s in text.split("\n"):
        cur += s + "\n"
        if len(cur) > chunk_size:
            chunks.append(cur)
            cur = ""
    if cur != "":
        chunks.append(cur)
    return chunks


# テキストを要約する --- (*2)
def summarize(text, max_len=800):
    # テキストをチャンクに分割
    chunks = split_text(text)
    print(f"=== 要約: チャンク数: {len(chunks)} ===")
    # 要約のためのプロンプトひな形 --- (*3)
    summarize_template = (
        "### 指示:\n次の入力を簡潔に要約してください。\n" + "### 入力:\n```{chunk}```\n"
    )
    # チャンクごとに要約する --- (*4)
    result_all = ""
    for chunk in chunks:
        prompt = summarize_template.format(chunk=chunk)
        print("--- 要約プロンプト ---\n" + prompt)
        result = call_chatgpt(prompt) + "\n"
        print("--- 要約結果 ---\n" + result)
        result_all += result + "\n"
    # 文字数以上であれば再帰的に要約 --- (*5)
    if len(result_all) > max_len:
        result_all = summarize(result_all, max_len)
    return result_all


# ChatGPTのAPIを呼び出す関数 --- (*6)
use_azure = False


def call_chatgpt(prompt):
    if use_azure:
        client = openai.AzureOpenAI()
        completion = client.chat.completions.create(
            model="gpt-4.1-nano", messages=[{"role": "user", "content": prompt}]
        )
    else:
        client = openai.OpenAI()
        completion = client.chat.completions.create(
            model="gpt-4.1-nano", messages=[{"role": "user", "content": prompt}]
        )
    return completion.choices[0].message.content


# Wikipediaから本文を取得 --- (*7)
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


if __name__ == "__main__":
    # Wikipediaからテキストを取得して要約 --- (*8)
    wiki_text = get_wikitext("太陽")
    result = summarize(wiki_text)
    print(f"=== 結果:{len(result)}文字 ===\n{result}")
