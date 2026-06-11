class BinHeap:
    def __init__(self):
        self.heaplist = [0]
        self.size = 0
    def percUp(self, i):
        while i//2 > 0:
            if self.heaplist[i] < self.heaplist[i//2]:
                self.heaplist[i], self.heaplist[i//2] = self.heaplist[i//2], self.heaplist[i]
            i = i//2
    def insert(self, k):
        self.heaplist.append(k)
        self.size += 1
        self.percUp(self.size)
    def FindMin(self,i):
        if i*2+1>self.size:
            return i*2
        else:
            if self.heaplist[i*2] < self.heaplist[i*2+1]:
                return i*2
            else:
                return i*2+1
    def percDown(self,i):
        while i*2 <= self.size:
            mc = self.FindMin(i)
            if self.heaplist[i] > self.heaplist[mc]:
                self.heaplist[i], self.heaplist[mc] = self.heaplist[mc], self.heaplist[i]
            i = mc
    def delMin(self):
        val = self.heaplist[1]
        self.heaplist[1] = self.heaplist[self.size] # 注意这里size和实际队列长度的区别
        self.size -= 1
        self.heaplist.pop()
        self.percDown(1) # 这里是要往下沉的所以是1
        return val
    
t = int(input())

while t:
    hp = BinHeap()
    n = int(input())

    while n:
        op = list(map(int, input().split()))

        if op[0] == 1:
            hp.insert(op[1])
        else:
            print(hp.delMin())

        n -= 1

    t -= 1