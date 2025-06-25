"""
Title   : Langchain完全入門
Section : 4 Memory - 過去の対話を短期/長期で記憶する
Theme   : 過去の会話に対して追加質問する
Date    : 2025/04/27
Page    : P151
"""

from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, AIMessage


# LLMの定義
chat = ChatOpenAI(model="gpt-4o-mini")

# AIの過去の回答
content_ai = """
茶碗蒸しを作るために必要な食材は以下の通りです： 
1. 卵：茶碗蒸しの主要な材料であり、卵を使って滑らかなカスタード状の蒸し液を作ります。
2. 出汁：茶碗蒸しには出汁が必要です。一般的には鰹節や昆布から作った出汁が使われます。
3. 醤油：茶碗蒸しに風味を与えるため、醤油を使います。一般的には薄口醤油が使用されます。
4. 塩：蒸し液に塩味を加えるために使用します。
5. 水：茶碗蒸しの蒸し液を作るための水が必要です。
6. 具材：茶碗蒸しには様々な具材を追加することができます。一般的な具材には鶏肉、海鮮、野菜などがあります。
これらの材料を使用して、茶碗蒸しを作ることができます。具体的なレシピに従って手順を進めると良いでしょう。
"""

# 連続的な会話
# --- AIの回答を再現した上で次の質問を行う
result = chat(
    [
        HumanMessage(content="茶碗蒸しを作るのに必要な食材を教えて"),
        AIMessage(content=content_ai),
        HumanMessage(content="前の回答を英語に翻訳して"),
    ]
)

# 結果確認
print(result.content)
