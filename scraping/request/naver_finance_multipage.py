import pyautogui
import requests
from urllib.parse import unquote
from bs4 import BeautifulSoup

# last_page = pyautogui.prompt("몇 페이지까지 가져올까요? (1페이지 = 50개)")

last_page = 50

kospi_500_data = []
kospi_data_sample = {}  # {'N': '', '종목명': '', '현재가': '', '전일비': '', '등락률': '', '액면가': '', '상장주식수': '', 'PER': '', 'ROE': '', 'PBR': '', '유보율': '', '토론실': ''}

for page_index in range(1, last_page + 1):
    url_in_page = f"https://finance.naver.com/sise/field_submit.naver?menu=market_sum&returnUrl=http://finance.naver.com/sise/sise_market_sum.naver?&page={page_index}&fieldIds=per&fieldIds=roe&fieldIds=listed_stock_cnt&fieldIds=pbr&fieldIds=reserve_ratio"

    response = requests.get(url_in_page)
    soup = BeautifulSoup(response.text, 'html.parser')

    # 헤더값 추출
    if page_index == 1:
        table_heads = soup.select("table.type_2 > thead > tr > th[scope='col']")
        for head in table_heads:
            kospi_data_sample[head.get_text()] = object()

    # 데이터 추출
    trs = soup.select("table.type_2 > tbody > tr[onmouseover='mouseOver(this)']")
    for tr in trs:
        data = kospi_data_sample.copy()

        name = tr.select_one("td:nth-child(2)").text
        per = tr.select_one("td:nth-child(7)").text
        roe = tr.select_one("td:nth-child(8)").text
        pbr = tr.select_one("td:nth-child(9)").text
        reserve_ratio = tr.select_one("td:nth-child(10)").text

        # 데이터 전처리
        if per != 'N/A' and roe != 'N/A' and pbr != 'N/A' and reserve_ratio != 'N/A':
            per = float(per.replace(',', ''))
            roe = float(roe.replace(',', ''))
            pbr = float(pbr.replace(',', ''))
            reserve_ratio = float(reserve_ratio.replace(',', ''))

            data['종목명'] = name
            data['PER'] = per
            data['ROE'] = roe
            data['PBR'] = pbr
            data['유보율'] = reserve_ratio

        kospi_500_data.append(data)  # 최종 데이터 Add
    print(f"{page_index} 페이지 가 실행 완료되었습니다.")

print(len(kospi_500_data))  # 50 개 * 50 페이지 = 2500