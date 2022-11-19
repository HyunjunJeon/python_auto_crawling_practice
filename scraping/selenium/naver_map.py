from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

import time
import pyautogui
import pyperclip
import openpyxl

workbook = openpyxl.Workbook()
worksheet = workbook.create_sheet()
worksheet.append(["순위", "이름", "별점", "방문자 리뷰", "블로그 리뷰"])

chrome_options = Options()
chrome_options.add_experimental_option("detach", True)  # 브라우저 꺼짐 방지
chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"]) # 셀레니움 로그 무시

service = Service(ChromeDriverManager().install())  # 크롬 드라이버 최신 버전을 항상 가져옴

naver_map_base_url = 'https://map.naver.com/v5/'

browser = webdriver.Chrome("/Applications/Google Chrome.app", service=service, options=chrome_options)
browser.get(naver_map_base_url)
browser.implicitly_wait(5)
browser.maximize_window()

# selenium browser 를 컨트롤 하는 시점부터 try-catch-finally 구문을 타게끔
try:
    # 검색창 입력
    search = browser.find_element(By.CSS_SELECTOR, "input.input_search")
    pyperclip.copy("신당역 맛집")
    time.sleep(0.5)
    search.click()
    with pyautogui.hold(['command']):
        time.sleep(1)
        pyautogui.press('v')

    time.sleep(1)
    search.send_keys(Keys.ENTER)
    time.sleep(1.5)


    # iframe 안으로 들어가기
    browser.switch_to.frame("searchIframe")

    # 다 첫번째 것만 찾아가기 때문에.. 난수로 지정되는 것보다는 났지 않을까? (주기적으로 class 난수값이 바뀌기 때문에, 디자인 틀이 바뀌지 않는다면 순서는 잘 안바뀌는거 아닐까)
    # ** 아니면 난수(class 값)를 찾는 프로그램을 하나 추가로 둬야할 듯 ** (난수가 바뀌어도 프로그램이 대응할 수 있는 유일한 방법)

    # iframe 내 아무 동작도 하지 않는 DOM 하나 클릭 (무한스크롤 동작시키기 위해서)
    browser.find_element(By.CSS_SELECTOR, "#_pcmap_list_scroll_container").click()

    # 로딩된 데이터 개수 확인
    lis = browser.find_elements(By.CSS_SELECTOR, "li.UEzoS.rTjJo")
    before_len = len(lis)

    while True:
        # 스크롤을 맨 아래로 내림
        browser.find_element(By.CSS_SELECTOR, "body").send_keys(Keys.END)  # iframe 내에 아무런 태그나 선택한 것: body

        time.sleep(1.5)

        # 스크롤 후 로딩된 데이터 개수 확인
        lis = browser.find_elements(By.CSS_SELECTOR, "li.UEzoS.rTjJo")
        after_len = len(lis)

        if before_len == after_len:
            break

        before_len = after_len

    rank = 1
    for li in lis:
        # 광고가 있으면 li 바로 밑에 아래의 a 태그가 존재하기 때문에
        ads = li.find_elements(By.CSS_SELECTOR, "a.gU6bV")

        # 별점이 있는 것만 정보를 추가 수집하기 위해서
        ems = li.find_elements(By.CSS_SELECTOR, "span.h69bs.a2RFq > em")

        if len(ads) == 0:
            if len(ems) > 0:
                # 가게명
                store_name = li.find_element(By.CSS_SELECTOR, "span.place_bluelink.TYaxT").text
                # 별점
                star_point = ems[0].text

                # 영업 시간
                store_opening_hour = li.find_elements(By.CSS_SELECTOR, "span.h69bs.KvAhC")

                if len(store_opening_hour) > 0:
                    # 방문자 리뷰 수
                    visitor_review = li.find_element(By.CSS_SELECTOR, "span.h69bs:nth-child(2)").text
                    # 블로그 리뷰 수
                    blog_review = li.find_element(By.CSS_SELECTOR, "span.h69bs:nth-child(3)").text
                else:
                    # 방문자 리뷰 수
                    visitor_review = li.find_element(By.CSS_SELECTOR, "span.h69bs:nth-child(2)").text
                    # 블로그 리뷰 수
                    blog_review = li.find_element(By.CSS_SELECTOR, "span.h69bs:nth-child(3)").text

                print(rank, store_name, star_point, store_opening_hour, visitor_review, blog_review)

                # 데이터 저장을 위한 처리
                visitor_review = visitor_review.replace("방문자리뷰 ", "").replace(",", "")
                blog_review = blog_review.replace("블로그리뷰 ", "").replace(",", "")

                worksheet.append([rank, store_name, float(star_point), int(visitor_review), int(blog_review)])
                rank += 1

        # iframe 밖으로 나오기 -> 추가로 서치할 부분이 있을 때에만...
        # browser.switch_to.default_content()

        workbook.save(f"naver_map_crawling.xlsx")
except Exception as e:
    print("error 발생", e)

finally:
    browser.quit() # 브라우저 종료




