from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Chrome WebDriverを初期化
driver = webdriver.Chrome()

# ログインページに移動
login_url = "https://uta.pw/sakusibbs/users.php?action=login"
driver.get(login_url)

# ログイン情報を入力して送信
user_input = driver.find_element(By.CSS_SELECTOR, "#user")
pass_input = driver.find_element(By.CSS_SELECTOR, "#pass")
login_button = driver.find_element(By.CSS_SELECTOR, "#loginForm input[type=submit]")

user_input.send_keys("book-prompt")
pass_input.send_keys("1LUSwKxrsc6WKk1y")
login_button.click()

# マイページに移動
mypage_url = "https://uta.pw/sakusibbs/users.php?user_id=2045"
driver.get(mypage_url)

# リンクをクリック
download_link = driver.find_element(By.LINK_TEXT, "一覧をCSVでダウンロード")
download_link.click()

# ブラウザを閉じる
time.sleep(3)
driver.quit()
