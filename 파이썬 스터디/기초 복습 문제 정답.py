# 1번 문제 정답
list_1=["135794-1597532","249751-2567485","976415-1674982","967512-2254984","669452-1154985","794625-2687519","994672-1532648","123456-2465845","624578-1549758","987456-225468"]
for var in list_1:
    if var[7] == "1":
        print("남자")
    else:
        print("여자")
# 2번 문제 정답
list_2=["aa_1123_ddf", "b_445_yyyyu", "ide_998_uqnc"]
for row in list_2:
    temp1 = row.find("_")
    temp2 = row[temp1+1:].find("_")
    print(row[temp1+1:(temp1-1)+(temp2+2)])
# 3번 문제 정답
list_3=[4, 1, 2, 10, 7, 3]
size = len(list_3)
for var in range(1, size):
    for var1 in range(var, 0, -1):
        if list_3[var1] < list_3[var1 - 1]:
            list_3[var1], list_3[var1 - 1] = list_3[var1 - 1], list_3[var1]
        else:
            break
    print(list_3)