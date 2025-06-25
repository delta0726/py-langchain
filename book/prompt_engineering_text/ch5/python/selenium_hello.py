from selenium import webdriver


from selenium.webdriver.common.keys import Keys
import time

# WebDriverを初期化
driver = webdriver.Chrome()

# Googleのトップページを開く
driver.get("https://www.google.com")

# 検索ボックスを探し、キーワードを入力
search_box = driver.find_element("name", "q")
search_box.send_keys("自動操作テスト")

# Enterキーを押して検索実行
search_box.send_keys(Keys.RETURN)
# ページが読み込まれるのを待つ（最大5秒待つ）

driver.implicitly_wait(5)

# 5行待機
time.sleep(5)


# ブラウザを閉じる
driver.quit
