import time
from selenium import webdriver

# WebDriverの初期化
driver = webdriver.Chrome()

# 1. ログインページにアクセス
login_url = "https://uta.pw/sakusibbs/users.php?action=login"
driver.get(login_url)

# ログイン情報の入力
username = driver.find_element("id", "user")
password = driver.find_element("id", "pass")

username.send_keys("book-prompt")
password.send_keys("1LUSwKxrsc6WKk1y")

# ログインボタンのクリック
login_button = driver.find_element("css selector", "#loginForm input[type=submit]")
login_button.click()

# 2. 作品一覧ページに移動
work_list_url = "https://uta.pw/sakusibbs/users.php?user_id=1"
driver.get(work_list_url)

# 3. 作品一覧リンクを取得
url_list = []
ul_element = driver.find_element("css selector", "#mmlist")
li_elements = ul_element.find_elements("tag name", "li")

for li in li_elements:
    a_element = li.find_element("tag name", "a")
    url_list.append(a_element.get_attribute("href"))

# 4. 作品ページに移動し、お気に入りボタンをクリック
for url in url_list:
    driver.get(url)
    time.sleep(1)  # サーバー負荷を抑えるための待機
    fav_button = driver.find_elements("css selector", "#fav_add_btn")
    
    if fav_button:
        fav_button[0].click()
        time.sleep(1)  # サーバー負荷を抑えるための待機

# WebDriverを終了
driver.quit()
