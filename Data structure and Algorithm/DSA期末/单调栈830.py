# 给定一个长度为 N 的整数数列，输出每个数左边第一个比它小的数，如果不存在则输出 -1。

# 数据范围
# 1≤N≤10^5
# 1≤数列中元素≤10^9


# 思路真的很重要！！！！

num = int(input())
s = []
s = list(map(int,input().split( )))

stack = []
for p in s:
    while stack and stack[-1]>=p:
        stack.pop()
    if stack:
        print(stack[-1],end=' ')
    else:
        print(-1,end=' ')
    stack.append(p)
