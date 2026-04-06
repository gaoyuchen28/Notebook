# 双向列表实现
class Node:
    def __init__(self, value):
        self.value = value
        self.next = None
        self.prev = None

class DoublyLinkedList:
# 在链表尾部添加节点
# 在链表头部添加节点
# 删除链表中的指定节点
# 打印链表中的所有元素，从头到尾
# 打印链表中的所有元素，从尾到头
    def __init__(self):
        self.head = None
        self.tail = None
    
    def append(self, value):
        node = Node(value)
        if self.head == None:
            self.head = node
            self.tail = node
        else:
            self.tail.next = node
            node.prev = self.tail
            self.tail = node
    
    def prepend(self, value):
        node = Node(value)
        if self.head == None:
            self.head = node
            self.tail = node
        else:
            node.next = self.head
            self.head.prev = node
            self.head = node
        
    def delete(self, p):
        if p is None:
            return
        if p == self.tail:
            self.tail = self.tail.prev
            self.tail.next = None
        else:
            p.prev.next = p.next
            p.next.prev = p.prev
    
    def print_list(self):
        current = self.head
        while current:
            print(current.value, end = "<->")
            current = current.next
        print("None")
    
    def print_reverse(self):
        current = self.tail
        while current:
            print(current.value, end="<->")
            current = current.prev
        print("None")
    
dll = DoublyLinkedList()

# 添加节点
dll.append(10)
dll.append(20)
dll.append(30)

# 在头部添加节点
dll.prepend(5)

# 打印链表
print("从头到尾打印：")
dll.print_list()    # 5 <-> 10 <-> 20 <-> 30 <-> None

# 打印链表（逆序）
print("从尾到头打印：")
dll.print_reverse() # 30 <-> 20 <-> 10 <-> 5 <-> None

# 删除节点
dll.delete(dll.head.next)  # 删除第二个节点（数据为10）

# 打印链表
print("删除一个节点后，链表为：")   
dll.print_list()    # 5 <-> 20 <-> 30 <-> None