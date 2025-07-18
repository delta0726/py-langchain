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

# 最大公約数を求めるツールの利用class LCM(BaseModel):
    num1: int = Field(description="整数1")
    num2: int = Field(description="整数2")


lcm_function = {
    "name": "lcm",
    "description": "最小公倍数を求める",
    "parameters": LCM.model_json_schema(),
}

tools = [
    {"type": "function", "function": gcd_function},
    {"type": "function", "function": lcm_function},
]

messages = [
    {
        "role": "user",
        "content": "50141 と 53599 の最大公約数と最小公倍数を求めてください。",
    }
]

response = client.chat.completions.create(
    model="gpt-4o-mini", messages=messages, tools=tools
)
choice = response.choices[0]
if choice.finish_reason == "tool_calls":
    for tool in choice.message.tool_calls:
        if tool.function.name == "gcd":
            gcd_args = GCD.model_validate_json(tool.function.arguments)
            print(f"最大公約数: {math.gcd(gcd_args.num1, gcd_args.num2)}")
        elif tool.function.name == "lcm":
            lcm_args = LCM.model_validate_json(tool.function.arguments)
            print(f"最小公倍数: {math.lcm(lcm_args.num1, lcm_args.num2)}")
elif choice.finish_reason == "stop":
    print("AI: ", choice.message.content)