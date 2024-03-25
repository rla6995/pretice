# 모듈 불러오기
import sys
sys.path.append('./')
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import MWIS_metric
from category_encoders import OneHotEncoder, MEstimateEncoder
from sklearn.model_selection import KFold, StratifiedKFold, train_test_split
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.ensemble import HistGradientBoostingRegressor, VotingRegressor
from sklearn.metrics import median_absolute_error, roc_auc_score, roc_curve
from sklearn.metrics.pairwise import euclidean_distances
from sklearn.pipeline import make_pipeline
from sklearn.base import BaseEstimator, TransformerMixin, RegressorMixin, clone
from sklearn.preprocessing import FunctionTransformer, StandardScaler, PowerTransformer
from sklearn.linear_model import QuantileRegressor
from scipy.cluster.hierarchy import dendrogram, linkage
from scipy.spatial.distance import squareform
from mapie.regression import MapieRegressor
from sklego.linear_model import LADRegression
from xgboost import XGBRegressor, XGBClassifier
from lightgbm import LGBMRegressor
from catboost import CatBoostRegressor
# 파일 실행하기
sample=pd.read_csv("./birth_sample_submission.csv")
train=pd.read_csv("./birth_train.csv")
test=pd.read_csv("./birth_test.csv")
print("완료1")
# 데이터 기본정보 확인
train.info()
train_corr=train.corr()
print("완료2")
# DMAR(결혼상태),LD_INDL(분만유도),RF_CESAR(이전제왕절개여부),SEX=object
basic=train.describe()
print("완료3")
# 타겟 데이터 분포 확인
plt.hist(train["DBWT"])
plt.boxplot(train["DBWT"])
print("완료4")
# 누락값들 개수 확인(9,99,99.9,999,9999=누락 또는 미기재)
train_columns=train.columns.tolist()
for var in train_columns[1:]:
    print(train[str(var)].value_counts())
"""
ATTEND=56(9)
BFACIL=11(9)
BMI=2454(99.9)
CIG_0=516(99)
DLMP_MM=5075(99)
DMAR=13262( )
DOB_TT=2(9999)
FAGECOMB=12573(99)
FEDUC=14856(9)
ILLB_R=3431(999)
ILOP_R=10723(999)
ILP_R=12945(999)
MBSTATE_REC=211(3)
MEDUC=1441(9)
M_Ht_In=548(99)
NO_INFEC=202(9)
NO_MMORB=59(9)
PAY=622(9)
PAY_REC=622(9)
PRECARE=2668(99)
PREVIS=2745(99)
PRIORDEAD=242(99)
PRIORLIVE=171(99)
PRIORTERM=324(99)
PWgt_R=2187(999)
RDMETH_REC=24(9)
RF_CESARN=40(99)
WTGAIN=3287(99)
"""
print("완료4")
# 각 열의 데이터 특성 누락값 제거 후 확인
dic={"ATTEND":9,"BFACIL":9,"BMI":99.9,"CIG_0":99,"DLMP_MM":99,"DMAR":" ","DOB_TT":9999,"FAGECOMB":99,"FEDUC":9,"ILLB_R":999,"ILOP_R":999,"ILP_R":999,"MBSTATE_REC":3,"MEDUC":9,"M_Ht_In":99,"NO_INFEC":9,"NO_MMORB":9,"PAY":9,"PAY_REC":9,"PRECARE":99,"PREVIS":99,"PRIORDEAD":99,"PRIORLIVE":99,"PRIORTERM":99,"PWgt_R":999,"RDMETH_REC":9,"RF_CESARN":99,"WTGAIN":99}
null_columns=["ATTEND","BFACIL","BMI","CIG_0","DLMP_MM","DMAR","DOB_TT","FAGECOMB","FEDUC","ILLB_R","ILOP_R","ILP_R","MBSTATE_REC","MEDUC","M_Ht_In","NO_INFEC","NO_MMORB","PAY","PAY_REC","PRECARE","PREVIS","PRIORDEAD","PRIORLIVE","PRIORTERM","PWgt_R","RDMETH_REC","RF_CESARN","WTGAIN"]
sub=[]
for var in train_columns:
    if var in null_columns:
        sub.append(train[str(var)][train[str(var)]!=dic[str(var)]])
    else:
        pass
print("완료5")
# 이상치 탐지
basic_re=pd.DataFrame()
for row in sub:
    basic_re=pd.concat([basic_re,row.describe()],axis=1)
fig1, axs1 = plt.subplots(nrows=7,ncols=6, figsize=(20, 15))
for i, data in enumerate(sub):
    axs1[i//6,i%6].hist(data)
sub3=[sub[2],sub[3],sub[4],sub[6],sub[7],sub[9],sub[10],sub[11],sub[14],sub[19],sub[20],sub[22],sub[23],sub[24],sub[27]]
fig2, axs2 = plt.subplots(nrows=5,ncols=3, figsize=(20, 15))
for i, var4 in enumerate(sub3):
    axs2[i//3,i%3].boxplot(var4)
print("완료6")
# 영향을 주는 이상치는 없는거 같음?
# 데이터 시각화
fig1, axs1 = plt.subplots(nrows=6,ncols=5, figsize=(20, 15))
plt.subplots_adjust(top=0.9, bottom=0.1, left=0.1, right=0.9, hspace=0.5, wspace=0.5)
for i, data in enumerate(sub):
    try:
        row, col = i // 5, i % 5
        sns.kdeplot(data,ax=axs1[row, col])
        axs1[row, col].set_title(f'{train_columns[i]}', size=14)
        axs1[row, col].set_xlabel(None)
    except Exception as e:
        pass
print("완료7")
# 타겟 데이터인 출생 무게와 비슷한 분포를 보이는 것은 BMI,FAGECOMB,M_Ht_In,PRECARE,PWgt_R,WTGAIN
# 미기재 및 누락의 개수 카운팅
dic={"ATTEND":9,"BFACIL":9,"BMI":99.9,"CIG_0":99,"DLMP_MM":99,"DMAR":" ","DOB_TT":9999,"FAGECOMB":99,"FEDUC":9,"ILLB_R":999,"ILOP_R":999,"ILP_R":999,"MBSTATE_REC":3,"MEDUC":9,"M_Ht_In":99,"NO_INFEC":9,"NO_MMORB":9,"PAY":9,"PAY_REC":9,"PRECARE":99,"PREVIS":99,"PRIORDEAD":99,"PRIORLIVE":99,"PRIORTERM":99,"PWgt_R":999,"RDMETH_REC":9,"RF_CESARN":99,"WTGAIN":99}
null_columns=["ATTEND","BFACIL","BMI","CIG_0","DLMP_MM","DMAR","DOB_TT","FAGECOMB","FEDUC","ILLB_R","ILOP_R","ILP_R","MBSTATE_REC","MEDUC","M_Ht_In","NO_INFEC","NO_MMORB","PAY","PAY_REC","PRECARE","PREVIS","PRIORDEAD","PRIORLIVE","PRIORTERM","PWgt_R","RDMETH_REC","RF_CESARN","WTGAIN"]
train_columns=train.columns.tolist()
null_count=[]
for var in train.iterrows():
    counter=0
    for var1,var2 in zip(var[1].index,var[1].values):
        if var1 in null_columns:
            if var2 == dic[str(var1)]:
                counter+=1
    null_count.append(counter)
train["Null_count"]=pd.Series(null_count)
corr=train.corr()
print("완료8")
# 특성 엔지니어링(누락값들 각 열 요소들의 비율을 확률로 랜덤 지정)
sub1=[]
total=[]
for var in sub:
    a1=var.value_counts()
    for var1 in a1:
        sub1.append(var1/a1.sum())
    total.append(sub1)
    sub1=[]
counter=0
def fun(x,y):
    if x == dic[str(var)]:
        return int(np.random.choice(sub[y].value_counts().index,size=1,p=total[y]))
    else:
        return x
for var in train:
    if str(var) in null_columns:
        train[str(var)]=train[str(var)].apply(lambda x:fun(x,counter))
        counter+=1
train["DMAR"]=train["DMAR"].apply(lambda x:int(x))
print("완료9")
# 문자형 자료 숫자로 바꾸기
string_data=["DMAR","LD_INDL","RF_CESAR","SEX"]
def fun(x,y,z):
    if x == dic[z]:
        return int(np.random.choice(sub[y].value_counts().index,size=1,p=total[y]))
    else:
        return x
def fun1(x):
    if x=="N":
        return 0
    elif x=="F":
        return 0
    else:
        return 1
train["LD_INDL"]=train["LD_INDL"].apply(lambda x:fun1(x))
train["RF_CESAR"]=train["RF_CESAR"].apply(lambda x:fun1(x))
train["SEX"]=train["SEX"].apply(lambda x:fun1(x))
print("완료10")
# 범주형 자료 값 더하기
Categorical_Data=["ATTEND","BFACIL","DMAR","FEDUC","LD_INDL","MBSTATE_REC","MEDUC","NO_INFEC","NO_MMORB","NO_RISKS","PAY","PAY_REC","RDMETH_REC","RESTATUS","RF_CESAR","RF_CESARN","SEX"]
Categorical_Sum=[]
for var in train.iterrows():
    C_sum=0
    for var1,var2 in zip(var[1].index,var[1].values):
        if var1 in Categorical_Data:
            C_sum+=var2
    Categorical_Sum.append(C_sum)
train["Categorical_Sum"]=pd.Series(Categorical_Sum)
print("완료11")
# 다른 코드에서 참고한 특성값 추가
def fe(df):
    df['approx_term'] = np.where(df['DLMP_MM'] != 99, df['DOB_MM'] - df['DLMP_MM'], 0)
    df['approx_term'] = np.where(df['approx_term'] < 0, df['approx_term'] + 12, df['approx_term'])
fe(train)
print("완료12")
# 훈련데이터 미숙, 평범, 우량으로 나눔
train_less=train[train["DBWT"]<2500]
train_normal=train[2500<=train["DBWT"]]
train_normal=train_normal[train_normal["DBWT"]<=3800]
train_over=train[train["DBWT"]>3800]           
less_corr=train_less.corr()
normal_corr=train_normal.corr()
over_corr=train_over.corr()
print("완료13")
# 다른 코드에서 참고한 kde plot 그리기
fig1, axs1 = plt.subplots(nrows=7, ncols=6, figsize=(25, 20),dpi=300)
plt.subplots_adjust(top=0.9, bottom=0.1, left=0.1, right=0.9, hspace=0.5, wspace=0.5)
for i, (less,normal,over) in enumerate(zip(train_less,train_normal,train_over)):
    try:
        row, col = i // 6, i % 6
        sns.kdeplot(train_less[str(less)], ax=axs1[row, col],color="r")
        sns.kdeplot(train_normal[str(normal)], ax=axs1[row, col],color="g")
        sns.kdeplot(train_over[str(over)], ax=axs1[row, col],color="b")
        axs1[row, col].set_title(f'{train_columns[i]}', size=14)
        axs1[row, col].set_xlabel(None)
    except Exception as e:
        pass
fig1.legend(["train_less","train_normal","train_over"])
plt.show() 
print("완료14")
# 확인해야 할 요소: ILLB_R,ILP_R,M_Ht_In,NO_INFEC,NO_MMORB,NO_RISKS,PAY,PREVIS,PRIORLIVE,RDMETH_REC,WTGAIN
# ATTEND(미숙아일수록 의사가 아이를 받은 비율이 높음)
a0=train_less["ATTEND"].value_counts()
b0=train_normal["ATTEND"].value_counts()
c0=train_over["ATTEND"].value_counts()
labels0=["1","2","3","4","5"]
title0=["less","normal","over"]
fig1, axs1 = plt.subplots(ncols=3, figsize=(12, 6))
for idx, var in enumerate([a0, b0, c0]):
    axs1[idx].pie(x=[var[1],var[2],var[3],var[4],var[5]], labels=labels0, autopct='%1.1f%%', startangle=90)
    axs1[idx].set_title(f'{title0[idx]}')
fig1.suptitle('ATTEND', fontsize=16)
plt.show()
print("완료15")
# ILLB_R,ILP_R(우량아 일수록 처음 낳는 비율이 줄음)
a1=train_less["ILP_R"].value_counts()
b1=train_normal["ILP_R"].value_counts()
c1=train_over['ILP_R'].value_counts()
labels1=["first", "not_first"]
title1=["less","normal","over"]
fig1, axs1 = plt.subplots(ncols=3, figsize=(12, 6))
for idx, var in enumerate([a1, b1, c1]):
    axs1[idx].pie(x=[var[888],var[3:300].sum()], labels=labels1, autopct='%1.1f%%', startangle=90)
    axs1[idx].set_title(f'{title1[idx]}')
fig1.suptitle('ILLB_R', fontsize=16)
plt.show()
print("완료16")
# MBSTATE_REC(큰 차이 없음)
a2=train_less["MBSTATE_REC"].value_counts()
b2=train_normal["MBSTATE_REC"].value_counts()
c2=train_over["MBSTATE_REC"].value_counts()
labels2=["America", "Foregin"]
title2=["less","normal","over"]
fig1, axs1 = plt.subplots(ncols=3, figsize=(12, 6))
for idx, var in enumerate([a2, b2, c2]):
    axs1[idx].pie(x=[var[1],var[2]], labels=labels2, autopct='%1.1f%%', startangle=90)
    axs1[idx].set_title(f'{title2[idx]}')
fig1.suptitle('MBSTATE_REC', fontsize=16)
plt.show()
print("완료17")
# M_Ht_In(차이 있을거 같았는데 큰 차이 없었음)
a3=train_less["M_Ht_In"].value_counts()
b3=train_normal["M_Ht_In"].value_counts()
c3=train_over["M_Ht_In"].value_counts()
plt.bar(x=c3.index,height=c3)
print("완료18")
# NO_INFEC(우량아 일수록 감염없는 사람의 비중이 줄긴하나 유의미 한지는 모르겠음)
a4=train_less["NO_INFEC"].value_counts()
b4=train_normal["NO_INFEC"].value_counts()
c4=train_over["NO_INFEC"].value_counts()
labels4=["False", "True"]
title4=["less","normal","over"]
fig1, axs1 = plt.subplots(ncols=3, figsize=(12, 6))
for idx, var in enumerate([a4, b4, c4]):
    axs1[idx].pie(x=[var[0],var[1]], labels=labels4, autopct='%1.1f%%', startangle=90)
    axs1[idx].set_title(f'{title4[idx]}')
fig1.suptitle('NO_INFEC', fontsize=16)
plt.show()
print("완료19")
# NO_MMORB(평범한 아이가 어머니가 감염 없는 경우가 더 많으나 유의미 한지는 모르겠음)
a5=train_less["NO_MMORB"].value_counts()
b5=train_normal["NO_MMORB"].value_counts()
c5=train_over["NO_MMORB"].value_counts()
labels5=["False", "True"]
title5=["less","normal","over"]
fig1, axs1 = plt.subplots(ncols=3, figsize=(12, 6))
for idx, var in enumerate([a5, b5, c5]):
    axs1[idx].pie(x=[var[0],var[1]], labels=labels5, autopct='%1.1f%%', startangle=90)
    axs1[idx].set_title(f'{title5[idx]}')
fig1.suptitle('NO_MMORB', fontsize=16)
plt.show()
print("완료20")
# NO_RISKS(미숙아가 리스크요소가 있는 비율이 더 많음)
a6=train_less["NO_RISKS"].value_counts()
b6=train_normal["NO_RISKS"].value_counts()
c6=train_over["NO_RISKS"].value_counts()
labels6=["False", "True"]
title6=["less","normal","over"]
fig1, axs1 = plt.subplots(ncols=3, figsize=(12, 6))
for idx, var in enumerate([a6, b6, c6]):
    axs1[idx].pie(x=[var[0],var[1]], labels=labels6, autopct='%1.1f%%', startangle=90)
    axs1[idx].set_title(f'{title6[idx]}')
fig1.suptitle('NO_RISKS', fontsize=16)
plt.show()
print("완료21")
# PAY(우량아 일수록 정부기반의 보험보다 사설보험과 자가지불의 비율이 증가함)
a7=train_less["PAY"].value_counts()
b7=train_normal["PAY"].value_counts()
c7=train_over["PAY"].value_counts()
labels7=["1","2","3","4","5","6","8"]
title7=["less","normal","over"]
fig1, axs1 = plt.subplots(ncols=3, figsize=(12, 6))
for idx, var in enumerate([a7, b7, c7]):
    axs1[idx].pie(x=[var[1],var[2],var[3],var[4],var[5],var[6],var[8]], labels=labels7, autopct='%1.1f%%', startangle=90)
    axs1[idx].set_title(f'{title7[idx]}')
fig1.suptitle('PAY', fontsize=16)
plt.show()
print("완료22")
# PREVIS(우량아 일수록 군집의 중심이 높음)
a8=train_less["PREVIS"].value_counts()
b8=train_normal["PREVIS"].value_counts()
c8=train_over["PREVIS"].value_counts()
plt.bar(x=a8.index,height=a8)
plt.bar(x=b8.index,height=b8)
plt.bar(x=c8.index,height=c8)
print("완료23")
# PRIORLIVE(우량아 일수록 생존 자녀 수가 있는 경우의 비율이 많음)
a9=train_less["PRIORLIVE"].value_counts()
b9=train_normal["PRIORLIVE"].value_counts()
c9=train_over["PRIORLIVE"].value_counts()
labels9=["0", "other"]
title9=["less","normal","over"]
fig1, axs1 = plt.subplots(ncols=3, figsize=(12, 6))
for idx, var in enumerate([a9, b9, c9]):
    axs1[idx].pie(x=[var[0],var[1:14].sum()], labels=labels9, autopct='%1.1f%%', startangle=90)
    axs1[idx].set_title(f'{title9[idx]}')
fig1.suptitle('PRIORLIVE', fontsize=16)
plt.show()
print("완료24")
# RDMETH_REC(미숙아가 제왕절개술의 비율이 더 높게 나옴, 그 다음은 우량아)
a10=train_less["RDMETH_REC"].value_counts()
b10=train_normal["RDMETH_REC"].value_counts()
c10=train_over["RDMETH_REC"].value_counts()
labels10=["1","2","3","4"]
title10=["less","normal","over"]
fig1, axs1 = plt.subplots(ncols=3, figsize=(12, 6))
for idx, var in enumerate([a10, b10, c10]):
    axs1[idx].pie(x=[var[1],var[2],var[3],var[4]], labels=labels10, autopct='%1.1f%%', startangle=90)
    axs1[idx].set_title(f'{title10[idx]}')
fig1.suptitle('RDMETH_REC', fontsize=16)
plt.show()
print("완료25")
# RESTATUS(미숙아가 주내 거주자 비율이 높음)
a11=train_less["RESTATUS"].value_counts()
b11=train_normal["RESTATUS"].value_counts()
c11=train_over["RESTATUS"].value_counts()
labels11=["1","2","3","4"]
title11=["less","normal","over"]
fig1, axs1 = plt.subplots(ncols=3, figsize=(12, 6))
for idx, var in enumerate([a11, b11, c11]):
    axs1[idx].pie(x=[var[1],var[2],var[3],var[4]], labels=labels11, autopct='%1.1f%%', startangle=90)
    axs1[idx].set_title(f'{title11[idx]}')
fig1.suptitle('RESTATUS', fontsize=16)
plt.show()
print("완료26")
# WTGAIN(큰 차이 없음, 굳이 따지면 우량아 일수록 군집의 중심이 높음)
a12=train_less["WTGAIN"].value_counts()
b12=train_normal["WTGAIN"].value_counts()
c12=train_over["WTGAIN"].value_counts()
plt.bar(x=a12.index,height=a12)
plt.bar(x=b12.index,height=b12)
plt.bar(x=c12.index,height=c12)
print("완료27")
# 그래프 없는거
# DMAR(우량아일수록 결혼 안함의 수가 적음)
labels13 = ["1", "2"]
title13=["less","normal","over"]
fig1, axs1 = plt.subplots(ncols=3, figsize=(12, 6))
data_counts_less = train_less["DMAR"].value_counts()
data_counts_normal = train_normal["DMAR"].value_counts()
data_counts_over = train_over["DMAR"].value_counts()
for idx, data_counts in enumerate([data_counts_less, data_counts_normal, data_counts_over]):
    axs1[idx].pie(data_counts, labels=labels13, autopct='%1.1f%%', startangle=90)
    axs1[idx].set_title(f'{title13[idx]}')
fig1.suptitle('DMAR', fontsize=16)
plt.show()
print("완료28")
# LD_INDL(우량아 일수록 분만 유도 비율이 큼)
labels14=["1", "2"]
title14=["less","normal","over"]
fig1, axs1 = plt.subplots(ncols=3, figsize=(12, 6))
data_counts_less = train_less["LD_INDL"].value_counts()
data_counts_normal = train_normal["LD_INDL"].value_counts()
data_counts_over = train_over["LD_INDL"].value_counts()
for idx, data_counts in enumerate([data_counts_less, data_counts_normal, data_counts_over]):
    axs1[idx].pie(data_counts, labels=labels14, autopct='%1.1f%%', startangle=90)
    axs1[idx].set_title(f'{title14[idx]}')
fig1.suptitle('LD_INDL', fontsize=16)
plt.show()
print("완료29")
# RF_CESAR(큰 차이 없음)
labels15=["1", "2"]
title15=["less","normal","over"]
fig1, axs1 = plt.subplots(ncols=3, figsize=(12, 6))
data_counts_less = train_less["RF_CESAR"].value_counts()
data_counts_normal = train_normal["RF_CESAR"].value_counts()
data_counts_over = train_over["RF_CESAR"].value_counts()
for idx, data_counts in enumerate([data_counts_less, data_counts_normal, data_counts_over]):
    axs1[idx].pie(data_counts, labels=labels15, autopct='%1.1f%%', startangle=90)
    axs1[idx].set_title(f'{title15[idx]}')
fig1.suptitle('RF_CESAR', fontsize=16)
plt.show()
print("완료30")
# SEX(우량아부분은 남자가 많음)
labels16=["1", "2"]
title16=["less","normal","over"]
fig1, axs1 = plt.subplots(ncols=3, figsize=(12, 6))
data_counts_less = train_less["SEX"].value_counts()
data_counts_normal = train_normal["SEX"].value_counts()
data_counts_over = train_over["SEX"].value_counts()
for idx, data_counts in enumerate([data_counts_less, data_counts_normal, data_counts_over]):
    axs1[idx].pie(data_counts, labels=labels16, autopct='%1.1f%%', startangle=90)
    axs1[idx].set_title(f'{title16[idx]}')
fig1.suptitle('SEX', fontsize=16)
plt.show()
print("완료31")
# 타겟 데이터인 출생 무게와 비슷한 분포를 보이는 것은 BMI,FAGECOMB,M_Ht_In,PRECARE,PWgt_R,WTGAIN
# 출생 무게 증가 영향 요인: ILLB_R,ILP_R,PAY,PREVIS,PRIORLIVE,DMAR,LD_INDL,SEX
# 출생 무게 감소 영향 요인: NO_RISKS, RDMETH_REC, ATTEND, RESTATUS
# 큰 차이 없음: M_Ht_In, WTGAIN, RF_CESAR,NO_INFEC,NO_MMORB, MBSTATE_REC, 그 외 나머지
# 사용할 요인:ATTEND,BMI,DMAR,FAGECOMB,ILLB_R,LD_INDL,M_Ht_In,NO_RISKS,PAY,PREVIS,PRIORLIVE,PWgt_R,RDMETH_REC,RESTATUS,SEX,WTGAIN
# 일단 사용할 요인들만으로 트레인 데이터 재구성
use_element=["ATTEND","BMI","DMAR","FAGECOMB","ILLB_R","LD_INDL","M_Ht_In","NO_RISKS","PAY","PREVIS","PRIORLIVE","PWgt_R","RDMETH_REC","RESTATUS","SEX","WTGAIN","approx_term","Categorical_Sum","DBWT"]
re_train=pd.DataFrame()
for var in use_element:
    re_train=pd.concat([re_train,train[str(var)]],axis=1)
re_train_corr=re_train.corr()
# 모델링 준비
X = re_train.copy()
y = X.pop('DBWT')
seed = 42
splits = 5
kf = KFold(random_state = seed, shuffle = True)
np.random.seed(seed) 
print("완료32")
# test값 재처리
test=pd.read_csv("./birth_test.csv")
test_columns=test.columns.tolist()
dic={"ATTEND":9,"BFACIL":9,"BMI":99.9,"CIG_0":99,"DLMP_MM":99,"DMAR":" ","DOB_TT":9999,"FAGECOMB":99,"FEDUC":9,"ILLB_R":999,"ILOP_R":999,"ILP_R":999,"MBSTATE_REC":3,"MEDUC":9,"M_Ht_In":99,"NO_INFEC":9,"NO_MMORB":9,"PAY":9,"PAY_REC":9,"PRECARE":99,"PREVIS":99,"PRIORDEAD":99,"PRIORLIVE":99,"PRIORTERM":99,"PWgt_R":999,"RDMETH_REC":9,"RF_CESARN":99,"WTGAIN":99}
null_columns=["ATTEND","BFACIL","BMI","CIG_0","DLMP_MM","DMAR","DOB_TT","FAGECOMB","FEDUC","ILLB_R","ILOP_R","ILP_R","MBSTATE_REC","MEDUC","M_Ht_In","NO_INFEC","NO_MMORB","PAY","PAY_REC","PRECARE","PREVIS","PRIORDEAD","PRIORLIVE","PRIORTERM","PWgt_R","RDMETH_REC","RF_CESARN","WTGAIN"]
sub=[]
for var in test_columns:
    if var in null_columns:
        sub.append(test[str(var)][test[str(var)]!=dic[str(var)]])
    else:
        pass
sub1=[]
total=[]
for var in sub:
    a1=var.value_counts()
    for var1 in a1:
        sub1.append(var1/a1.sum())
    total.append(sub1)
    sub1=[]
counter=0
def fun(x,y):
    if x == dic[str(var)]:
        return int(np.random.choice(sub[y].value_counts().index,size=1,p=total[y]))
    else:
        return x
for var in test:
    if str(var) in null_columns:
        test[str(var)]=test[str(var)].apply(lambda x:fun(x,counter))
        counter+=1
test["DMAR"]=test["DMAR"].apply(lambda x:int(x))
def fe(df):
    df['approx_term'] = np.where(df['DLMP_MM'] != 99, df['DOB_MM'] - df['DLMP_MM'], 0)
    df['approx_term'] = np.where(df['approx_term'] < 0, df['approx_term'] + 12, df['approx_term'])
fe(test)
def fun1(x):
    if x=="N":
        return 0
    elif x=="F":
        return 0
    else:
        return 1
test["LD_INDL"]=test["LD_INDL"].apply(lambda x:fun1(x))
test["RF_CESAR"]=test["RF_CESAR"].apply(lambda x:fun1(x))
test["SEX"]=test["SEX"].apply(lambda x:fun1(x))
Categorical_Data=["ATTEND","BFACIL","DMAR","FEDUC","LD_INDL","MBSTATE_REC","MEDUC","NO_INFEC","NO_MMORB","NO_RISKS","PAY","PAY_REC","RDMETH_REC","RESTATUS","RF_CESAR","RF_CESARN","SEX"]
Categorical_Sum=[]
for var in test.iterrows():
    C_sum=0
    for var1,var2 in zip(var[1].index,var[1].values):
        if var1 in Categorical_Data:
            C_sum+=var2
    Categorical_Sum.append(C_sum)
test["Categorical_Sum"]=pd.Series(Categorical_Sum)
use_element=["ATTEND","BMI","DMAR","FAGECOMB","ILLB_R","LD_INDL","M_Ht_In","NO_RISKS","PAY","PREVIS","PRIORLIVE","PWgt_R","RDMETH_REC","RESTATUS","SEX","WTGAIN","approx_term","Categorical_Sum","DBWT"]
re_test=pd.DataFrame()
for var in use_element:
    re_test=pd.concat([re_test,test[str(var)]],axis=1)
print("완료33")
# 모델 검증
def cross_val_score(estimator, cv = kf, label = ''):
    X = train.copy()
    y = X.pop('DBWT')
    #initiate prediction arrays and score lists
    val_predictions = np.zeros((len(X)))
    #train_predictions = np.zeros((len(sample)))
    coverages, val_scores = [], []
    #training model, predicting prognosis probability, and evaluating metrics
    for fold, (train_idx, val_idx) in enumerate(cv.split(X, y)):
        model = clone(estimator)
        #define train set
        X_train = X.iloc[train_idx].reset_index(drop = True)
        y_train = y.iloc[train_idx].reset_index(drop = True)
        #define validation set
        X_val = X.iloc[val_idx].reset_index(drop = True)
        y_val = y.iloc[val_idx].reset_index(drop = True)
        X_val_1, X_val_2, y_val_1, y_val_2 = train_test_split(X_val, y_val, random_state = seed, test_size = .5)
        #train model
        model.fit(X_train, y_train)
        cqr = MapieRegressor(model, cv = 'prefit')
        cqr.fit(X_val_1, y_val_1)
        _, val_preds_2 = cqr.predict(X_val_2, alpha = .1)
        cqr = MapieRegressor(model, cv = 'prefit')
        cqr.fit(X_val_2, y_val_2)
        _, val_preds_1 = cqr.predict(X_val_1, alpha = .1)
        #make predictions
        val_preds = np.zeros((len(X_val), 2))
        val_preds[X_val_1.index, 0] = val_preds_1[:, 0].flatten()
        val_preds[X_val_1.index, 1] = val_preds_1[:, 1].flatten()
        val_preds[X_val_2.index, 0] = val_preds_2[:, 0].flatten()
        val_preds[X_val_2.index, 1] = val_preds_2[:, 1].flatten()
        #evaluate model for a fold
        WIS, coverage = MWIS_metric.score(y_val, val_preds[:, 0], val_preds[:, 1], .1)
        #append model score for a fold to list
        val_scores.append(WIS)
        coverages.append(coverage * 100)
    print(f'Val Score: {np.mean(val_scores):.5f} ± {np.std(val_scores):.5f} | Coverage: {np.mean(coverages):.3f}% ± {np.std(coverages):.3f}% | {label}')
    return val_scores, coverages
print("완료34")
# 손실 함수
score_list = pd.DataFrame()
models = [
    ('LAD', LADRegression()),
    ('XGB', XGBRegressor(random_state = seed, objective = 'reg:absoluteerror')),
    ('LGB', LGBMRegressor(random_state = seed, objective = 'mae')),
    ('CB', CatBoostRegressor(random_state = seed, objective = 'MAE', verbose = 0)),
    ('GB', GradientBoostingRegressor(random_state = seed, loss = 'absolute_error')),
    ('HGB', HistGradientBoostingRegressor(random_state = seed, loss = 'absolute_error')),
]
for label, model in models:
    score_list[label], _ = cross_val_score(
        make_pipeline(OneHotEncoder(cols = re_test), model),
        label = label
    )
print("완료35")
# 예측 & 넣기
X_train, X_cal, y_train, y_cal = train_test_split(X, y, random_state = seed, test_size = .1)
model = make_pipeline(
    OneHotEncoder(cols = re_test),
    GradientBoostingRegressor(random_state = seed, loss = 'absolute_error')
).fit(X_train, y_train)
cqr = MapieRegressor(model, cv = 'prefit').fit(X_cal, y_cal)
submission = test.copy()
_, prediction = cqr.predict(re_test, alpha = .1)
sample['pi_lower'] = prediction[:, 0]
sample['pi_upper'] = prediction[:, 1]
sample[['pi_lower', 'pi_upper']].to_csv('submission.csv')
print("완료36")
print("all complte")
