# 单向列表实验二：维护了tail和size
class LinkList: 
# 功能包括：
# 打印、
# 在链表头部插入、
# 在链表尾部插入、
# 在节点p后插入、
# 删除节点 p 后的节点、
# 删除头节点并返回数据、
    class Node:
        def __init__(self, value):
            self.value = value
            self.next = None
    
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    def print(self):
        if self.size == 0:
            return
        current = self.head
        while current:
            print(current.value, end = " ")
            current = current.next
        print()
    
    def pushFront(self, value):
        node = LinkList.Node(value)
        if self.size == 0:
            self.head = node
            self.tail = node
        else:
            p = self.head
            self.head = node
            node.next = p
        self.size += 1
    
    def pushBack(self, value):
        node = LinkList.Node(value)
        if self.size == 0:
            self.head = node
            self.tail = node
        else:
            self.insert_after(self.tail, value)
        self.size += 1
    
    def insert_after(self, p, value):# If p is None, insert at the beginning
        node = LinkList.Node(value)
        if p is None:
            self.pushFront(value)
        else:
            if p == self.tail:
                p.next = node
                self.tail = node
            else:
                node.next = p.next
                p.next = node
        self.size += 1
    
    def delete_after(self,p):
        if p is None or p.next is None:
            return
        else:
            if p.next == self.tail:
                self.tail = p
            else:
                p.next = p.next.next
            self.size -= 1
    
    def popFront(self):
        if self.size == 0:
            self.tail = None
        else:
            value = self.head.value
            self.head = self.head.next
            self.size -= 1
            return value
        
if __name__ == "__main__":
    ll = LinkList()
    ll.pushFront(1)
    ll.pushFront(2)
    ll.pushBack(3)
    ll.print()  # 应该输出: 2,1,3
    ll.delete_after(ll.head)  # 删除第二个元素 (1)
    ll.print()  # 应该输出: 2,3
    print(f"Pop Front: {ll.popFront()}")  # 应该输出: Pop Front: 2
    ll.print()  # 应该输出: 3