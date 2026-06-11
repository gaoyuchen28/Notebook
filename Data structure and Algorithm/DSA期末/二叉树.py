while True:
    n,m = map(int, input().split())
    if n==0 and m==0:
        break
    ans =0
    right = n
    left = n
    while left <= m:
        ans += min(m, right) - left + 1
        right = right*2 + 1
        left = left*2
    print(ans)
