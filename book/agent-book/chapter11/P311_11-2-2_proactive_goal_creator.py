"""
Title   : LangChainとLangGraphによるRAG・AIエージェント実践入門
Chapter : 11 エージェントデザインパターン
Section : 2 18のエージェントデザインパターン
Theme   : 2 プロアクティブ・クリエイター
Date    : 2025/06/30
Page    : P311-313
"""


# ＜概要＞
# - パッシブゴールクリエイターを拡張したユーザーの入力から具体的な目標を抽出するためのパターン
# - AIエージェントが効果的にユーザーをサポートするには、明示的な質問の対応に加えて、状況に応じた先回り対応も必要となる
# - ユーザーが言語化できないこと/気づいていないことを目標抽出に加える
# - 過度に積極的な目標設定はユーザーの意図との乖離を生み出すため注意


# ＜カテゴリ＞
# - 目標設定と計画生成


# ＜関連パターン＞
# - 1. パッシブ・ゴールクリエイター


# ＜プロセス＞
# - 1. ユーザーの入力や明示的な要求を受け取る
# - 2. ユーザーの過去の行動履歴/現在の状況/外部情報を収集する
# - 3. 収集した情報を分析し、ユーザーが明示していない潜在的なニーズを特定する
# - 4. 特定された要素をもとに、追加目標や考慮次項を生成する
# - 5. 生成された追加目標をユーザーの明示的な要求と統合する
# - 6. 統合された目標セットをAIエージェントの次の処理ステップに渡す
