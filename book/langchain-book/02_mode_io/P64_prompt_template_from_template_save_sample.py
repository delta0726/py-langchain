"""
Title   : Langchain完全入門
Section : 2 Language Models
Theme   : テンプレートの保存と再利用
Date    : 2025/04/25
Page    : P64
"""

from langchain.prompts import PromptTemplate
from langchain.prompts import load_prompt


# プロンプトの作成
# --- テンプレート形式で作成
prompt = PromptTemplate(
    template="{product}はどこの会社が開発した製品ですか？", input_variables=["product"]
)

# JSONに変換して保存
# --- JSON保存はテンプレート集を作成する際に有効
prompt.save("prompt/prompt.json")

# プロンプトのロード
# --- PromptTemplateのオブジェクトとして読み込まれる
loaded_prompt = load_prompt("prompt/prompt.json")
type(loaded_prompt)
vars(loaded_prompt)
