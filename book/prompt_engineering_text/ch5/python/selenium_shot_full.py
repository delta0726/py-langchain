import os

from pyhere import here
from selenium import webdriver

cd = here()
os.chdir(cd)

# ヘッドレス起動
options = webdriver.ChromeOptions()
options.add_argument("--headless")
driver = webdriver.Chrome(options=options)


# スクリーンショットを撮影する関数
def fullpage_screenshot(driver, url, file):
    # 指定したURLにアクセス
    driver.get(url)

    # ページ全体の高さを取得
    page_height = driver.execute_script(
        "return Math.max( document.body.scrollHeight, document.body.offsetHeight, document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight );"
    )

    # ページの高さをウィンドウの高さに設定
    driver.set_window_size(
        driver.execute_script("return window.innerWidth"), page_height
    )

    # スクリーンショットを保存
    driver.save_screenshot(file)


# 撮影したいWebサイトのURLを指定
urls = ["https://nadesi.com", "https://kujirahand.com"]

# 各Webサイトのスクリーンショットを撮影
for idx, url in enumerate(urls):
    filename = f"screenshot_{idx}.png"
    fullpage_screenshot(driver, url, filename)
    print(f"スクリーンショットを撮影しました: {filename}")

# ブラウザを終了
driver.quit()
