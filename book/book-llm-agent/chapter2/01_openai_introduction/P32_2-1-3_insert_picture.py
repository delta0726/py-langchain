"""
Title   : やさしく学ぶLLMエージェント
Chapter : 2 エージェント作成のための基礎知識
Section : 1 OpenAI API 
Theme   : 
Date    : 2025/06/25
Page    : P25
"""


import base64
from pathlib import Path
from typing import Any

from openai import OpenAI

client = OpenAI()


def image2content(image_path: Path) -> dict[str, Any]:
    # base64 エンコード
    with image_path.open("rb") as f:
        image_base64 = base64.b64encode(f.read()).decode("utf-8")

    # content の作成
    content = {
        "type": "image_url",
        "image_url": {"url": f"data:image/png;base64,{image_base64}", "detail": "low"},
    }
    return content


prompt = "これは何の画像ですか?"
image_path = Path("./sample_image1.png")
contents = [{"type": "text", "text": prompt}, image2content(image_path)]

response = client.chat.completions.create(
    model="gpt-4o-mini",
    temperature=0.0,
    messages=[{"role": "user", "content": contents}],
)

print(response.choices[0].message.content)


image_path2 = Path("./sample_image2.png")

prompt = "2枚の画像の違いを教えてください。"
contents = [
    {"type": "text", "text": prompt},
    image2content(image_path),
    image2content(image_path2),
]
response = client.chat.completions.create(
    model="gpt-4o-mini",
    temperature=0.0,
    messages=[{"role": "user", "content": contents}],
)

print(response.choices[0].message.content)