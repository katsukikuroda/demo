import time

import chromedriver_binary
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome()

# Web サイトを開く
url = "https://www.e-typing.ne.jp/roma/check/"
driver.get(url)

# 「今すぐチェック」ボタンを押す
start_btn_1 = driver.find_element("id", "level_check_btn")
start_btn_1.click()
time.sleep(2)

# 「スタート」ボタンを押す
driver.switch_to.frame("typing_content")
start_btn_2 = driver.find_element("id", "start_btn")
start_btn_2.click()
time.sleep(1)

# 「スペースキー」を押す
body = driver.find_element("tag name", "body")
body.send_keys(Keys.SPACE)
time.sleep(5)

while True:
    # ゲームが終わると sentenceText 要素 がなくなりエラーが出るので try~except~ で例外処理する
    try:
        sentence_element = driver.find_element("id", "sentenceText")

    except:
        # エラーが出たらゲームは終了しているので while 文を抜ける
        break

    else:
        # sentence_element に text がない瞬間があるので if 文にして存在確認する
        if not sentence_element.text is None:
            for char in sentence_element.text:
                body.send_keys(char)
                time.sleep(0.03)

input('何か入力してください')

driver.quit()