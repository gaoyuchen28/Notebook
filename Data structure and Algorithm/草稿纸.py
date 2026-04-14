# N皇后问题

def isok(n, pos):
    for i in range(n):
        if result[i] == pos or abs(i - n) == abs(result[i] - pos):
            return False
    
    return True

def queen(N, m):
    if N == m:
        for i in range(N):
            print(result[i], end = " ")
        print(" ")
        return True
    else:
        succeed = False
        for i in range(N):
            if isok(m,i):
                result[m]=i
                succeed = queen(N, m+1) or succeed
        return succeed


n = int(input())
result = [-1]*n
queen(n, 0)
print()