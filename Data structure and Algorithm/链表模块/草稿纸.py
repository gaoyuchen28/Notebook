# 斐波那契数列

def Fib(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return Fib(n-1) + Fib(n-2)

n = int(input())
data = []
for i in range(n):
    data.append(Fib(i)) # 用append！！！

for num in data:
    print(num, end = " ")