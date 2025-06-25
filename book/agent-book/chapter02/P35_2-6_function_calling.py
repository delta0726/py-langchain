"""
Title   : LangChainとLangGraphによるRAG・AIエージェント実践入門
Chapter : 2 OpenAIのチャットAPIの基礎
Section : 
Theme   : Function Calling
Date    : 2025/05/06
Page    : P34-41
"""

# ＜ポイント＞
# - Function callingは2023年6月に追加された機能
# - 利用可能な関数をLLMに伝えておいてLLMに｢関数を使いたい｣という判断をさせる機能
# - LLMが関数を実行するわけでなく、LLMは｢関数を使いたい｣という応答を返すだけ

# ＜使いどころ＞
# - LLMをアプリケーションに組み込んで活用するのはJSONで結果取得することから始まる
# - JSONで受け取った結果をもとに、プログラム内の関数を条件分岐させたり引数として利用したりする
# - Function Callingはその処理を一連の手続き化したものと言える
# - あくまでシングルステップであり、エージェントのようなマルチステップには対応していない

# インポート
# --- toolsとget_current_weatherはコードが長いので別ファイルにした
import json
from openai import OpenAI
from tools.tools_config import tools
from func.get_current_weather import get_current_weather


# LLMの定義
client = OpenAI()

# メッセージの定義
messages = [
    {"role": "user", "content": "東京の天気はどうですか？"},
]

# 問い合わせ(1回目)
# --- toolsを与える
response = client.chat.completions.create(
    model="gpt-4o",
    messages=messages,
    tools=tools,
)

# 結果確認
# --- "content"がnull となっている（まだ問い合わせしていないので当然）
# --- tool_callsに"get_current_weather"をこんな引数で実行したいと言っている
# --- 名前空間にget_current_weather()があるためAIは関数を探してきた
print(response.to_json(indent=2))

# メッセージを修正
# --- AIのソリューションをメッセージに追加
response_message = response.choices[0].message
messages.append(response_message.to_dict())

# 関数リストの作成
available_functions = {
    "get_current_weather": get_current_weather,
}

# 関数実行
# --- 使いたい関数は複数あるかもしれないのでループ
tool_call = response_message.tool_calls[0]
for tool_call in response_message.tool_calls:
    function_name = tool_call.function.name
    function_to_call = available_functions[function_name]
    function_args = json.loads(tool_call.function.arguments)
    function_response = function_to_call(
        location=function_args.get("location"),
        unit=function_args.get("unit"),
    )
    print(function_response)

    # 関数の実行結果を会話履歴としてmessagesに追加
    messages.append(
        {
            "tool_call_id": tool_call.id,
            "role": "tool",
            "name": function_name,
            "content": function_response,
        }
    )


print(json.dumps(messages, ensure_ascii=False, indent=2))


# 問い合わせ(2回目)
second_response = client.chat.completions.create(
    model="gpt-4o",
    messages=messages,
    tools=tools,
)


# 結果確認
print(second_response.to_json(indent=2))
