# 圣诞礼物

eps = 1e-6

class Candy:
    def __init__(self, v, w):
        self.v = v
        self.w = w
    def __lt__(self, other):
        return (self.v/self.w - other.v/other.w)>eps

n, w = list(map(int, input().split()))

candies = [Candy(0,0) for i in range(n)]
for i in range(n):
    candies[i].v, candies[i].w = list(map(float, input().split()))

candies.sort()
totalv = 0
totalw = 0
for i in range(n):
    if totalw + candies[i].w <= w:
        totalv += candies[i].v
        totalw += candies[i].w
    else:
        totalv += candies[i].v * (w - totalw)/candies[i].w # 搁不下一整箱了还可以换
        break

print('%.1f'%totalv)