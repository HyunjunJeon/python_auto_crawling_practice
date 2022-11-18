import requests
from urllib.parse import unquote
from bs4 import BeautifulSoup

decoded_url = unquote("https://finance.naver.com/sise/field_submit.naver?menu=market_sum&returnUrl=http%3A%2F%2Ffinance.naver.com%2Fsise%2Fsise_market_sum.naver&fieldIds=per&fieldIds=roe&fieldIds=listed_stock_cnt&fieldIds=pbr&fieldIds=reserve_ratio")

print(decoded_url)

response = requests.get(decoded_url)
soup = BeautifulSoup(response.text, 'html.parser')

kospi_500_data = []
kospi_data_sample = {}  # {'N': '', '종목명': '', '현재가': '', '전일비': '', '등락률': '', '액면가': '', '상장주식수': '', 'PER': '', 'ROE': '', 'PBR': '', '유보율': '', '토론실': ''}

# 표 안에 있는 데이터 가져오기
table_heads = soup.select("table.type_2 > thead > tr > th[scope='col']")
for head in table_heads:
    print(head.get_text())
    kospi_data_sample[head.get_text()] = object()



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

    kospi_500_data.append(data) # 최종 데이터 Add
    # print(name, per, roe, pbr, reserve_ratio)

print(kospi_500_data)