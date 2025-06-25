"""
Title   : LangChainとLangGraphによるRAG・AIエージェント実践入門
Chapter : 3 プロンプトエンジニアリング
Section : 
Theme   : システムロールの活用
Date    : 2025/05/07
Page    : P50
"""

# ＜LLMのロール＞
# system   : LLMモデルに対する初期の指示（人格や振る舞いを定義）
# user     : 人間からの発話（指示、質問）
# assistant: LLMモデルからの応答

# ＜Systemロールの使いどころ＞
# 1. 人格・専門性の定義
# 2. 口調・文体の設定
# 3. 禁止事項・制約の指示（不要なことを避けたいとき）
# 4. タスクの役割・制限の明示（GPTがどう振る舞うべきかを明確にする）
# 5. 思考スタイルや出力形式の制御（エージェント系やChainとの併用時に非常に重要）

# ＜ポイント＞
# - テンプレートの｢命令｣の部分をsystemロールとして分離することもできる
# - 使いどころの3を応用したイメージ
# - 具体的には｢命令｣をsystemのcontentsに書いてしまう

from openai import OpenAI

# LLMの定義
client = OpenAI()


# 関数定義
# --- テンプレートに基づく問い合わせ
def generate_recipe(dish: str) -> str:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "ユーザーが入力した料理のレシピを考えてください。",
            },
            {"role": "user", "content": f"{dish}"},
        ],
    )
    return response.choices[0].message.content


# 問い合わせ
recipe = generate_recipe(dish="カレー")

# 結果確認
print(recipe)
