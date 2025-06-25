import os
import openai
import time
import json
from dotenv import load_dotenv, find_dotenv

# 環境設定
load_dotenv(find_dotenv())
api_key = os.getenv("OPENAI_API_KEY")


# ツールを選択するプロンプト --- (*1)
SELECT_TOOL_TEMPLATE = """
### 指示:
与えられたツールの一覧から相応しいツールを選んで、目標を達成するために努力してください。
### ツール一覧:
- 計算機: 引数に与えた計算式を計算します
  - 引数:
    - 計算式: 計算式を指定
- 検索: 指定したキーワードを検索します。
  - 引数:
    - キーワード: 検索キーワード
- 現在時刻: 現在時刻を返します。
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


# ツールを選択するプロンプトを実行 --- (*3)
def select_tool(prompt):
    # プロンプトを実行
    prompt = prompt.replace("`", '"')  # 「`」をエスケープ
    st_prompt = SELECT_TOOL_TEMPLATE.replace("{input}", prompt)
    res = call_chatgpt(st_prompt)
    print("=== 応答 ===\n" + res)
    try:
        # JSONを取得 --- (*4)
        if "```json" in res:
            res = res.split("```json")[1].split("```")[0]
        # 文字列をJSONに変換 --- (*4a)
        data = json.loads(res)
        action = data["行動"]
        arg = data["引数"]
        memo = data["備考"]
        # 言語モデルが選んだツールに応じて処理を行う --- (*5)
        if action == "計算機":
            val = eval(arg)
            return f"{memo}→{val}"  # 引数を計算して返す
        elif action == "検索":
            return f"「{arg}」を検索します。(TODO)" + memo
        elif action == "現在時刻":
            return time.strftime("%Y年%m月%d日 %H:%M") + "→" + memo
        else:
            return "ツールが見つかりませんでした。" + res
    except Exception as e:
        return "JSONが取得できませんでした。" + e


# メイン処理 --- (*6)
if __name__ == "__main__":
    prompt = "4300円の柿を30箱、3000円の苺を50箱買いました。合計いくらですか？"
    res = select_tool(prompt)
    print("=== 結果 ===\n" + res)
    time.sleep(3)
