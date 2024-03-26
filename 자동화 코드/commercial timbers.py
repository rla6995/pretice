# 라이브러리 임포트
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup as bs
import time
import pandas as pd
# 웹 드라이버 실행
wd = webdriver.Chrome()
wd.get("https://www.delta-intkey.com/wood/en/index.htm")
wait = WebDriverWait(wd, 10)
# 페이지 파싱
ps = wd.page_source
code = bs(ps)
tables = code.select("p")
# 필요 리스트 생성
total = []
sub = []
# 개수만큼 반복문 시행
for var in range(11, 37):
    wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)
    # 리스트 생성할 데이터 추출
    a = wait.until(EC.visibility_of_element_located((By.XPATH, f"/html/body/p[{var}]")))
    wait.until(EC.element_to_be_clickable((By.XPATH, f"/html/body/p[{var}]")))
    # 리스트 반복 시행
    for idx, var2 in enumerate((a.text.split("•")[1:])):
        wd.find_element(By.XPATH, f"/html/body/p[{var}]/a[{idx + 2}]").click()
        time.sleep(2)
        # 내부 페이지 파싱
        ps2 = wd.page_source
        code2 = bs(ps2)
        # 코드 선택 후 데이터 추출
        content = code2.select("h3")
        tables2 = code2.select("p")
        sub.append(content[0].text)
        for var3 in tables2[:-1]:
            sub.append(var3.text)
        total.append(sub)
        sub=[]
        # 돌아가기
        wd.back()
# 데이터 엑셀 파일로 저장
data=pd.DataFrame(total,columns=["name1","name2","name3","name4","name5","name6","name7","name8","name9","name10","name11","name12","name13","name14","name15","name16","name17","name18"])
data.to_excel("timber.xlsx")
