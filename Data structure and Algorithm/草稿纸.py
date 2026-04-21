# 数字三角形_递归+函数值储存

n = int(input())
D = []
maxSum = [[-1 for j in range(i+1)] for i in range(n)]
def Maxsum(i, j):
    if i == n-1:
        return D[i][j]
    if maxSum[i][j] != -1:
        return maxSum[i][j]
    x = Maxsum(i+1,j)
    y = Maxsum(i+1,j+1)
    maxSum[i][j] = max(x,y)+D[i][j]
    return maxSum[i][j]

for i in range(n):
    lst = list(map(int,input().split()))
    D.append(lst)

print(Maxsum(0,0))