import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

chrome_options = Options()
chrome_options.add_experimental_option("detach", True)  # 브라우저 꺼짐 방지
chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"]) # 셀레니움 로그 무시

service = Service(ChromeDriverManager().install())  # 크롬 드라이버 최신 버전을 항상 가져옴

search_keyword = '트레이딩뷰'
youtube_base_url = f'https://www.youtube.com/results?search_query={search_keyword}'

browser = webdriver.Chrome("/Applications/Google Chrome.app", service=service, options=chrome_options)
browser.get(youtube_base_url)
browser.implicitly_wait(5)
browser.maximize_window()

try:
    time.sleep(2)

    # 7번만 스크롤 하기
    scroll_count = 7
    for _ in range(scroll_count):
        browser.find_element(By.CSS_SELECTOR, "body").send_keys(Keys.END) # 스크롤을 맨 아래로
        time.sleep(1.5)  # 스크롤 사이에 페이지 로딩 시간을 줌


    # Selenium - BeautifulSoup 연동
    html = browser.page_source
    soup = BeautifulSoup(html, "html.parser")

    infos = soup.select("div.text-wrapper")
    for info in infos:
        # 원하는 정보 꺼내오기
        # 스트리밍중일 경우 날짜가 없는 경우도 있는데, 그럴 땐 default 값 처리를 해줘야함
        title = info.select_one("a#video-title").text
        # 조회수 예시: 1천 미만: 823회 / 1천 이상: 1.1천회 / 1만 이상: 3.4만회, 15만회 /
        view_count = info.select_one("div#metadata-line > span:nth-child(2)").text
        date = info.select_one("div#metadata-line > span:nth-child(3)").text

        kor_arabia = {"없음": 0, "천": 1000, "만": 10000, "억": 100000000}
        change_view_count = view_count.replace("조회수", "").replace("회", "").strip()
        if kor_arabia.get(change_view_count[-1]):
            final_view_count = float(change_view_count.replace(change_view_count[-1], "")) * kor_arabia[change_view_count[-1]]
        else:
            final_view_count = int(change_view_count)

        print(title, final_view_count, date)


except Exception as e:
    print("error 발생", e)


finally:
    browser.quit()