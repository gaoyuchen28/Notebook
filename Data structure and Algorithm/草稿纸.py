# 电影节

class Movie:
    def __init__(self, s, e):
        self.s = s
        self.e = e
    def __lt__(self, other):
        return self.e < other.e

n = int(input())
mov = [Movie(0,0) for i in range (n)]
for i in range(n):
    mov[i].s , mov[i].e = list(map(int, input().split()))

mov.sort()
result = 1
e = mov[0].e
for i in range(n):
    if mov[i].s >= e:
        result += 1
        e = mov[i].e

print(result)