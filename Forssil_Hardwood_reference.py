import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from bs4 import BeautifulSoup as bs
import re
import numpy as np
Forssil_Hardwood=[]
sub_wood=[]
alpabet=[2,3,4,5,6,7,8,9,10,12,13,14,15,16,18,19,20,21,22]
wd = webdriver.Chrome()
wd.get("https://insidewood.lib.ncsu.edu/taxtree/typeofwood/FH/letter/a/taxtype/family?1")
for var in alpabet:
    ps = wd.page_source
    code = bs(ps)
    tables = code.select("div[class='wicket-tree']")
    count_list=tables[0].text.split()
    for idx, var1 in enumerate(count_list):
        wd.find_element(By.XPATH, (f"/html/body/table[3]/tbody/tr/td[4]/table[2]/tbody/tr/td/div/div/div[{idx+2}]/div/a[2]")).click()
        time.sleep(3)
        ps = wd.page_source
        code = bs(ps)
        tds=code.select("td[class=description]")
        for idc,var2 in enumerate(tds):
            wd.find_element(By.XPATH, (f"/html/body/table[3]/tbody/tr/td[4]/table[2]/tbody/tr[{idc+2}]/td[4]/a")).click()
            time.sleep(3)
            tds1=wd.find_element(By.CSS_SELECTOR, "body > table:nth-child(3) > tbody > tr > td:nth-child(4) > div:nth-child(2) > table > tbody > tr > td")  
            sub_wood.append(tds1.text.split(" ",3))
            try:
                tds2=wd.find_element(By.CSS_SELECTOR,"body > table:nth-child(3) > tbody > tr > td:nth-child(4) > div:nth-child(5) > table > tbody")    
                sub_wood.append(tds2.text.split("\n",))
            except:
                pass
            try:
                tds3=wd.find_element(By.CSS_SELECTOR,"body > table:nth-child(3) > tbody > tr > td:nth-child(4) > div:nth-child(7)")
                sub_wood.append(tds3.text.split("\n"))
            except:
                pass
            Forssil_Hardwood.append(sub_wood)
            sub_wood=[]
            wd.back()
        test=code.select("td[align=left]")
        a=test[4].text.split()
        if a[3]!=a[5]:
            wd.find_element(By.XPATH, ("/html/body/table[3]/tbody/tr/td[4]/table[1]/tbody/tr[5]/td[3]/span/a[1]")).click()
            time.sleep(3)
            ps = wd.page_source
            code = bs(ps)
            tds = code.select("td[class=description]")
            for idc,var2 in enumerate(tds):
                wd.find_element(By.XPATH, (f"/html/body/table[3]/tbody/tr/td[4]/table[2]/tbody/tr[{idc+2}]/td[4]/a")).click()
                time.sleep(3)
                tds1=wd.find_element(By.CSS_SELECTOR, "body > table:nth-child(3) > tbody > tr > td:nth-child(4) > div:nth-child(2) > table > tbody > tr > td")  
                sub_wood.append(tds1.text.split(" ",3))
                try:
                    tds2=wd.find_element(By.CSS_SELECTOR,"body > table:nth-child(3) > tbody > tr > td:nth-child(4) > div:nth-child(5) > table > tbody")    
                    sub_wood.append(tds2.text.split("\n",))
                except:
                    pass
                try:
                    tds3=wd.find_element(By.CSS_SELECTOR,"body > table:nth-child(3) > tbody > tr > td:nth-child(4) > div:nth-child(7)")
                    sub_wood.append(tds3.text.split("\n"))
                except:
                    pass
                Forssil_Hardwood.append(sub_wood)
                sub_wood=[]
                wd.back()
            while True:
                try:
                    wd.find_element(By.XPATH, ("/html/body/table[3]/tbody/tr/td[4]/table[1]/tbody/tr[5]/td[3]/span/a[3]")).click()
                    time.sleep(3)
                    ps = wd.page_source
                    code = bs(ps)
                    tds = code.select("td[class=description]")
                    for idc,var2 in enumerate(tds):
                        wd.find_element(By.XPATH, (f"/html/body/table[3]/tbody/tr/td[4]/table[2]/tbody/tr[{idc+2}]/td[4]/a")).click()
                        time.sleep(3)
                        tds1=wd.find_element(By.CSS_SELECTOR, "body > table:nth-child(3) > tbody > tr > td:nth-child(4) > div:nth-child(2) > table > tbody > tr > td")  
                        sub_wood.append(tds1.text.split(" ",3))
                        try:
                            tds2=wd.find_element(By.CSS_SELECTOR,"body > table:nth-child(3) > tbody > tr > td:nth-child(4) > div:nth-child(5) > table > tbody")    
                            sub_wood.append(tds2.text.split("\n",))
                        except:
                            pass
                        try:
                            tds3=wd.find_element(By.CSS_SELECTOR,"body > table:nth-child(3) > tbody > tr > td:nth-child(4) > div:nth-child(7)")
                            sub_wood.append(tds3.text.split("\n"))
                        except:
                            pass
                        Forssil_Hardwood.append(sub_wood)
                        sub_wood=[]
                        wd.back()
                except:
                    break
        else:
            pass
        wd.back()
    wd.find_element(By.XPATH, (f"/html/body/table[3]/tbody/tr/td[4]/table[1]/tbody/tr/td[{var}]/a")).click()
    time.sleep(5)
a=[]
b=[]        
c=[]
for var in Forssil_Hardwood:
    if len(var)==1:
        a.append(var[0])
        b.append("")
        c.append("")
    elif len(var)==2:
        a.append(var[0])
        b.append(var[1])
        c.append("")
    elif len(var)==3 or 4:
        a.append(var[0])
        b.append(var[1])
        if type(var[2])==list:
            if len(var[2])>1:
                c.append((var[2][1:]))
            else:
                c.append(var[2][0][13:])
        else:
            c.append(var[2][13:])
b_re=[]
for var2 in b:
    b_re.append(var2[::2])
b_re2=[]
for var3 in b_re:
    b_re2.append(", ".join(var3))
for var4 in range(len(c)):
    if type(c[var4])==list:
        c[var4]=" ".join(c[var4])
FH_df=pd.DataFrame(a,columns=["name1","name2","name3","name4"])
FH_number=pd.Series(b_re2,name="number")
FH_reference=pd.Series(c,name="reference")
FH_df["number"]=FH_number
FH_df["reference"]=FH_reference
FH_df.to_excel('FH_all.xlsx', index=True)