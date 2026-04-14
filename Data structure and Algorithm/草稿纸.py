# 斐波那契数优化


def Fib(n):
    if n == 0:
        return 0
    if n == 1 or n == 2:
        return 1
    elif Fib_res[n] >= 0:
        return Fib_res[n]
    else:
        Fib_res[n-1] = Fib(n-1)
        Fib_res[n-2] = Fib(n-2)
        return Fib_res[n-1] + Fib_res[n-2]

n = int(input())
Fib_res = [-1]*(n+1)
for i in range(n):
    print(Fib(i), end = " ")