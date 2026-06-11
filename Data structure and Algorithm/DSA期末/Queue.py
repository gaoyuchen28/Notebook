# 队列的特点就是先进先出。
# 对于一个元素 i 进队列，我们定义为 + i ，对于一个元素 i 出队列，我们定义为 - i ，
# 由此我们可以把对队列的操作翻译为一个序列，我们定义为队列序列。
# 对于"+1 -1 +2 +3 -2 +4"的操作，最后队列中保留两个元素3和4。
# 现在我们给出你一个个队列序列，请告诉我们这些是不是合法的队列序列。

# 首先第一行为一个整数T代表样例的数目。
# 对于每个样例，第一行为整数n，代表序列中有n个操作。
# 第二行会有n个空格隔开的，格式为" +i "或者" -i "的操作，保证 i 不小于0。

class Queue:
    def __init__(self):
        self.item = []
    
    def is_empty(self):
        return self.item == []

    def enqueue(self, item):
        self.item.insert(0, item)
    
    def dequeue(self):
        return self.item.pop()
    
    def size(self):
        return len(self.item)
    
    def not_contains(self, item):
        for i in range(self.size()):
            if item == self.item[i]:
                return False  
        return True         

n = int(input())
for i in range(n):
    valid = 1
    s = Queue()
    m = int(input())
    Symbol = input().split()
    for p in range(m):
        if Symbol[p][0] == "+":
            s.enqueue(Symbol[p][1:])
        elif Symbol[p][0] == "-":
            if s.is_empty() or s.not_contains(Symbol[p][1:]):
                print(f"Case {i+1}: no")
                valid = 0
                break
            s.dequeue()
    if valid == 1:
        print(f"Case {i+1}: yes")