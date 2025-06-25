"""
Title   : LangChainとLangGraphによるRAG・AIエージェント実践入門
Chapter : 3 プロンプトエンジニアリング
Section : 
Theme   : 文脈を与える
Date    : 2025/05/07
Page    : P50
"""

# ＜ポイント＞
# - 前提条件や外部情報などを文脈として与えると、文脈に従った回答を得ることができる
# - 前提条件を明示することで意図した回答が得られるようになる
# - 一般的かつ直感的な処理なため、特別なテクニックとは見なせない

from openai import OpenAI

# LLMの定義
client = OpenAI()


# 関数定義
# --- テンプレートに基づく問い合わせ
def generate_recipe(dish: str) -> str:
    # テンプレートの作成
    prompt = """
    ユーザーが入力した料理のレシピを考えてください。

    前提条件: '''
    分量: 一人分
    味の好み: 辛口
    '''

    料理名: '''
    {dish}
    '''
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": {prompt},
            },
            {"role": "user", "content": f"{dish}"},
        ],
    )
    return response.choices[0].message.content


# 問い合わせ
recipe = generate_recipe("カレー")

# 結果確認
print(recipe)
