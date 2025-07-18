"""
Title   : LangChainとLangGraphによるRAG・AIエージェント実践入門
Chapter : 11 エージェントデザインパターン
Section : 2 18のエージェントデザインパターン
Theme   : 11 インクリメンタル・モデルクエリ
Date    : 2025/06/30
Page    : P332-336
"""


# ＜概要＞
# - プラン生成プロセスの各ステップでLLMにアクセスして段階的に推論を進めるパターン
# - ワンショット・モデルクエリで期待どおりの品質の回答が得れそうにない場合に検討する
# - リフレクションからのフィードバックを反映してプロンプトを修正していく


# ＜カテゴリ＞
# - 目標設定と計画生成


# ＜関連パターン＞
# - 7. セルフ・リフレクション
# - 8. クロス・リフレクション
# - 9. ヒューマン・リフレクション
# - 10. ワンショット・モデルクエリ


# ＜プロセス＞
# - 1. ユーザーからの初期の質問や指示を受け取る
# - 2. 初期クエリを生成しLLMに送信する
# - 3. LLMからの応答を分析して、追加情報が必要な点/改善点などをLLMや人間のフィードバックから特定する
# - 4. 特定された点に基づいてフォローアップのクエリを生成する
# - 5. フォローアップのクエリをLLMに送信して、追加情報/改善点を反映した回答を得る
# - 6. 必要に応じてステップ3-5を繰り返す
# - 7. 得られた情報を統合し、最終的な回答を生成する
# - 8. 統合された回答をユーザーに提示する
