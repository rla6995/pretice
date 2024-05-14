# 코딩 구몬
# 다음 파일을 다운로드 후 지정된 경로를 써 넣어서 파일 열기
import csv
# 괄호 안에 파일의 경로를 넣으면 된다
temp = open("C:/Users/USER/Desktop/김태진/데이터/subway.csv")
rdr = csv.reader(temp)
data1 = []
for var in rdr:
    data1.append(var)
# enumerate()의 사용법
# for enumerate변수,대상변수 in enumerate(대상):
#   반복문 돌릴 조건
# enumerate변수가 0부터 대상의 개수만큼 1씩 증가
# 예시문
a=[1,2,3,4,5,5,6,6,7,8,5,5,77,4,2,1]
for idx,var in enumerate(a):
    print(idx)
# 결과물: 0123456789101112131415
# 중복제거 함수: set()
# 예시문
set(a)
# 결과: {1, 2, 3, 4, 5, 6, 7, 8, 77}

# 리스트에 특정 문자 넣기
# 객체=[0]*개수
# 예시문
re = [0]*48
#결과: re에 48개의 0이 들어감

# 다음 파일을 서울 지하철의 시간대별 승 하차 인원에 대한 파일이다
# 다음에 제시되는 문제들을 풀어보시오

# 1번 문제: 7~9시에 하차 인원이 가장 많이 발생한 역은?
low = -999
for idx, var in enumerate(data1[2:]):
    if low < int(var[13].replace(",", "")) + int(var[11].replace(",", "")):
        low = int(var[13].replace(",", "")) + int(var[11].replace(",", ""))
        idx_flag = idx
        
print(low)
print(data1[idx_flag+2][3])

# 2번 문제: 역별 7시~9시의 승차 인원과 하차 인원을 추출해보시오

total = []
sub = []
for var in data1[2:]:
    sub = []
    sub.append(var[3])
    sub.append(int(var[10].replace(",", "")) + int(var[12].replace(",", "")))
    sub.append(int(var[11].replace(",", "")) + int(var[13].replace(",", "")))
    total.append(sub)

# 3번 문제: 각 호선별 시간대 승,하차 인원의 시간대별 값 
# ex) [[1호선, 4시승차, 4시하차, .......], [2호선, 4시승차, 4시하차,........]

sub_number = []
for var in data1[2:]:
    sub_number.append(var[1])
sub_number = list(set(sub_number))
sub_number.sort()
total = []
re = [0]*48
for var in sub_number:
    for var1 in data1[2:]:
        if var in var1:
            for idx, var2 in enumerate(var1[4:52]):
                re[idx] += int(var2.replace(",", ""))
    re.insert(0, var)
    total.append(re)
    re = [0] * 48


