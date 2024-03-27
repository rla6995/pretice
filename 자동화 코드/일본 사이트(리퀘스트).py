# 필요 라이브러리 임포트
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import requests
from bs4 import BeautifulSoup as bs
# 필요 리스트 생성
list_total=[]
list_sub=[]
# 내부 데이터 추출 과정(데이터 리퀘스트)
url1="https://db.ffpri.go.jp/WoodDB/IDBK/ident.php?-action=browse&-recid="
for var in range(7088,7869):
    # 페이지 파싱
    ps=requests.get(url1+str(var))
    code = bs(ps.text)
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
# 외부 데이터 추출 과정(데이터 리퀘스트)
# 필요 리스트 생성
a=[]
b=[]
# 링크 수 만큼 반복수행
url2="https://db.ffpri.go.jp/WoodDB/IDBK/recordlist.php?-action=find&-skip="
for var in range(0,800,50):
    ps2=requests.get(url2+str(var)+"&-max=50")
    # 페이지 파싱
    code2 = bs(ps2.text)
    table1=code2.select("tr")
    # 데이터 추출
    for var2 in table1[2:-1]:
        tds=var2.select("td")
        for var3 in tds[:-1]:
            a.append(var3.text.strip())
        b.append(a)
        a=[]
# 내부 데이터에 연결
b1=[item for item in b for _ in range(8)]
for ch1 in range(0,len(list_total)):
    for ch2 in b1[ch1]:
        list_total[ch1][0]=b1[ch1]
# 데이터 전처리
sub=[]
result=[]
for var3 in list_total:
    for var4 in var3[2:]:
        for var in var3[0]:
            sub.append(var)
        sub.append(var3[1])
        for var5 in var4:
            sub.append(var5)
        result.append(sub)
        sub=[]
# 데이터 엑셀 파일로 저장
result1=pd.DataFrame(result,columns=["Family","Genus","Species","화명","name1","name2","name3"])
result1.to_excel("일본 사이트.xlsx")