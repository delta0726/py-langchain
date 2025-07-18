"""
Title   : やさしく学ぶLLMエージェント
Chapter : 2 エージェント作成のための基礎知識
Section : 1 OpenAI API 
Theme   : 
Date    : 2025/06/25
Page    : P25
"""

from openai import OpenAI
import requests

client = OpenAI()

prompt = """\
メタリックな球体
"""

response = client.images.generate(
    model="dall-e-3", prompt=prompt, n=1, size="1024x1024"
)

image_url = response.data[0].url
image = requests.get(image_url).content
with open("output1.png", "wb") as f:
    f.write(image)
    
    
response = client.images.generate(
    model="dall-e-3", prompt=prompt, n=1, size="1024x1024", response_format="b64_json"
)

image = response.data[0].b64_json

with open("output2.png", "wb") as f:
    f.write(base64.b64decode(image))
    
print(response.data[0].revised_prompt)