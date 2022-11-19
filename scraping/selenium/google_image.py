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

search_keyword="강아지"
google_image_base_url = f"https://www.google.com/search?q={search_keyword}&hl=en&sxsrf=ALiCzsZ-DJpwkUXZPaFlK8zCZEWq3fw_CQ:1668856883501&source=lnms&tbm=isch&sa=X&ved=2ahUKEwiC9-KtkLr7AhUikVYBHbl4D94Q_AUoAXoECAEQAw&biw=1440&bih=1383&dpr=1"

browser = webdriver.Chrome("/Applications/Google Chrome.app", service=service, options=chrome_options)
browser.get(google_image_base_url)
browser.implicitly_wait(5)
browser.maximize_window()

import os

img_dir_name = "google_image_download"

if not os.path.exists(img_dir_name):
    os.mkdir(img_dir_name)

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

    # 썸네일 이미지 태그 추출
    images = browser.find_elements(By.CSS_SELECTOR, "img.rg_i.Q4LuWd")

    for count, image in enumerate(images, 1):
        # 이미지를 클릭해서 큰 이미지를 찾기
        # element click intercepted 오류가 나옴
        # JS 로 이 DOM 을 직접 클릭을 해주도록 변경
        # image.click()
        browser.execute_script("arguments[0].click()", image)
        time.sleep(1)

        big_images = browser.find_elements(By.CSS_SELECTOR, "img.n3VNCb")
        for big_image in big_images:
            main_image_src = big_image.get_attribute("src")
            if main_image_src.startswith("http"):  # base64 는 걸러내고 받음

                # 여기서 403 Forbidden 을 해결하기 위한 User-Agent Header 추가
                # Idea: 실제로 Image 가 있는 리스트만 걸러서 어디 파일같은데 써놓고(or 메모리)
                # 그걸 다른 프로세스에서 받아가서 urllib으로 이미지 다운로드 받는게 동작 속도 면에서는 더 빠르지 않을까?
                opener = urllib.request.build_opener()
                opener.addheaders = [{'User-Agent', 'Mozila/5.0'}]
                urllib.request.install_opener(opener)
                urllib.request.urlretrieve(main_image_src, f"./{img_dir_name}/{count}.png")


except Exception as e:
    print("error 발생", e)

finally:
    browser.quit()