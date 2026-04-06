# 仅设尾指针的循环链表
class CircleLinkList: 
# 在链表头部插入元素
# 在链表尾部插入元素
# 移除并返回链表头部元素
# 移除并返回链表尾部元素
# 打印链表中的所有元素
    class Node:
        def __init__(self, value):
            self.value = value
            self.next = None
    
    def __init__(self):
        self.tail = None
        self.size = 0
    
    def pushFront(self,value):
        node = CircleLinkList.Node(value)
        if self.tail == None:
            self.tail = node
            self.tail.next = node
        else:
            node.next = self.tail.next
            self.tail.next = node
        self.size +=1
    
    def pushBack(self, value):
        node = CircleLinkList.Node(value)
        if self.tail == None:
            self.tail = node
            self.tail.next = node
        else:
            node.next = self.tail.next
            self.tail.next = node
            self.tail = node
        self.size +=1
    
    def popFront(self):
        if self.tail == None:
            return
        else:
            value = self.tail.next.value
            self.tail.next = self.tail.next.next
            self.size -=1
            return value
    
    def popBack(self):
        if self.tail == None:
            return
        else:
            value = self.tail.value
            current = self.tail.next
            while current.next != self.tail:
                current = current.next
            current.next = self.tail.next
            self.tail = current
            self.size -=1
            return value
    def print(self):
        if self.size == 0:
            print('Empty!')
        else:
            current = self.tail.next
            while current:
                print(current.value, end = ",")
                current = current.next
                if current == self.tail.next:
                    break
        print()
    
if __name__ == "__main__":
    clist = CircleLinkList()

    print("Pushing elements to front:")
    for i in range(3):
        clist.pushFront(i)
        clist.print()  # 应该依次输出: 0, 1,0, 2,1,0,

    print("Pushing elements to back:")
    for i in range(3, 6):
        clist.pushBack(i)
        clist.print()  # 应该依次输出: 2,1,0,3, 2,1,0,3,4, 2,1,0,3,4,5,

    print("Popping from front:")
    for _ in range(3):
        print(f"Popped: {clist.popFront()}")
        clist.print()  # 应该依次输出: 2,1,0,3,4,5, 1,0,3,4,5, 0,3,4,5,

    print("Popping from back:")
    for _ in range(3):
        print(f"Popped: {clist.popBack()}")
        clist.print()  # 应该依次输出: 5, 3,4, 5, 4, 3, Empty!