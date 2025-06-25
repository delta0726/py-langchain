from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time

# Chromeオプション設定（ヘッドレスを外せばブラウザ画面が見える）
options = Options()
options.add_argument("--start-maximized")  # 最大化で起動

# ドライバ自動インストール & Chrome起動
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Googleを開く
driver.get("https://www.google.com")

# タイトルを取得して表示
print("ページタイトル:", driver.title)

# 5秒待機してから終了
time.sleep(5)
driver.quit()