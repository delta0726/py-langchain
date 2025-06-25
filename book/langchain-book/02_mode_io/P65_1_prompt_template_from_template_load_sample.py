"""
Title   : Langchain完全入門
Section : 2 Language Models
Theme   : テンプレートの再利用
Date    : 2025/04/25
Page    : P65
"""

from langchain.prompts import load_prompt


# プロンプトのロード
loaded_prompt = load_prompt("prompt/prompt.json")
type(loaded_prompt)
vars(loaded_prompt)

# プロンプトの作成
print(loaded_prompt.format(product="iPhone"))
