"""
Title   : Chatgpt API & Python
Section : 3 短文の作成とSNSへの投稿を自動化しよう
Theme   : Xにポストする関数
Date    : 2025/04/30
Page    : P108
"""

import tweepy
import os

# Twitter APIキーを環境変数から取得
consumerKey = os.environ["TWITTER_CONSUMER_KEY"]
consumerSecret = os.environ["TWITTER_CONSUMER_SECRET"]
accessToken = os.environ["TWITTER_ACCESS_TOKEN"]
accessTokenSecret = os.environ["TWITTER_ACCESS_TOKEN_SECRET"]
bearerToken = os.environ["TWITTER_BEARER_TOKEN"]

# ポストを投稿する関数を定義
def post(tweet):
    #tweepy クライアントを作成
    client = tweepy.Client(
        bearer_token=bearerToken,
        consumer_key=consumerKey,
        consumer_secret=consumerSecret,
        access_token=accessToken,
        access_token_secret=accessTokenSecret,
    )

    # ポストを投稿
    client.create_tweet(text=tweet)