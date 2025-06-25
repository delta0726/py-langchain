import os

from pyhere import here
from selenium import webdriver

cd = here()
os.chdir(cd)


# ドライバの初期化
driver = webdriver.Chrome()

# ブラウザのウィンドウサイズを最大に設定
driver.maximize_window()

# 1つ目のページを開いて保存
driver.get("https://kujirahand.com")
driver.save_screenshot("ch5/png/web1.png")

# 2つ目のページを開いて保存
driver.get("https://nadesi.com")
driver.save_screenshot("ch5/png/web2.png")

# ブラウザを閉じる
driver.quit()
