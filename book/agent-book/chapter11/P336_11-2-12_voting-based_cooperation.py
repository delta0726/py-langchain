"""
Title   : LangChainとLangGraphによるRAG・AIエージェント実践入門
Chapter : 11 エージェントデザインパターン
Section : 2 18のエージェントデザインパターン
Theme   : 12 投票ベースの協調
Date    : 2025/06/30
Page    : P336-338
"""


# ＜概要＞
# - 複数のAIエージェントが独立して判断や提案を行い、その結果を投票によって集約して最終的な意思決定を行うパターン
# - 複雑な問題に対して多様な視点からのアプローチを可能とし、個々のAIエージェントによる判断や意思決定の誤りを軽減する
# - 意見が分かれた場合に収斂するように調整メカニズムが必要となる場合がある


# ＜カテゴリ＞
# - エージェント間の協調


# ＜関連パターン＞
# - 7. セルフ・リフレクション
# - 8. クロス・リフレクション
# - 9. ヒューマン・リフレクション


# ＜プロセス＞
# - 1. 問題や課題を複数のAIエージェントに提示する
# - 2. 各AIエージェントが独立して回答や提案を生成する
# - 3. 生成された回答や提案を収集する
# - 4. 事前に定義された投票方式に基づいて結果を集計する
# - 5. 集計結果に基づいて最終的な判断や決定を行う
# - 6. 必要に応じて、最終判断の根拠や各エージェントの意見も含めて結果を提示する
