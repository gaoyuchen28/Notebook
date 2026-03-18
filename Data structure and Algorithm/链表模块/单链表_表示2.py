# 基础结构
class linkedlist:
    class Node:
        def __init__(self,data,next=None): #这里的初始定义很重要，这里是默认了next是none
            self.data = data
            self.next = next
    
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0
    # 添加操作
    def pushFront(self, data):
        nd = linkedlist.Node(data,self.head) #这里强制认为next就是self.head
        self.head = nd
        if self.size == 0: #这里的if是为了定义tail！！
            self.tail = nd #每个函数都要考虑到对于尾的判断
        self.size +=1
    def insert_after(self, p, data):
        nd = linkedlist.Node(data)
        if p is None:
            self.pushFront(data)
        else:
            nd.next = p.next
            p.next = nd
            if p == self.tail: #每个函数都要考虑到对于尾的判断
                self.tail = nd
        self.size+=1
    def pushBack(self, data):
        if self.size == 0:
            self.pushFront(data)
        else:
            self.insert_after(self.tail, data)
    
    # 删除操作
    def popFront(self):
        if self.head is None:
            raise Exception("Popping front from empty link list.")
        else:
            data = self.head.data # 要记录pop出去的数是什么
            self.head = self.head.next
            self.size -=1
            if self.size ==0: #每个函数都要考虑到对于尾的判断
                self.tail = None
            return data
    def delete_after(self, p):
        if p is None or p.next is None:
            return
        if self.tail is p.next:  # 如果被拆的那节正好是车尾
            self.tail = p #每个函数都要考虑到对于尾的判断
        p.next = p.next.next
        self.size -=1
    def print(self):
        p = self.head
        while p is not None:
            if p!= self.head:
                print(",",end='')
            print(p.data, end='')
            p = p.next
        print()
if __name__ == "__main__":
    ll = linkedlist()
    ll.pushFront(1)
    ll.pushFront(2)
    ll.pushBack(3)
    ll.print()  # 应该输出: 2,1,3
    ll.delete_after(ll.head)  # 删除第二个元素 (1)
    ll.print()  # 应该输出: 2,3
    print(f"Pop Front: {ll.popFront()}")  # 应该输出: Pop Front: 2
    ll.print()  # 应该输出: 3