"""
Title   : LangChainとLangGraphによるRAG・AIエージェント実践入門
Chapter : 4 LangChainの基礎
Section : 3 Prompt Template
Theme   : プロンプト・テンプレート
Date    : 2025/05/14
Page    : P73
"""


# ＜ポイント＞
# - プロンプトはテンプレート化することができて専用のクラスも用意されている
#   --- 引数をテンプレートに埋め込むことで、柔軟なプロンプトを作成できる
#   --- 引数は辞書形式で複数指定することも、単一の文字列で指定することもできる

from langchain_core.prompts import PromptTemplate


# テンプレート定義
# --- {dish}などとしてプレースホルダーとして変数を指定する
# --- f-stringの記法と同様だが、template引数の中ではf''の指定は不要
prompt = PromptTemplate.from_template(
    template="""
    以下の料理のレシピを考えてください。
    料理名: {dish}
    """
)

# プロンプト作成
# --- 変数が複数の場合は辞書で指定
# --- 変数が1つの場合は文字列指定も可能
prompt_value_1 = prompt.invoke(input={"dish": "カレー"})
prompt_value_2 = prompt.invoke(input="カレー")

# 結果表示
print(prompt_value_1.text)
print(prompt_value_2.text)
