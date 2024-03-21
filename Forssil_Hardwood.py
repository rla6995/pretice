# 필요 라이브러리 임포트
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup as bs
import re
# 필요 리스트 생성
Forssil_Hardwood=[]
alpabet=[2,3,4,5,6,7,8,9,10,12,13,14,15,16,18,19,20,21,22]
# 웹 드라이버 실행
wd = webdriver.Chrome()
wd.get("https://insidewood.lib.ncsu.edu/taxtree/typeofwood/FH/letter/a/taxtype/family?1")
for var in alpabet:
    # 페이지 파싱 후 목록 추출
    ps = wd.page_source
    code = bs(ps)
    tables = code.select("div[class='wicket-tree']")
    count_list=tables[0].text.split()
    # 요소 수 만큼 반복 실행
    for idx, var1 in enumerate(count_list):
        # 페이지 클릭 후 요소 추출
        wd.find_element(By.XPATH, (f"/html/body/table[3]/tbody/tr/td[4]/table[2]/tbody/tr/td/div/div/div[{idx+2}]/div/a[2]")).click()
        time.sleep(3)
        ps = wd.page_source
        code = bs(ps)
        tds=code.select("td[class=description]")
        for var2 in tds:
            # 데이터 목록에 넣기
            Forssil_Hardwood.append(var2.get_text().split(' ',3))
        # 페이지 수 다수일 경우 확인
        test=code.select("td[align=left]")
        a=test[4].text.split()
        if a[3]!=a[5]:
            # 페이지 개수가 여러 개 일 경우 페이지 넘기고 데이터 추출 저장 작업 실행
            wd.find_element(By.XPATH, ("/html/body/table[3]/tbody/tr/td[4]/table[1]/tbody/tr[5]/td[3]/span/a[1]")).click()
            time.sleep(3)
            ps = wd.page_source
            code = bs(ps)
            tds = code.select("td[class=description]")
            for var2 in tds:
                Forssil_Hardwood.append(var2.get_text().split(' ', 3))
            # while문 이용 페이지가 넘어가지지 않을 때까지 반복 실행
            while True:
                try:
                    wd.find_element(By.XPATH, ("/html/body/table[3]/tbody/tr/td[4]/table[1]/tbody/tr[5]/td[3]/span/a[3]")).click()
                    time.sleep(3)
                    ps = wd.page_source
                    code = bs(ps)
                    tds = code.select("td[class=description]")
                    for var2 in tds:
                        Forssil_Hardwood.append(var2.get_text().split(' ', 3))
                except:
                    break
        else:
            pass
        # 모든 과정 마치고 뒤로 돌아가기
        wd.back()
    # var의 숫자를 이용해서 다음 알파벳으로 넘기기 99가 되면 반복문 종료
    if var != 99:
        wd.find_element(By.XPATH, (f"/html/body/table[3]/tbody/tr/td[4]/table[1]/tbody/tr/td[{var}]/a")).click()
        time.sleep(5)
# 데이터 전처리 작업
FH_df=pd.DataFrame(Forssil_Hardwood)
result = []
for var in Forssil_Hardwood:
    result.append(" ".join(item for item in var if item is not None))
result2=[]
for var1 in result:
    result2.append(re.split(r'(\d+)',var1))
sub=[]
total=[]
for var2 in result2:
    if len(var2)>1:
        sub.append(var2[0])
        sub.append("".join(var2[1:]))
        total.append(sub)
        sub=[]
    else:
        sub.append(var2[0])
        total.append(sub)
        sub=[]
Forssil_Hardwood_list_sub=[]
Forssil_Hardwood_list=[]
for var3 in total:
    if len(var3)>1:
        for var4 in var3[0].split(maxsplit=3):
            Forssil_Hardwood_list_sub.append(var4)
        Forssil_Hardwood_list.append(Forssil_Hardwood_list_sub)
        Forssil_Hardwood_list_sub=[]
    else:
        Forssil_Hardwood_list.append(var3[0].split(maxsplit=3))
FH_number=[]
for var5 in total:
    if len(var5)>1:
        FH_number.append(var5[1].replace(" ",", "))
    else:
        FH_number.append("0")
# 데이터 프레임으로 변환
FH_df=pd.DataFrame(Forssil_Hardwood_list,columns=["name1","name2","name3","name4"])
FH_df["number"]=FH_number
FH_df["number"]=FH_df["number"].replace("0","")
# 엑셀 파일로 변환시켜 저장
FH_df.to_excel('Forssil_Hardwood.xlsx', index=True)