# 모듈 가져오기
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
import seaborn as sns
# 데이터 불러오기(나이별, 성별, 목적별, 교통수단별)
age=pd.read_csv("./20231204140943_방한 외래관광객 연령별.csv",encoding='cp949')
gender=pd.read_csv("./20231204140922_방한 외래관광객 성별.csv",encoding='cp949')
purpose=pd.read_csv("./20231204141001_방한 외래관광객 목적별.csv",encoding='cp949')
traffic=pd.read_csv("./20231204141022_방한 외래관광객 교통수단별.csv",encoding='cp949')
# null값 확인하기
age.info()
gender.info()
purpose.info()
traffic.info()
# 기초통계량 확인하기
age_basic=age.describe()
gender_basic=gender.describe()
prupose_basic=purpose.describe()
traffic_basic=traffic.describe()
# 국가별 방문자수 평균 구하기
age_country=age.groupby("국가명")["인원"].mean().sort_values(ascending=False)
gender_country=gender.groupby("국가명")["인원"].mean().sort_values(ascending=False)
purpose_country=purpose.groupby("국가명")["인원"].mean().sort_values(ascending=False)
traffic_country=traffic.groupby("국가명")["인원"].mean().sort_values(ascending=False)
# 월간 국가별 방문자수 시각화(국가별 평균치 상위5개국)
age_date=age[age["연령"]==age["연령"].max()]
age_date=age_date.reset_index()
age_date=age_date.drop(columns="index")
age_date=age_date.drop(age_date.index[0])
age_date=age_date.drop(age_date.index[0])
age_date=age_date.drop(age_date.index[3126])
age_date["기준일자"]=pd.to_datetime(age_date["기준일자"],format="%Y%m")
top5_visitor=age_date["국가명"][0:5]
# 그래프 함수 제작
def time_graph(name):
    fig,axes = plt.subplots(1,1,figsize=(10, 8))
    x=age_date[age_date["국가명"]==name].기준일자
    y=age_date[age_date["국가명"]==name].인원
    axes.set_title(name)
    axes.set_ylabel("visitor")
    axes.set_xlabel("date")
    axes.plot(x, y, linewidth=3.0)
# 5개국 그래프 그리기
for var in top5_visitor:
    time_graph(var)
# 국가별 증감률 비교(국가별 평균치 상위5개국)
age_country_growth=age.groupby("국가명")["증감률"].max().sort_values(ascending=False)
age_date["증감률"]=age_date["증감률"].apply(lambda x:x.replace("_",""))
age_date["증감률"]=pd.to_numeric(age_date["증감률"])
age_growth=age_date.sort_values("기준일자",ascending=False)
age_growth=age_growth.reset_index()
age_growth=age_growth.drop(columns="index")
top5_growth=age_country_growth.index[0:5]
# 그래프 함수 제작
def time_graph2(name):
    fig,axes = plt.subplots(1,1,figsize=(10, 8))
    x=age_growth[age_growth["국가명"]==name].기준일자
    y=age_growth[age_growth["국가명"]==name].증감률
    axes.set_title(name)
    axes.set_ylabel("growth")
    axes.set_xlabel("date")
    axes.plot(x, y, linewidth=3.0)
# 5개국 그래프 그리기
for var in top5_growth:
    time_graph2(var)
