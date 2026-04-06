# 单向链表实现1：尾插法
class Node:
    def __init__(self, value): # 简单说就是Node其实就包括value和next两个部分
        self.value = value
        self.next = None

class LinkedList: #需要包括插入、删除、print三个功能
    def __init__(self): # LinkedList 表示整个链表结构，self.head 是链表的入口，指向链表的第一个节点（head node）
        self.head = None
    
    def insert(self, value):
        node = Node(value)
        if self.head == None:
            self.head = node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = node

    def delete(self, value):
        if self.head == None:
            return
        else:
            current = self.head
            while current.next:
                if current.next.value == value:
                    break
                current = current.next
            if current == None:
                return
            else:
                current.next = current.next.next
    def display(self): # 输出模块的判断
        current = self.head
        while current:
            print(current.value, end = " ")
            current = current.next
        print()

linked_list = LinkedList()
linked_list.insert(1)
linked_list.insert(2)
linked_list.insert(3)
linked_list.display()  # 输出：1 2 3
linked_list.delete(2)
linked_list.display()