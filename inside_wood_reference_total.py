# 필요 라이브러리 임포트
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup as bs
# 필요 리스트 생성
total=[]
alpabet1=[2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,26,99]
alpabet2=[2,3,4,5,6,7,8,9,10,12,13,14,15,16,18,19,20,21,22,99]
alpabet3=[3,16,19,20,99]
url_list=["https://insidewood.lib.ncsu.edu/taxtree/typeofwood/MH/letter/a/taxtype/family?1","https://insidewood.lib.ncsu.edu/taxtree/typeofwood/FH/letter/a/taxtype/family?1","https://insidewood.lib.ncsu.edu/taxtree/typeofwood/MS/letter/a/taxtype/family?1"]
alpabet_list=[alpabet1,alpabet2,alpabet3]
sub_wood=[]
# 웹드라이버 실행
for url,alpha in zip(url_list,alpabet_list):
    wd = webdriver.Chrome()
    wd.get(url)
    # 리스트 반복문 시행
    for var in alpha:
        # 파싱 후 목록 추출
        ps = wd.page_source
        code = bs(ps)
        tables = code.select("div[class='wicket-tree']")
        # 목록 리스트 생성
        count_list=tables[0].text.split()
        # 목록 리스트 수 만큼 반복문 시행
        for idx, var1 in enumerate(count_list):
            # 목록 클릭 후 페이지 파싱 
            wd.find_element(By.XPATH, (f"/html/body/table[3]/tbody/tr/td[4]/table[2]/tbody/tr/td/div/div/div[{idx+2}]/div/a[2]")).click()
            time.sleep(3)
            ps = wd.page_source
            code = bs(ps)
            # 세부 목록 코드 추출
            tds=code.select("td[class=description]")
            # 세부 목록 만큼 반복문 시행
            for idc,var2 in enumerate(tds):
                # 세부 목록 클릭
                wd.find_element(By.XPATH, (f"/html/body/table[3]/tbody/tr/td[4]/table[2]/tbody/tr[{idc+2}]/td[4]/a")).click()
                time.sleep(3)
                # 데이터 추출(이름)
                tds1=wd.find_element(By.CSS_SELECTOR, "body > table:nth-child(3) > tbody > tr > td:nth-child(4) > div:nth-child(2) > table > tbody > tr > td")  
                sub_wood.append(tds1.text.split(" ",3))
                # 데이터 추출(숫자), 시도해보고 해당 요소 없으면 패스
                try:
                    tds2=wd.find_element(By.CSS_SELECTOR,"body > table:nth-child(3) > tbody > tr > td:nth-child(4) > div:nth-child(5) > table > tbody")    
                    sub_wood.append(tds2.text.split("\n",))
                except:
                    pass
                # 데이터 추출(참고문헌), 시도해보고 해당 요소 없으면 패스
                try:
                    tds3=wd.find_element(By.CSS_SELECTOR,"body > table:nth-child(3) > tbody > tr > td:nth-child(4) > div:nth-child(7)")
                    sub_wood.append(tds3.text.split("\n"))
                except:
                    pass
                # 추출 데이터들 목록에 넣기
                total.append(sub_wood)
                # 서브 목록 초기화
                sub_wood=[]
                # 목록으로 돌아가기
                wd.back()
            # 페이지 수 확인을 위한 총 개수 확인
            test=code.select("td[align=left]")
            a=test[4].text.split()
            # 페이지 수가 여러개 일시 조건문 실행, 1페이지 일시 패스
            if a[3]!=a[5]:
                # 다음으로 가는 버튼 클릭
                wd.find_element(By.XPATH, ("/html/body/table[3]/tbody/tr/td[4]/table[1]/tbody/tr[5]/td[3]/span/a[1]")).click()
                time.sleep(3)
                # 페이지 파싱 후 세부목록 추출
                ps = wd.page_source
                code = bs(ps)
                tds = code.select("td[class=description]")
                # 세부 목록 만큼 반복문 시행
                for idc,var2 in enumerate(tds):
                    # 세부 목록 클릭
                    wd.find_element(By.XPATH, (f"/html/body/table[3]/tbody/tr/td[4]/table[2]/tbody/tr[{idc+2}]/td[4]/a")).click()
                    time.sleep(3)
                    # 데이터 추출(이름)
                    tds1=wd.find_element(By.CSS_SELECTOR, "body > table:nth-child(3) > tbody > tr > td:nth-child(4) > div:nth-child(2) > table > tbody > tr > td")  
                    sub_wood.append(tds1.text.split(" ",3))
                    # 데이터 추출(숫자), 시도해보고 해당 요소 없으면 패스
                    try:
                        tds2=wd.find_element(By.CSS_SELECTOR,"body > table:nth-child(3) > tbody > tr > td:nth-child(4) > div:nth-child(5) > table > tbody")    
                        sub_wood.append(tds2.text.split("\n",))
                    except:
                        pass
                    # 데이터 추출(참고문헌), 시도해보고 해당 요소 없으면 패스
                    try:
                        tds3=wd.find_element(By.CSS_SELECTOR,"body > table:nth-child(3) > tbody > tr > td:nth-child(4) > div:nth-child(7)")
                        sub_wood.append(tds3.text.split("\n"))
                    except:
                        pass
                    # 추출 데이터들 목록에 넣기
                    total.append(sub_wood)
                    # 서브 목록 초기화
                    sub_wood=[]
                    # 목록으로 돌아가기
                    wd.back()
                # 페이지 수가 2개 이상일 때 While문으로 반복시행, 다음으로 넘기는 버튼을 누르는 것을 시행해서 가능하면 넘긴 후 데이터 추출, 반응 없으면 끝내기
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
                            total.append(sub_wood)
                            sub_wood=[]
                            wd.back()
                    except:
                        break
            else:
                pass
            # 큰 목록으로 돌아가기
            wd.back()
        # 다음 알파벳으로 넘기기, 만약 99(없는 항목)이라면 페이지를 넘기지 않고 그대로 반복문 종료
        if var != 99:
            wd.find_element(By.XPATH, (f"/html/body/table[3]/tbody/tr/td[4]/table[1]/tbody/tr/td[{var}]/a")).click()
            time.sleep(5)
# 추출 목록 구분할 빈 리스트 생성
a=[]
b=[]
c=[]
# 목록 구분해서 리스트에 넣기(a=이름,b=숫자,c=참고문헌, 데이터 프레임으로 만들 수 있도록 행 개수 통일, 참고문헌의 경우 불필요 부분 제거)
for var in total:
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
# 숫자 목록 전처리(불필요한 부분 제거 후 ", "로 합치기)
b_re=[]
for var2 in b:
    b_re.append(var2[::2])
b_re2=[]
for var3 in b_re:
    b_re2.append(", ".join(var3))
# 참고문헌 목록 전처리(여러개 일시 병합)
for var4 in range(len(c)):
    if type(c[var4])==list:
        c[var4]=" ".join(c[var4])
# 데이터프레임으로 변환
total_df=pd.DataFrame(a,columns=["name1","name2","name3","name4"])
total_number=pd.Series(b_re2,name="number")
total_reference=pd.Series(c,name="reference")
total_df["number"]=total_number
total_df["reference"]=total_reference
# 액셀 파일로 변환 저장
total_df.to_excel('total.xlsx', index=True)