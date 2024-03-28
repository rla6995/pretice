import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup as bs
url_list=["https://www.emuseum.go.kr/headerSearch?cateClass=&cateListFlag=&keyword=&pageNum=1&rows=9&reltRows=10&sort=&highQualityYn=&isImgExistOp=&mckoglsvOp=&isIntrstMuseumOp=&filedOp=&detailFlag=true&dq=&ps01Lv1=&ps01Lv2=&ps01Lv3=&mcSeqNo=&author=&ps06Lv1=&ps06Lv2=&ps08Lv1=PS08007&ps08Lv2=&ps09Lv1=&ps09Lv2=&ps09Lv3=&ps09Lv4=&gl05Lv1=&gl05Lv2=&ps12Lv1=&ps15Lv1=&culturalHerNo=&publicType=&detailedDes=&thema=&storySeq=&categoryLv=&categoryCode=&mobileFacetIng=&location=&facet1Lv1=&facet1Lv2=&facet2Lv1=&facet3Lv1=&facet3Lv2=&facet4Lv1=PS08007&facet4Lv2=&facet5Lv1=&facet5Lv2=&facet5Lv3=&facet5Lv4=&facet6Lv1=&facet6Lv2=&facet7Lv1Selected=&facet7Lv1=&facet8Lv1=&gl27Lv1=&gl27Lv2=&gl27Lv3=&gl27Lv4=&gl28Lv1=&gl28Lv2=&gl28Lv3=&gl29Lv1=&gl30Lv1=&mcgpyear1=&mcgpyear2=&mcginves=&mcgchalj=&mcgchams=&facetGL27Lv1=&facetGL27Lv2=&facetGL27Lv3=&facetGL27Lv4=&facetGL28Lv1=&facetGL28Lv2=&facetGL29Lv1=&facetGL30Lv1=&mcgwonpn=&keywordHistory=%EB%82%98%EB%AC%B4&showSearchOption=&intrstMuseumCode=&returnUrl=&selectMakerGroup=0&radioSearchCheck=&headerPs01Lv1=&headerPs01Lv2=&headerPs01Lv3=",
          "https://www.emuseum.go.kr/headerSearch?detailFlag=true&rows=9&pageNum=1&keywordHistory=%EC%A2%85%EC%9D%B4%2C%EC%A0%84%EC%B2%B4&searchType=1&dq=&location=&mcSeqNo=&author=&culturalHerNo=&tagInfos=&publicType=&ps01Lv1=&ps01Lv2=&ps01Lv3=&ps06Lv1=&ps06Lv2=&ps08Lv1=PS08009&ps08Lv2=&ps09Lv1=&ps09Lv2=&ps09Lv3=&ps09Lv4=&ps15Lv1=&ps12Lv1=&gl05Lv1=&gl05Lv2=&facet1Lv1=&facet1Lv2=&facet2Lv1=&facet3Lv1=&facet4Lv1=PS08009&facet5Lv1=&facet6Lv1=&facet8Lv1=&facet1Lv1Nm=&facet1Lv2Nm=&facet2Lv1Nm=&facet3Lv1Nm=&facet4Lv1Nm=%EC%A2%85%EC%9D%B4&facet5Lv1Nm=&facet6Lv1Nm=&facet8Lv1Nm=&tagOp=single",
          "https://www.emuseum.go.kr/headerSearch?detailFlag=true&rows=9&pageNum=1&keywordHistory=%EC%84%AC%EC%9C%A0%2C%EC%A0%84%EC%B2%B4&searchType=1&dq=&location=&mcSeqNo=&author=&culturalHerNo=&tagInfos=&publicType=&ps01Lv1=&ps01Lv2=&ps01Lv3=&ps06Lv1=&ps06Lv2=&ps08Lv1=PS08011&ps08Lv2=&ps09Lv1=&ps09Lv2=&ps09Lv3=&ps09Lv4=&ps15Lv1=&ps12Lv1=&gl05Lv1=&gl05Lv2=&facet1Lv1=&facet1Lv2=&facet2Lv1=&facet3Lv1=&facet4Lv1=PS08011&facet5Lv1=&facet6Lv1=&facet8Lv1=&facet1Lv1Nm=&facet1Lv2Nm=&facet2Lv1Nm=&facet3Lv1Nm=&facet4Lv1Nm=%EC%84%AC%EC%9C%A0&facet5Lv1Nm=&facet6Lv1Nm=&facet8Lv1Nm=&tagOp=single",
          "https://www.emuseum.go.kr/headerSearch?detailFlag=true&rows=9&pageNum=1&keywordHistory=%EC%94%A8%EC%95%97%2C%EC%A0%84%EC%B2%B4&searchType=1&dq=&location=&mcSeqNo=&author=&culturalHerNo=&tagInfos=&publicType=&ps01Lv1=&ps01Lv2=&ps01Lv3=&ps06Lv1=&ps06Lv2=&ps08Lv1=PS08012&ps08Lv2=&ps09Lv1=&ps09Lv2=&ps09Lv3=&ps09Lv4=&ps15Lv1=&ps12Lv1=&gl05Lv1=&gl05Lv2=&facet1Lv1=&facet1Lv2=&facet2Lv1=&facet3Lv1=&facet4Lv1=PS08012&facet5Lv1=&facet6Lv1=&facet8Lv1=&facet1Lv1Nm=&facet1Lv2Nm=&facet2Lv1Nm=&facet3Lv1Nm=&facet4Lv1Nm=%EC%94%A8%EC%95%97&facet5Lv1Nm=&facet6Lv1Nm=&facet8Lv1Nm=&tagOp=single",
          "https://www.emuseum.go.kr/headerSearch?detailFlag=true&rows=9&pageNum=1&keywordHistory=%ED%95%A9%EC%84%B1%EC%9E%AC%EC%A7%88%2C%EC%A0%84%EC%B2%B4&searchType=1&dq=&location=&mcSeqNo=&author=&culturalHerNo=&tagInfos=&publicType=&ps01Lv1=&ps01Lv2=&ps01Lv3=&ps06Lv1=&ps06Lv2=&ps08Lv1=PS08016&ps08Lv2=&ps09Lv1=&ps09Lv2=&ps09Lv3=&ps09Lv4=&ps15Lv1=&ps12Lv1=&gl05Lv1=&gl05Lv2=&facet1Lv1=&facet1Lv2=&facet2Lv1=&facet3Lv1=&facet4Lv1=PS08016&facet5Lv1=&facet6Lv1=&facet8Lv1=&facet1Lv1Nm=&facet1Lv2Nm=&facet2Lv1Nm=&facet3Lv1Nm=&facet4Lv1Nm=%ED%95%A9%EC%84%B1%EC%9E%AC%EC%A7%88&facet5Lv1Nm=&facet6Lv1Nm=&facet8Lv1Nm=&tagOp=single",
          "https://www.emuseum.go.kr/headerSearch?detailFlag=true&rows=9&pageNum=1&keywordHistory=%EC%B9%A0%EA%B8%B0%2C%EC%A0%84%EC%B2%B4&searchType=1&dq=&location=&mcSeqNo=&author=&culturalHerNo=&tagInfos=&publicType=&ps01Lv1=&ps01Lv2=&ps01Lv3=&ps06Lv1=&ps06Lv2=&ps08Lv1=PS08017&ps08Lv2=&ps09Lv1=&ps09Lv2=&ps09Lv3=&ps09Lv4=&ps15Lv1=&ps12Lv1=&gl05Lv1=&gl05Lv2=&facet1Lv1=&facet1Lv2=&facet2Lv1=&facet3Lv1=&facet4Lv1=PS08017&facet5Lv1=&facet6Lv1=&facet8Lv1=&facet1Lv1Nm=&facet1Lv2Nm=&facet2Lv1Nm=&facet3Lv1Nm=&facet4Lv1Nm=%EC%B9%A0%EA%B8%B0&facet5Lv1Nm=&facet6Lv1Nm=&facet8Lv1Nm=&tagOp=single"]
total=[]
sub=[]
wd = webdriver.Chrome()
for var5 in url_list:
    wd.get(var5)
    time.sleep(5)
    ps = wd.page_source
    code = bs(ps)
    item=code.select("div[class='item']")
    item2=code.select("span[class='f24']")
    for var4 in range(1,(int("".join(item2[0].text[1:-1].strip().split(",")))//90)+2):
        for var3 in range(4,13):
            for var in range(1,len(item)+1):
                wd.execute_script(f"document.querySelector('#contents > div.inner.up_container > div.result_form > div.overflow-h > div.right_form > div.img_list.overflow-h > div:nth-child({var}) > a').click()")
                time.sleep(5)
                ps2 = wd.page_source
                code2 = bs(ps2)
                lis=code2.select("li")
                for var2 in lis[16:24]:
                    sub.append(var2.text.split())
                total.append(sub)
                sub=[]
                wd.back()
            wd.find_element(By.XPATH, (f"/html/body/div[2]/div[1]/div[2]/div[2]/div[2]/div[3]/div[3]/ul/li[{var3}]/a")).click()
        if var4 != (int("".join(item2[0].text[1:-1].strip().split(",")))//90)+1:
            wd.find_element(By.XPATH, ("/html/body/div[2]/div[1]/div[2]/div[2]/div[2]/div[3]/div[3]/ul/li[13]/a")).click()
        else:
            pass