import time
import urllib.request
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

chrome_options = Options()
chrome_options.add_experimental_option("detach", True)  # 브라우저 꺼짐 방지
chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"]) # 셀레니움 로그 무시

service = Service(ChromeDriverManager().install())  # 크롬 드라이버 최신 버전을 항상 가져옴

search_keyword="귀도반로섬"
naver_image_base_url = f"https://search.naver.com/search.naver?where=image&sm=tab_jum&query={search_keyword}"

browser = webdriver.Chrome("/Applications/Google Chrome.app", service=service, options=chrome_options)
browser.get(naver_image_base_url)
browser.implicitly_wait(5)
browser.maximize_window()

import os

img_dir_name = "naver_image_download"

if not os.path.exists(img_dir_name):
    os.mkdir(img_dir_name)

import requests

try:
    time.sleep(2)

    before_h = 0
    # 무한 스크롤 처리
    while True:
        browser.find_element(By.CSS_SELECTOR, "body").send_keys(Keys.END) # 스크롤을 맨 아래로
        time.sleep(0.5)

        after_h = browser.execute_script("return window.scrollY")

        if after_h == before_h:
            break

        before_h = after_h

    images = browser.find_elements(By.CSS_SELECTOR, "._image._listImage")

    for count, image in enumerate(images, 1):
        # 각 이미지 태그 내 실제 이미지의 주소
        image_src = image.get_attribute("src")
        print(image_src, count)
        urllib.request.urlretrieve(image_src, f"./{img_dir_name}/{count}.png")




except Exception as e:
    print("error 발생", e)

finally:
    browser.quit()