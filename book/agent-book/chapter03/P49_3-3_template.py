"""
Title   : LangChainとLangGraphによるRAG・AIエージェント実践入門
Chapter : 3 プロンプトエンジニアリング
Section : 
Theme   : プロンプトのテンプレート化
Date    : 2025/05/07
Page    : P49-50
"""

# ＜ポイント＞
# - テンプレート化の本質は｢命令｣と｢入力データ｣の分離にある
# - 本例のように"""や###で区切ることで入力データを明示することが多い
# - プロンプトのテンプレート化はformatメソッドやf-stringで行うのがベーシック
# - この方法はクラスなどは使わず、Python本来の機能でプロンプトを書いている
# - 素直な方法ではあるが応用が利かないので実務には適さない

from openai import OpenAI

# LLMの定義
client = OpenAI()

# テンプレートの作成
prompt = '''\
以下の料理のレシピを考えてください。

料理名: """
{dish}
"""
'''

# 動作確認
dish = "カレー"
print(prompt.format(dish=dish))


# 関数定義
# --- テンプレートに基づく問い合わせを実行
# --- 文字列のfomartメソッドを使っただけなので応用は利かない
def generate_recipe(dish: str) -> str:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": prompt.format(dish=dish)},
        ],
    )
    return response.choices[0].message.content


# 問い合わせ
recipe = generate_recipe("カレー")

# 結果確認
print(recipe)
