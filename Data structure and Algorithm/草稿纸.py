# 铺瓷砖问题

n = int(input())
num = {0:1, 1:1, 2:2, 3:4, 4:8}

def total(n):
    if n <= 4:
        return num[n]
    else:
        for i in range(5, n+1):
            num[i] = num[i-1] + num[i-2] + num[i-3] + num[i-4]
        return num[n]

print(total(n))