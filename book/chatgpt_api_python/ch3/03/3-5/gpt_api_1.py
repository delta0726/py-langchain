"""
Title   : Chatgpt API & Python
Section : 3 短文の作成とSNSへの投稿を自動化しよう
Theme   : ツイート用の文章生成のプロンプトを作成
Date    : 2025/04/30
Page    : P106
"""

from openai import OpenAI


# LLMの定義
client = OpenAI()


# ChatGPTにリクエストを送信する関数を定義
def make_tweet():
    # ChatGPTへの指示文
    request = """
    私はIT系企業の新入社員（入社1年目）です。
    私に代わって140字以内のTwitter投稿を作成してください。
    以下の例文を参考にしてください。
    """

    # ツイート例-1
    tweet1 = """
    例文1：仕事でPythonを使うことになりそうだから、現在勉強中！
    プログラミングとか難しくてよくわからないよ...
    """

    # ツイート例-2
    tweet2 = """
    例文2：最近ChatGPTについていろいろ調べてるんだけど、
    あれってなんでも質問に答えてくれてすごいよね！
    とりあえずPythonを使って、簡単な会話をするプログラムを作ってみるつもり。
    うまくできるかな？
    """

    # 文章を連結して一つの命令文にする
    content = request + tweet1 + tweet2

    # 問い合わせ
    # --- temperatureを0にして創造性を抑制
    # --- 例文と同じようなニュアンスとなる（完全に一致するわけではない）
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0,
        messages=[
            {"role": "user", "content": content},
        ],
    )

    # 投稿文の内容を返却
    return response.choices[0].message.content
