import openai
import json
import wikipediaapi
import chromadb_summarize as summarize

# 検索キーワードを取得するためのプロンプトのひな形 --- (*1)
SEARCH_KEYWORD_TEMPLATE = """
### 指示:
次の質問に答えるためにWikipediaを検索します。
取得すべき情報ページのタイトルをいくつか列挙してください。
### 質問:
```{question}```
### 出力形式:
JSON形式で出力してください。
```json
["タイトル1", "タイトル2", "タイトル3"]
```
"""

# 質問に答えるためのプロンプトのひな形 --- (*2)
QA_TEMPLATE = """
### 指示:
次の情報を参考にして質問に答えてください。
なお、途中経過を一つずつ列挙しながら、質問の答えを考えてください。
### 情報:
```{info}```
### 質問:
```{question}```
"""


# 質問を行う関数 --- (*3)
def ask_question(question):
    # 検索キーワードを決定する --- (*4)
    question = question.replace("`", '"')  # エスケープ
    prompt = SEARCH_KEYWORD_TEMPLATE.format(question=question)
    result = summarize.call_chatgpt(prompt)
    print("=== 検索キーワード ===\n", result)
    title_list = json.loads(result)
    # 記事を取得してDBに保存 --- (*5)
    for title in title_list:
        text = summarize.get_wikitext(title)
        summarize.insert_text(f"{title}: {text}")
    # 質問と関係のありそうなテキストを取得 --- (*6)
    info = summarize.query_text(question)
    # 質問に答えてもらう --- (*7)
    prompt = QA_TEMPLATE.format(info=info, question=question)
    print("=== 質問プロンプト ===\n", prompt)
    result = summarize.call_chatgpt(prompt)
    print("=== 回答 ===\n", result)
    return result


if __name__ == "__main__":
    # 実際に質問する --- (*8)
    question = "月が地球に与える影響を教えてください。"
    ask_question(question)
