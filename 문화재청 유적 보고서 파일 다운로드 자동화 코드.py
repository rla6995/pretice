from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re
import pickle
import tarfile
# 목록 불러오기(이름은 목록 파일 이름,경로는 파일 있는곳으로 지정 필요)
with open('data_list.pickle', 'rb') as f:
    data = pickle.load(f)
# 웹드라이버 옵션 설정
options = webdriver.ChromeOptions()
prefs = {'download.default_directory': '다운로드'}
options.add_experimental_option('prefs', prefs)
# 목록 불러오기2(이름은 목록 파일 이름,경로는 파일 있는곳으로 지정 필요)
# 목록 불러오기는 둘 중 하나만 수행하면 됨
filename = 'C:/Users/USER/data_list.spydata'
tar = tarfile.open(filename, "r")
tar.extractall()
extracted_files = tar.getnames()
for f in extracted_files:
    if f.endswith('.pickle'):
        with open(f, 'rb') as fdesc:
            data = pickle.loads(fdesc.read())
# 목록 정렬 후 중복 제거
data_list = sorted(list(data["data_list"]))
set(data_list)
# 웹 드라이버 실행
wd = webdriver.Chrome(options=options)
wd.get("https://www.e-minwon.go.kr:8443/hmop/Hp_GrndreptList.do")
# 리스트 개수 만큼 반복문 실행
for var in data_list:
    # 목록의 보고서 검색 후 클릭
    wd.find_element(By.XPATH, "/html/body/div/div/div/form/div/div[1]/div/fieldset/table/tbody/tr[2]/td[2]/input").send_keys(f"{var}")
    wd.find_element(By.XPATH, "/html/body/div/div/div/form/div/div[1]/div/fieldset/table/tbody/tr[3]/td[5]/input[1]").click()
    wd.find_element(By.XPATH, "/html/body/div/div/div/form/div/table/tbody/tr/td[2]/a").click()
    # 첨부파일 프레임으로 변경 후 필요 데이터 추출(test2=첨부파일 건수)
    WebDriverWait(wd, 10).until(EC.frame_to_be_available_and_switch_to_it((By.NAME, 'fileframe')))
    a = WebDriverWait(wd, 10).until(EC.visibility_of_element_located((By.XPATH, '/html/body/form[1]/span'))).text
    test = WebDriverWait(wd, 10).until(EC.visibility_of_element_located((By.XPATH, '/html/body/form'))).text
    test1 = re.findall(r'\[(.*?)\]', test)
    test2 = re.findall(r'\d+', test1[0].split()[1])[0]
    a1 = re.findall('\((.*?)\)', a)
    wd.switch_to.default_content()
    # 조건문으로 첨부파일 개수 별 다른 실행 지정
    if int(test2) > 1:
        # 첨부파일 경로 코드 설정
        url = '/html/body/form/a'
        # 첨부파일 개수 만큼 반복시행
        for var2 in range(1, int(test2) + 1):
            # 첨부 파일의 경로 코드 변경 후 다운로드
            url = url[:-2] + "/span" + url[-2:]
            WebDriverWait(wd, 10).until(EC.frame_to_be_available_and_switch_to_it((By.NAME, 'fileframe')))
            wd.find_element(By.XPATH, url).click()
            # 시도 했을 때 팝업 창이 떳을 시 다음과 같은 작업 수행
            try:
                # 경고 창 뜨면 경고창으로 전환
                WebDriverWait(wd, 3).until(EC.alert_is_present())
                # 경고문 확인 버튼 누르기
                alert = wd.switch_to.alert
                alert.accept()
                # 새 팝업 창으로 전환
                WebDriverWait(wd, 10).until(EC.number_of_windows_to_be(2))
                wd.switch_to.window(wd.window_handles[1])
                # 팝업 창의 다운로드 버튼 클릭
                WebDriverWait(wd, 10).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[2]"))).click()
                # 닫고 기다린 후 원래 창으로 전환
                wd.close()
                time.sleep(10)
                wd.switch_to.window(wd.window_handles[0])
            except:
                pass
    # 첨부 파일 1개 일때 작업 수행
    else:
        # 경로 코드 생성
        url = '/html/body/form/span/a'
        # 첨부 파일 프레임으로 전환 후 파일 다운로드
        WebDriverWait(wd, 10).until(EC.frame_to_be_available_and_switch_to_it((By.NAME, 'fileframe')))
        wd.find_element(By.XPATH, url).click()
        # 시도 했을 때 팝업 창이 떳을 시 다음과 같은 작업 수행
        try:
            # 경고 창 뜨면 경고창으로 전환
            WebDriverWait(wd, 3).until(EC.alert_is_present())
            # 경고문 확인 버튼 누르기
            alert = wd.switch_to.alert
            alert.accept()
            # 새 팝업 창으로 전환
            WebDriverWait(wd, 10).until(EC.number_of_windows_to_be(2))
            wd.switch_to.window(wd.window_handles[1])
            # 팝업 창의 다운로드 버튼 클릭
            WebDriverWait(wd, 10).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[2]/input"))).click()
            # 닫고 기다린 후 원래 창으로 전환
            wd.close()
            wd.switch_to.window(wd.window_handles[0])
        except:
            pass
    # 원래 창으로 돌아 온 후 뒤로 가기
    wd.switch_to.default_content()
    wd.back()
    # 검색란 글자 제거
    wd.find_element(By.XPATH, "/html/body/div/div/div/form/div/div[1]/div/fieldset/table/tbody/tr[2]/td[2]/input").clear()

# 이 파일은 한가지 문제점이 존재
# 첨부 파일의 개수가 다수일 때 마지막이 팝업 창이 뜨는 경우 다운을 받은 후 뒤로가기가 진행이 안됨, 이에 대한 코드 수정이 필요함