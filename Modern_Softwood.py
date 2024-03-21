# 필요 라이브러리 임포트
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup as bs
import re
# 필요 리스트 생성
Modern_Softwood=[]
alpabet=[3,16,19,20,99]
# 웹 드라이버 실행
wd = webdriver.Chrome()
wd.get("https://insidewood.lib.ncsu.edu/taxtree/typeofwood/MH/letter/a/taxtype/family?1")
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
            Modern_Softwood.append(var2.get_text().split(' ',3))
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
                Modern_Softwood.append(var2.get_text().split(' ', 3))
            # while문 이용 페이지가 넘어가지지 않을 때까지 반복 실행
            while True:
                try:
                    wd.find_element(By.XPATH, ("/html/body/table[3]/tbody/tr/td[4]/table[1]/tbody/tr[5]/td[3]/span/a[3]")).click()
                    time.sleep(3)
                    ps = wd.page_source
                    code = bs(ps)
                    tds = code.select("td[class=description]")
                    for var2 in tds:
                        Modern_Softwood.append(var2.get_text().split(' ', 3))
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
MS_df=pd.DataFrame(Modern_Softwood)
result = []
for var in Modern_Softwood:
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
Modern_Softwood_list_sub=[]
Modern_Softwood_list=[]
for var3 in total:
    if len(var3)>1:
        for var4 in var3[0].split(maxsplit=3):
            Modern_Softwood_list_sub.append(var4)
        Modern_Softwood_list.append(Modern_Softwood_list_sub)
        Modern_Softwood_list_sub=[]
    else:
        Modern_Softwood_list.append(var3[0].split(maxsplit=3))
MS_number=[]
for var5 in total:
    if len(var5)>1:
        MS_number.append(var5[1].replace(" ",", "))
    else:
        MS_number.append("0")
# 데이터 프레임으로 변환
MS_df=pd.DataFrame(Modern_Softwood_list,columns=["name1","name2","name3","name4"])
MS_df["number"]=MS_number
MS_df["number"]=MS_df["number"].replace("0","")
# 엑셀 파일로 변환시켜 저장
MS_df.to_excel('Modern_Hardwood.xlsx', index=True)
