"""
Title   : やさしく学ぶLLMエージェント
Chapter : 2 エージェント作成のための基礎知識
Section : 2 LangChain入門
Theme   : LCELを使った簡単な翻訳アプリケーション
Date    : 2025/06/25
Page    : P46-48
"""

# ＜ポイント＞
# - PromptTemplateを使うことでf-stringの文字列より柔軟なテンプレート化ができる
# - LCELでRunnableオブジェクトにすることでinvoke()など共通メソッドが使える

from langchain_openai.chat_models import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser


# 1 テンプレート作成
TRANSLATION_PROMPT = """
以下の文章を {language} に翻訳し、翻訳結果のみを返してください。
{source_text}
"""

# チェイン定義
prompt = PromptTemplate.from_template(template=TRANSLATION_PROMPT)
llm = ChatOpenAI(model="gpt-4o-mini")
output_parser = StrOutputParser()
runnable = prompt | llm | output_parser

# 入力値の設定
language = "日本語"
source_text = """
cogito, ergo sum
"""

# 実行
response = runnable.invoke(input={"language": language, "source_text": source_text})

# 結果表示
print(response)
