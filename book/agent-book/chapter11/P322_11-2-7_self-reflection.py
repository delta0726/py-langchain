"""
Title   : LangChainとLangGraphによるRAG・AIエージェント実践入門
Chapter : 11 エージェントデザインパターン
Section : 2 18のエージェントデザインパターン
Theme   : 7 セルフ・リフレクション
Date    : 2025/06/30
Page    : P322-324
"""


# ＜概要＞
# - AIエージェントが自身の出力や推論プロセスを評価して必要に応じて修正するパターン
# - 評価結果はDBに保存しておくことで、次回に類似したタスクを実行する際の参考にすることもある
# - 人間のPDCAプロセスからインスピレーションを受けたプロセス


# ＜カテゴリ＞
# - 推論の確実性向上


# ＜関連パターン＞
# - 5. シングルパス・プランジェネレータ
# - 6. マルチパス・プランジェネレータ
# - 8. クロス・リフレクション
# - 9. ヒューマン・リフレクション


# ＜プロセス＞
# - 1. AIエージェントが初期の回答や判断を生成する
# - 2. 生成された結果に対して事前に定義した評価基準やDB保存された教訓に基づいてフィードバックを作成
# - 3. AIエージェントがフィードバックを分析して問題点や改善点を特定する
# - 4. 特定された問題点や改善点をメモリに保存する
# - 5. 生成された回答や判断を特定された問題点に基づいて修正する
# - 6. 必要に応じてこのプロセスを複数回において繰り返す
# - 7. 改善された結果をユーザーに提示する
