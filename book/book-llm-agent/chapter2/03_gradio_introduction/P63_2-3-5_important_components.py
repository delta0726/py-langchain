"""
Title   : やさしく学ぶLLMエージェント
Chapter : 2 エージェント作成のための基礎知識
Section : 3 Gradioを用いたGUIの作成 
Theme   : 重要なコンポーネントの導入
Date    : 2025/06/25
Page    : P
"""

import gradio as gr


def text2text(text):
    text = "<<" + text + ">>"
    return text

def audio_upload(audio):
    return audio


with gr.Blocks() as demo:
    # Audio
    audio = gr.Audio(label="音声", type="filepath")
    # Checkbox
    checkbox = gr.Checkbox(label="チェックボックス")
    # File
    file = gr.File(label="ファイル", file_types=["image"])
    # Number
    number = gr.Number(label="数値")
    # Markdown
    markdown = gr.Markdown(label="Markdown", value="# タイトル\n## サブタイトル\n本文")
    # Slider
    slider = gr.Slider(
        label="スライダー", minimum=-10, maximum=10, step=0.5, interactive=True
    )
    # Textbox
    textbox = gr.Textbox(label="テキストボックス")


# 起動
demo.launch(share=False, inbrowser=True, debug=True, height=1200)
