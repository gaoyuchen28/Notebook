# Sort the Queue
def Findmin(n):
    if len(n) == 1:
        c.append(n[0])
        return
    else:
        for i in range(len(n)):
            if n[0] > n[i]:
                n[0], n[i] = n[i], n[0]
        Findmin(n[1:])
        c.append(n[0])
        return

c = []
n = list(map(int, input().split(", ")))
Findmin(n)
print(c)