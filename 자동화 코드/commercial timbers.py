from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup as bs
import time
wd = webdriver.Chrome()
wd.get("https://www.delta-intkey.com/wood/en/index.htm")
wait = WebDriverWait(wd, 10)
ps = wd.page_source
code = bs(ps)
tables = code.select("p")
total = []
sub = []
for var in range(11, 37):
    wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)
    a = wait.until(EC.visibility_of_element_located((By.XPATH, f"/html/body/p[{var}]")))
    wait.until(EC.element_to_be_clickable((By.XPATH, f"/html/body/p[{var}]")))
    for idx, var2 in enumerate((a.text.split("•")[1:])):
        wd.find_element(By.XPATH, f"/html/body/p[{var}]/a[{idx + 2}]").click()
        time.sleep(2)
        ps2 = wd.page_source
        code2 = bs(ps2)
        content = code2.select("h3")
        tables2 = code2.select("p")
        sub.append(content[0].text)
        for var3 in tables2[:-1]:
            sub.append(var3.text)
        total.append(sub)
        sub=[]
        wd.back()