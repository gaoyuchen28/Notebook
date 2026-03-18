class CircleLinkList:
    class Node:
        def __init__(self, data, next=None):
            self.data = data
            self.next = next
    
    def __init__(self):
        self.tail = None #循环链表没有head
        self.size = 0
    
    def is_empty(self): # 检查链表是否为空
        return self.size==0
    
    def pushFront(self, data): # 在链表头部插入元素
        nd = CircleLinkList.Node(data)
        if self.size ==0:
            self.tail = nd
            nd.next = self.tail
        else:
            nd.next = self.tail.next # 这里的逻辑有点困难，必须先保存原来的head指针，再修改tail的指向
            self.tail.next = nd
        self.size += 1

    def pushBack(self, data): # 在链表尾部插入元素
        nd = CircleLinkList.Node(data)
        if self.size ==0:
            self.tail = nd
        else:
            nd.next = self.tail.next
            self.tail.next = nd # 当前尾节点指向新节点
            self.tail = nd
        self.size +=1
    
    def popFront(self): # 移除并返回链表头部元素
        if self.is_empty():
            return None
        else:
            p = self.tail.next
            if self.size ==1:
                self.tail = 0
            else:
                self.tail.next = p.next
            self.size -= 1
            return p.data
    
    def popBack(self): # 移除并返回链表尾部元素
        if self.is_empty():
            return None
        else:
            p = self.tail
            if self.size ==1:
                self.tail = None
                self.size -= 1
                return p.data
            else:
                while p.next != self.tail:
                    p = p.next
                data = p.next.data
                p.next = self.tail.next
                self.tail = p
                self.size -= 1
                return data

    def printList(self): # 打印链表中的所有元素
        if self.is_empty():
            print('Empty!')
        else:
            ptr = self.tail.next
            while True:
                print(ptr.data, end=', ' if ptr != self.tail else '\n')
                if ptr == self.tail:
                    break
                ptr = ptr.next

if __name__ == "__main__":
    clist = CircleLinkList()

    print("Pushing elements to front:")
    for i in range(3):
        clist.pushFront(i)
        clist.printList()  # 应该依次输出: 0, 1,0, 2,1,0,

    print("Pushing elements to back:")
    for i in range(3, 6):
        clist.pushBack(i)
        clist.printList()  # 应该依次输出: 2,1,0,3, 2,1,0,3,4, 2,1,0,3,4,5,

    print("Popping from front:")
    for _ in range(3):
        print(f"Popped: {clist.popFront()}")
        clist.printList()  # 应该依次输出: 2,1,0,3,4,5, 1,0,3,4,5, 0,3,4,5,

    print("Popping from back:")
    for _ in range(3):
        print(f"Popped: {clist.popBack()}")
        clist.printList()  # 应该依次输出: 5, 3,4, 5, 4, 3, Empty!