"""
Title   : LangChainとLangGraphによるRAG・AIエージェント実践入門
Chapter : 3 プロンプトエンジニアリング
Section : 
Theme   : 出力形式を指定する
Date    : 2025/05/07
Page    : P52
"""

# ＜ポイント＞
# - 出力形式をJSONにするとアプリケーションの処理の連携性が高まる
# - いかにJSONに上手く出力するかが腕の見せどころ
# - 本例ではプロンプトでJSON形式での出力を指示している
# - response_formatでJSONを指定することで安定性が増す(P30)

from openai import OpenAI

# LLMの定義
client = OpenAI()


# 関数定義
# --- JSONフォーマットで出力
def generate_recipe(dish: str) -> str:
    system_prompt = """\
    ユーザーが入力した料理のレシピを考えてください。

    出力は以下のJSON形式にしてください。

    ```
    {
    "材料": ["材料1", "材料2"],
    "手順": ["手順1", "手順2"]
    }
    ```
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"{dish}"},
        ],
    )
    return response.choices[0].message.content


# 問い合わせ
recipe = generate_recipe(dish="カレー")

# 結果確認
print(recipe)
