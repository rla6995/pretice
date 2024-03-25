# 필요 라이브러리 임포트
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup as bs
import pandas as pd
# 필요 리스트 생성
Base_list=[]
start=[1,2,3,4,5,6,7,8,9,10]
other=[3,4,5,6,7,8,9,10,11,12]
check=0
# 웹드라이버 실행
wd = webdriver.Chrome()
wd.get("https://www.e-minwon.go.kr:8443/hmop/Hp_GrndreptList.do")
# 유적 페이지 수 만큼 반복 실행
for var in range(1,77):
    # 처음 열과 그 다음열들의 넘기는 부분의 코드가 달라 따로 실행
    if check==0:
        # 1_10번째
        for a1 in start:
            # 세부 페이지 반복
            for var1 in range(1,11):
                # 클릭 후 페이지 파싱
                wd.find_element(By.XPATH, (f"//tr[{var1}]/td[2]/a[@href='#']")).click()
                time.sleep(3)
                ps = wd.page_source
                code = bs(ps)
                # 추출 데이터 선택(tr들 선택 후 td들을 추출해서 데이터 추출)
                tables = code.select("table[class='tbl type_02 mb_10']")
                trs = tables[0].select("tr")
                sub = []
                total = []
                for var2 in trs:
                    tds = var2.select("td")
                    for var3 in tds:
                    # td코드들에서 필요 데이터 추출 후 리스트에 넣기
                        sub.append(var3.text)
                    total.append(sub[0].strip())
                    sub = []
                # 데이터들 리스트에 넣기
                Base_list.append(total)
                # 원래 페이지로 이동
                wd.back()
            # 다음 페이지로 넘기기
            next_page_element = wd.find_element(By.XPATH, f"/html/body/div/div/div/form/div/div[4]/div/a[{a1}]")
            next_page_element.click()
        check=check+1
    else:
        # 그 이후 계속 반복
        for a1 in other:
            # 세부 페이지 반복
            for var1 in range(1,11):
                # 클릭 후 페이지 파싱
                wd.find_element(By.XPATH, (f"//tr[{var1}]/td[2]/a[@href='#']")).click()
                time.sleep(3)
                ps = wd.page_source
                code = bs(ps)
                # 추출 데이터 선택(tr들 선택 후 td들을 추출해서 데이터 추출)
                tables = code.select("table[class='tbl type_02 mb_10']")
                trs = tables[0].select("tr")
                sub = []
                total = []
                for var2 in trs:
                    tds = var2.select("td")
                    for var3 in tds:
                    # td코드들에서 필요 데이터 추출 후 리스트에 넣기
                        sub.append(var3.text)
                    total.append(sub[0].strip())
                    sub = []
                # 데이터들 리스트에 넣기
                Base_list.append(total)
                # 원래 페이지로 이동
                wd.back()
            # 다음 페이지로 넘기기
            next_page_element = wd.find_element(By.XPATH, f"/html/body/div/div/div/form/div/div[4]/a[{a1}]")
            next_page_element.click()
        check=check+1
    # 큰 틀 페이지 넘기기
    next_link = wd.find_element(By.CSS_SELECTOR, "a.next")
    next_link.click()
#리스트 데이터프레임으로 변환
base_df=pd.DataFrame(Base_list,columns=[""])
