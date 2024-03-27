# 필요 라이브러리 임포트
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup as bs
# 필요 리스트 생성
list_total=[]
list_sub=[]
# 내부 데이터 추출 과정(내부 데이터 링크 직접 접근)
for var in range(7088,7869):
    # 웹 드라이버 실행
    wd = webdriver.Chrome()
    wd.get(f"https://db.ffpri.go.jp/WoodDB/IDBK/ident.php?-action=browse&-recid={var}")
    time.sleep(3)
    # 페이지 파싱
    ps = wd.page_source
    code = bs(ps)
    # 코드 추출
    table2=code.select("font[size='3']")
    table3=code.select("table[border='1']")
    # 데이터 추출
    content=" ".join(table2[0].text.split())
    for var2 in range(1,len(table2[1:])+1):
        list_sub.append(content)
        list_sub.append(table2[var2].text.strip())
        for test2 in (table3[var2-1].text.split("\n\n\n")):
            list_sub.append(test2.split("\n\n"))
        list_total.append(list_sub)
        list_sub=[]
    # 닫기
    wd.close()
# 외부 데이터 추출 과정(외부 데이터 링크로 접근)
# 필요 리스트 생성
a=[]
b=[]
# 링크 수 만큼 반복수행
for var in range(0,800,50):
    # 웹 드라이버 실행
    wd2 = webdriver.Chrome()
    wd2.get(f"https://db.ffpri.go.jp/WoodDB/IDBK/recordlist.php?-action=find&-skip={var}&-max=50")
    time.sleep(3)
    # 페이지 파싱
    ps2 = wd2.page_source
    code2 = bs(ps2)
    table1=code2.select("tr[class='alt_row']")
    table2=code2.select("tr[class='table_row']")
    # 데이터 추출
    for var2 in table1:
        a.append(var2.text.split()[0])
        a.append(var2.text.split()[1])
        a.append(" ".join(var2.text.split()[2:-1]))
        a.append(" ".join(var2.text.split()[-1]))
        b.append(a)
        a=[]
    for var2 in table2:
        a.append(var2.text.split()[0])
        a.append(var2.text.split()[1])
        a.append(" ".join(var2.text.split()[2:-1]))
        a.append(" ".join(var2.text.split()[-1]))
        b.append(a)
        a=[]
    # 닫기
    wd2.close()
# 정렬
b.sort()
# 공백 및 빈칸 제거
b1 = [item for item in b for _ in range(8)]
# 내부 데이터에 연결
for ch1 in range(0,len(list_total)):
    for var1 in b1[ch1]:
        list_total[ch1][0]=b1[ch1]
# 데이터 전처리
sub=[]
result=[]
for var3 in list_total:
    for var4 in var3[2:]:
        for var in var3[0]:
            sub.append(var)
        filtered_list = [item for item in var4 if item.strip() != ""]
        sub.append(var3[1])
        for var5 in filtered_list:
            sub.append(var5)
        result.append(sub)
        sub=[]
# 데이터 엑셀 파일로 저장
result1=pd.DataFrame(result,columns=["Family","Genus","Species","화명","name1","name2","name3"])
result1.to_excel("일본 사이트.xlsx")
