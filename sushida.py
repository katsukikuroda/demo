"""
教材「タイピング自動化」で使用する、寿司打自動化（OCR なし）のコードです。
"""
import time

import chromedriver_binary
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains

driver = webdriver.Chrome()

# ウィンドウサイズを固定
# +123 としているのは、「自動テストソフトウェアによって制御されています。」という部分を考慮している
window = (730, 630+123)
driver.set_window_size(*window)

url = "https://sushida.net/play.html"
driver.get(url)

# # 寿司打のゲーム画面をずらすために書く
target_xpath = '//*[@id="game"]/div'
webgl_element = driver.find_element_by_xpath(target_xpath)
actions = ActionChains(driver)
actions.move_to_element(webgl_element)
actions.perform()

# 画面が表示されるまで待つ
time.sleep(8)

# スタートボタンの座標
center_x = 200
center_y = 256

# スタートボタンをクリックする
actions = ActionChains(driver)
actions.move_to_element_with_offset(webgl_element, center_x, center_y)
actions.click()
actions.perform()

# ボタンが表示されるまで待つ
time.sleep(2)

# お勧めコースをクリックする
actions = ActionChains(driver)
actions.move_to_element_with_offset(webgl_element, center_x, center_y).click().perform()

time.sleep(1)

# <body> に向かってキーを入力させる
target_xpath = '/html/body'
element = driver.find_element_by_xpath(target_xpath)
element.send_keys(" ")

start = time.time()

while time.time() - start < 90.0:
# 文字をテキトーに入力
    element.send_keys("abcdefghijklmnopqrstuvwxyz-!?.,")

input("何か入力してください")

# ドライバーを閉じる
driver.quit()