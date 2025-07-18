"""
Title   : やさしく学ぶLLMエージェント
Chapter : 2 エージェント作成のための基礎知識
Section : 1 OpenAI API 
Theme   : 
Date    : 2025/06/25
Page    : P25
"""

from openai import OpenAI

client = OpenAI()

# 最大公約数を求めるツールの利用

gcd_function = {
    "name": "gcd",
    "description": "最大公約数を求める",
    "parameters": {
        "type": "object",
        "properties": {
            "num1": {"type": "number", "description": "整数1"},
            "num2": {"type": "number", "description": "整数2"},
        },
        "required": ["num1", "num2"],
    },
}
tools = [{"type": "function", "function": gcd_function}]

messages = [
    {"role": "user", "content": "50141 と 53599 の最大公約数を求めてください。"}
]

response = client.chat.completions.create(
    model="gpt-4o-mini", messages=messages, tools=tools
)
print(response.choices[0].message.content)  # None
print(response.choices[0].finish_reason)  # tool_calls
print(response.choices[0].message.tool_calls)  # [ChatCompletionMessageToolCall(...)]


# 関数情報を抽出

import json

function_info = response.choices[0].message.tool_calls[0].function
name = function_info.name
args = json.loads(function_info.arguments)

# 最大公約数の計算

import math

print(math.gcd(args["num1"], args["num2"]))


# Pydantic を用いた関数の定義

from pydantic import BaseModel, Field


class GCD(BaseModel):
    num1: int = Field(description="整数1")
    num2: int = Field(description="整数2")


gcd_function = {
    "name": "gcd",
    "description": "最大公約数を求める",
    "parameters": GCD.model_json_schema(),
}


tools = [{"type": "function", "function": gcd_function}]

messages = [
    {"role": "user", "content": "50141 と 53599 の最大公約数を求めてください。"}
]

response = client.chat.completions.create(
    model="gpt-4o-mini", messages=messages, tools=tools
)


# Pydantic を用いた引数の取得

parsed_result = GCD.model_validate_json(
    response.choices[0].message.tool_calls[0].function.arguments
)
print(parsed_result)


