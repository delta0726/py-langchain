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

    # ツイート例
    tweet1 = """
    例文1：仕事でPythonを使うことになりそうだから、現在勉強中！
    プログラミングとか難しくてよくわからないよ...
    """
    
    tweet2 = """
    例文2：最近ChatGPTについていろいろ調べてるんだけど、
    あれってなんでも質問に答えてくれてすごいよね！
    とりあえずPythonを使って、簡単な会話をするプログラムを作ってみるつもり。
    うまくできるかな？
    """

    # 指示文に例文を追加
    content = request + tweet1 + tweet2

    # ChatGPTにリクエストを送信
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": content},
        ],
    )

    # 生成されたツイートを返す
    return response.choices[0].message.content
