from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# 크롬 드라이버 자동 업데이트
from webdriver_manager.chrome import ChromeDriverManager

import time
import pyautogui
import pyperclip


chrome_options = Options()
chrome_options.add_experimental_option("detach", True)  # 브라우저 꺼짐 방지
chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"]) # 셀레니움 로그 무시


service = Service(executable_path=ChromeDriverManager().install())  # 크롬 드라이버 최신 버전을 항상 가져옴
driver = webdriver.Chrome(service=service, options=chrome_options)

# 웹페이지 주소 이동
# 웹 페이지가 로딩 될 때 까지 5초는 기다림
# driver.maximize_window()  # 화면 최대화
driver.implicitly_wait(5)
driver.get("https://nid.naver.com/nidlogin.login?mode=form&url=https%3A%2F%2Fwww.naver.com")
time.sleep(2)


# 아이디 입력창
id = driver.find_element(By.CSS_SELECTOR, "#id")
pyperclip.copy("asdjhgf92")
id.click()
with pyautogui.hold(['command']):   # https://github.com/asweigart/pyautogui/issues/687
    time.sleep(1)
    pyautogui.press('v')

# 비밀번호 입력창
pw = driver.find_element(By.CSS_SELECTOR, "#pw")
pyperclip.copy("WLGUSWNS921931")
pw.click()
with pyautogui.hold(['command']):
    time.sleep(1)
    pyautogui.press('v')

time.sleep(1)

login_btn = driver.find_element(By.XPATH, '//*[@id="log.login"]')  # 비밀번호 입력창
login_btn.click()

time.sleep(2)
driver.close() # 브라우저 닫기