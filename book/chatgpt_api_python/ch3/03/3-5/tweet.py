"""
Title   : Chatgpt API & Python
Section : 3 短文の作成とSNSへの投稿を自動化しよう
Theme   : ツイートを作成して投稿する
Date    : 2025/04/30
Page    : P108
"""

import gpt_api_1
import gpt_api_2
import twitter_api

"""
実行すると以下で反映が確認できる。
確認後は削除
https://x.com/explore/tabs/for-you
"""

# ChatGPTからツイート内容を取得
tweet_1 = gpt_api_1.make_tweet()
tweet_2 = gpt_api_2.make_tweet()

# Twitterにツイートを投稿
twitter_api.post(tweet=tweet_1)
twitter_api.post(tweet=tweet_2)
