# 필요 라이브러리 임포트
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup as bs
# 필요 리스트 생성
list_total=[]
list_sub=[]
# 웹드라이버 실행
for var in range(7088,7869):
    wd = webdriver.Chrome()
    wd.get(f"https://db.ffpri.go.jp/WoodDB/IDBK/ident.php?-action=browse&-recid={var}")
    time.sleep(3)
    ps = wd.page_source
    code = bs(ps)
    table2=code.select("font[size='3']")
    table3=code.select("table[border='1']")
    content=" ".join(table2[0].text.split())
    for var2 in range(1,len(table2[1:])+1):
        list_sub.append(content)
        list_sub.append(table2[var2].text.strip())
        for test2 in (table3[var2-1].text.split("\n\n\n")):
            list_sub.append(test2.split("\n\n"))
        list_total.append(list_sub)
        list_sub=[]
    wd.close()