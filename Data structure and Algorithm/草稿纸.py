# 最大上升子列

n = int(input())
maxLen = [1 for i in range(n+10)]
a = list(map(int, input().split()))
for i in range(n):
    for j in range(0,i):
        if a[i] > a[j]:
            maxLen[i] = max(maxLen[j]+1, maxLen[i])
print(max(maxLen))