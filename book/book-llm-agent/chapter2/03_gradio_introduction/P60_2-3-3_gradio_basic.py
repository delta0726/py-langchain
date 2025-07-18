"""
Title   : やさしく学ぶLLMエージェント
Chapter : 2 エージェント作成のための基礎知識
Section : 3 Gradioを用いたGUIの作成
Theme   : Gradioの基礎
Date    : 2025/07/18
Page    : P60-62
"""

# ＜概要＞
# - GradioとはAIアプリケーションのインターフェースを簡単に作るライブラリ
# - with構文は使わない最も単純なチュートリアルを示す

import gradio as gr


# 関数定義
def text2text(text):
    text = "<<" + text + ">>"
    return text


# インターフェース定義
input_text = gr.Text(label="入力")
output_text = gr.Text(label="出力")
demo = gr.Interface(inputs=input_text, outputs=output_text, fn=text2text)

# 起動
demo.launch(share=False, inbrowser=True, debug=True)
