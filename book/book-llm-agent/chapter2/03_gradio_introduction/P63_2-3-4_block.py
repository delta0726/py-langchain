"""
Title   : やさしく学ぶLLMエージェント
Chapter : 2 エージェント作成のための基礎知識
Section : 3 Gradioを用いたGUIの作成 
Theme   : with構文の使用
Date    : 2025/07/18
Page    : P61-62
"""

# ＜概要＞
# - Gradiohはwith構文を使うことで構造的なインターフェースを作成することができる


import gradio as gr


def text2text(text):
    text = "<<" + text + ">>"
    return text

def text2text_rich(text):
    top = "^" * len(text)
    bottom = "v" * len(text)
    text = f" {top}\n<{text}>\n {bottom}"
    return text

with gr.Blocks() as demo:
    input_text = gr.Text(label="入力")
    button1 = gr.Button(value="Normal")
    button2 = gr.Button(value="Rich")
    output_text = gr.Text(label="出力")

    button1.click(inputs=input_text, outputs=output_text, fn=text2text)
    button2.click(inputs=input_text, outputs=output_text, fn=text2text_rich)


# 起動
demo.launch(share=False, inbrowser=True, debug=True)