"""
Title   : LangChainとLangGraphによるRAG・AIエージェント実践入門
Chapter : 4 LangChainの基礎
Section : 4 Output parser
Theme   : strOuptputParser
Date    : 2025/05/16
Page    : P83
"""

# ＜ポイント＞
# - strOutputParserはLLMの出力をテキストに変換するために使用する
# - ouput.contentのように指定しなくてもテキストを取得できるのがメリット
# - LCELの構成要素としてチェーン処理に活用する（出力方式を確定させることでコードの簡素化）

from langchain_core.messages import AIMessage
from langchain_core.output_parsers import StrOutputParser


# 出力パーサーの定義
output_parser = StrOutputParser()

# AIメッセージの設定
ai_message = AIMessage(content="こんにちは。私はAIアシスタントです。")

# テキストの取得
# --- LLMへの問い合わせはしていない
ai_message = output_parser.invoke(input=ai_message)

# 結果確認
print(type(ai_message))
print(ai_message)

