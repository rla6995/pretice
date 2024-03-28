import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup as bs
total=[]
sub=[]
wd = webdriver.Chrome()
wd.get("http://www.nature.go.kr/kpni/SubIndex.do")
for var in range(1,4):
    wd.find_element(By.XPATH, (f"/html/body/div[2]/div/div/div[2]/div[3]/table/tbody/tr[{var}]/td[3]/a")).click()
    ps = wd.page_source
    code = bs(ps)
    list1=code.select("tr")
    check=code.select("p[class='page_num']")
    check1=check[0].text.split()[4].split("/")[1][:-1]
    for var4 in range(1,(int(check1)//10)+1):
        for var3 in range(2,12):
            a=var3
            for idx, var2 in enumerate(list1[1:]):
                wd.execute_script(f"document.querySelector('#txt > form:nth-child(3) > table > tbody > tr:nth-child({idx+1}) > td.left > a').click()")
                time.sleep(3)
                ps2 = wd.page_source
                code2 = bs(ps2)
                list2=code2.select("tr")
                for var3 in list2[1:]:
                    sub.append(var3.text.split())
                total.append(sub)
                sub=[]
                wd.find_element(By.XPATH, ("/html/body/div[2]/div[2]/div[2]/form[4]/div/a")).click()
                time.sleep(3)
            if a != 11:
                wd.execute_script(f"document.querySelector('#txt > form:nth-child(3) > div.bd_page > span.page_num > a:nth-child({a})').click()")
            else:
                pass
        try:
            wd.execute_script("document.querySelector('#txt > form:nth-child(3) > div.bd_page > span:nth-child(4) > a').click()")
        except:
            pass
    wd.back()