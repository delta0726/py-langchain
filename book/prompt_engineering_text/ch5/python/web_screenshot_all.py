import os
import time

from pyhere import here


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service as ChromeService
from PIL import Image

cd = here()
os.chdir(cd)


# Chromeドライバーのパスを指定してセッションを開始
chrome_service = ChromeService()
driver = webdriver.Chrome(service=chrome_service)

# 1. 「https://kujirahand.com」のページを表示
driver.get("https://kujirahand.com")

# 2. JavaScriptでページサイズを求めてウィンドウサイズを変更
page_height = driver.execute_script(
    "return Math.max( document.body.scrollHeight, document.body.offsetHeight, document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight );"
)
driver.set_window_size(800, page_height)

# 3. ページをスクロールしながらキャプチャを撮って「test_part_{番号}」に保存
screenshot_number = 1
scroll_height = driver.execute_script("return window.innerHeight;")
while True:
    driver.save_screenshot(f"ch5/png/test_part_{screenshot_number}.png")
    screenshot_number += 1
    driver.execute_script(f"window.scrollTo(0, {scroll_height});")
    scroll_height += driver.execute_script("return window.innerHeight;")
    time.sleep(2)  # 2秒待つ（必要に応じて調整）

    if scroll_height >= page_height:
        break

# 4. 保存した画像を上下に結合ページ全体を「test.png」に保存


images = [Image.open(f"ch5/png/test_part_{i}.png") for i in range(1, screenshot_number)]
total_height = sum(img.height for img in images)
combined_image = Image.new("RGB", (images[0].width, total_height))

y_offset = 0
for img in images:
    combined_image.paste(img, (0, y_offset))
    y_offset += img.height

combined_image.save("ch5/png/test.png")

# ブラウザを閉じる
driver.quit()
