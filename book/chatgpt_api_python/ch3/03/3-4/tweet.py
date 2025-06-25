"""
Title   : Chatgpt API & Python
Section : 3 短文の作成とSNSへの投稿を自動化しよう
Theme   : ツイートを作成して投稿する
Date    : 2025/04/30
Page    : P108
"""

"""
実行すると以下で反映が確認できる。
確認後は削除
https://x.com/explore/tabs/for-you
"""

import gpt_api
import twitter_api


# ツイート内容を作成
# --- ChatGPTで例文を元に生成している
tweet = gpt_api.make_tweet()

# Xにツイートを投稿
twitter_api.post(tweet=tweet)
