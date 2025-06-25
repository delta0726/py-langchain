"""
Title   : Langchain完全入門
Section : 2 Language Models
Theme   : プロンプトエンジニアリングを反映して質問する
Date    : 2025/04/26
Page    : P78
"""

from langchain.llms import OpenAI
from langchain.prompts import FewShotPromptTemplate, PromptTemplate


"""
＜ポイント＞
- プロンプト・エンジニアリングは、AIに対して適切な指示を与えるための技術
- Few-Shot Promptは、AIに対して具体的な例を与えることで、より正確な回答を引き出す手法
- 定型化された方法の1つであり、一連の処理がクラス化されている
"""

# 言語モデルの定義
# --- 高価なモデルなので実行しない
# llm = OpenAI(model="gpt-3.5-turbo-instruct")
llm = OpenAI(model="not-available")


# テンプレートの定義
# --- inputとoutputを入力変数として設定
# --- この時点でもプロンプトとして成立
prompt = PromptTemplate(
    input_variables=["input", "output"],
    template="入力: {input}\n出力: {output}",
)

# サンプルを定義
# --- Few-Shot Promptは例を与えて回答精度を高める手法
# --- 入力例/出力例
ex_input = """
LangChainは
ChatGPT・Large Language Model (LLM)の実利用をより柔軟に
簡易に行うためのツール群です
"""

ex_output = """
LangChainは、
ChatGPT・Large Language Model (LLM)の実利用をより柔軟に、
簡易に行うためのツール群です。
"""

examples = [{"input": ex_input, "output": ex_output}]

# 追加指示
prefix = """
以下の句読点の抜けた入力に句読点を追加してください。
追加して良い句読点は「、」「。」のみです。
他の句読点は追加しないでください。
"""

# プロンプトの定義
# --- example引数で入力例と出力例を定義
# --- example_prompt引数でテンプレートを渡す
# --- prefix(指示) ⇒ example(テンプレート) ⇒ suffix(出力場所)
few_shot_prompt = FewShotPromptTemplate(
    examples=examples,
    example_prompt=prompt,
    prefix=prefix,
    suffix="入力:\n{input_string}\n出力:\n",
    input_variables=["input_string"],
)

# プロンプトの作成
# --- FewShotPromptTemplateを使ってプロンプトを作成
formatted_prompt = few_shot_prompt.format(
    input_string="私はさまざまな機能がモジュールとして提供されているLangChainを使ってアプリケーションを開発しています"
)

# 問い合わせ
result = llm.predict(formatted_prompt)

# 確認
# --- プロンプト
# --- 回答
print("formatted_prompt: ", formatted_prompt)
print("result: ", result)
