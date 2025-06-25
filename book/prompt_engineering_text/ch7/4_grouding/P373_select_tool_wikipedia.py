# メモ:
# Wikipediaの内容は常に更新されており、書籍執筆時と大きく変わることがあります。
#
# そこで、下記のコードは、執筆当時の内容を再現するように修正しています。
# それで、書籍の結果に近い内容を返すために
# ファイル「wikipedia_cahce_内閣総理大臣.txt」(執筆時のWikipediaの内容を記録したテキスト)と
# ファイル「wikipedia_cahce_横浜市.txt」
# も一緒にコピーしてから実行してください。


import os
import openai
import time
import json
import wikipediaapi
from dotenv import load_dotenv, find_dotenv

# 環境設定
load_dotenv(find_dotenv())
api_key = os.getenv("OPENAI_API_KEY")


# ツールを選択するプロンプト --- (*1)
SELECT_TOOL_TEMPLATE = """
### 指示:
目標を達成するために、与えられたツールの一覧から相応しいツールを選んでください。
### ツール一覧:
- 検索: 指定したキーワードを検索します。
  - 引数:
    - キーワード: 検索キーワード
- 現在時刻: 現在時刻を返します。
- 計算機: 引数に与えた計算式を計算します
  - 引数:
    - 計算式: 計算式を指定
### 目標:
```{input}```
### 出力例:
JSON形式で出力してください。
```json
{"行動": "ツール名", "引数": "ここに引数", "備考": "ここに備考"}
```
"""


# ChatGPTのAPIを呼び出す関数 --- (*2)
def call_chatgpt(prompt):
    client = openai.OpenAI(api_key=api_key)
    completion = client.chat.completions.create(
        model="gpt-4.1-nano", messages=[{"role": "user", "content": prompt}]
    )
    return completion.choices[0].message.content
    return ""


# JSONデータを取得する --- (*3)
def get_json_data(response):
    if "```json" in response:
        response = response.split("```json")[1].split("```")[0]
    try:
        return json.loads(response)
    except Exception as e:
        print("JSONが取得できませんでした。" + e)
    return ""


# Wikipedia APIを呼び出して検索結果を返す --- (*4)
def get_wikipedia(arg):
    wiki = wikipediaapi.Wikipedia("llm-wiki-search", "ja")
    result = ""
    for page_name in arg.split(" "):
        print("wikipedia.page=", page_name)
        # キャッシュを確認
        fname = f"wikipedia_cahce_{page_name}.txt"
        if os.path.exists(fname):
            return open(fname, "r", encoding="utf-8").read()
        # ページを取得
        page = wiki.page(page_name)
        if page.exists():
            summary = f"- {page_name}: {page.summary}\n"
            open(fname, "w").write(summary)
            result += summary
    if result == "":
        result = "追加情報はありませんでした"
    return result


# 検索ツールを利用した時の処理 --- (*5)
def search_tool(question, arg):
    print(f"=== 検索: {arg} ===")
    summary = get_wikipedia(arg)
    print(summary)
    # 取得した情報を元に答えを求める
    prompt = (
        "### 指示:\n以下の情報を参考にして質問に答えてください。\n"
        + f"### 情報:\n```{summary}```\n"
        + f"### 質問:\n```"
        + question
        + "```"
    )
    print("=== 回答プロンプト ===\n" + prompt)
    return call_chatgpt(prompt)


# ツールを選択するプロンプトを実行 --- (*6)
def selec_tool(question):
    # プロンプトを実行
    question = question.replace("`", '"')  # 「`」をエスケープ
    st_prompt = SELECT_TOOL_TEMPLATE.replace("{input}", question)
    print("=== 行動選択プロンプト ===\n" + st_prompt)
    res = call_chatgpt(st_prompt)
    print("=== 応答 ===\n" + res)
    data = get_json_data(res)
    action = data["行動"]
    arg = data["引数"]
    memo = data["備考"]
    # 言語モデルが選んだツールに応じて処理を行う --- (*7)
    if action == "計算機":
        val = eval(arg)  # 引数を計算
        return f"=== 計算機 ===\n{memo} → {val}"
    elif action == "現在時刻":
        return time.strftime("%Y年%m月%d日 %H:%M") + "→" + memo
    elif action == "検索":
        return search_tool(question, arg)
    else:
        return "ツールが見つかりませんでした。" + res


# メイン処理 --- (*8)
if __name__ == "__main__":
    prompt = "内閣総理大臣は誰ですか？"
    res = selec_tool(prompt)
    print("=== 結果 ===\n" + res)
