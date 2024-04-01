# 파일 열기 순서
# 1. import csv->객체 지정 후 open("파일 경로")
# 2. csv.reader(오픈 파일 객체)
# 3. 반복문으로 데이터 삽입(append사용)
# 일단 이거는 파일 경로만 설치된 경로로 바꿔서 실행 시켜 사용
import csv
temp = open("C:/Users/USER/Desktop/주간조 수업/데이터/temp.csv")
rdr = csv.reader(temp)
data3 = []
for var in rdr:
    data3.append(var)
# append문: 리스트에 요소들을 삽입 할 때 사용
# 넣고 싶은 리스트.append(넣을 대상)
# 예시
a=[1,2,3]
b=4
a.append(b)
print(a)
# 문제1: for문과 append를 사용해서 두 리스트의 요소들을 병합
# 결과물: [100,200,300,400,500,600]
data1 = [100, 200, 300]
data2 = [400, 500, 600]

#문제2: for문과 if문을 사용해서 a리스트에는 홀수만 b리스트에는 짝수만 넣기
c=[1,2,4,5,9,7,5,1,6,2,4,8,4,5,1,36,5,4,2,18,45,6,1,54,15,13,54,53,1,5,5,26,26,26,2,45,15,6,2,1,84,2,1,16]
a=[]
b=[]

# 문제3: data3을 반복문과 attend를 이용해서 일교차를 data2리스트에 추가
# data3은 아래 코드를 파일 경로만 바꿔서 실행 시켜서 사용
# 같다->==,같지 않다->!=
# 소수점 숫자로 변환==float()
data2=[]
import csv
temp = open("C:/Users/USER/Desktop/주간조 수업/데이터/temp.csv")
rdr = csv.reader(temp)
data3 = []
for var in rdr:
    data3.append(var)
