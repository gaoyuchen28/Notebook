# 程序填空

class Node:
	def __init__(self, data, next=None):
		self.data, self.next = data, next
class LinkList:  #循环链表
	def __init__(self):
		self.tail = None
		self.size = 0
	def isEmpty(self):
		return self.size == 0
	def pushFront(self,data): # 在链表头部插入元素
		nd = Node(data)
		if self.tail == None:
			self.tail = nd
			nd.next = self.tail
		else:
			nd.next = self.tail.next
			self.tail.next = nd
		self.size += 1
	def pushBack(self,data): # 在链表尾部插入元素
		self.pushFront(data)
		self.tail = self.tail.next
	def popFront(self): # 移除并返回链表头部元素
		if self.size == 0:
			return None
		else:
			nd = self.tail.next
			self.size -= 1
			if self.size == 0:
				self.tail = None
			else:
				self.tail.next = nd.next
		return nd.data
	def printList(self):
		if self.size > 0:
			ptr = self.tail.next
			while True:
				print(ptr.data,end = " ")
				if ptr == self.tail:
					break
				ptr = ptr.next
			print("")
	def remove(self,data): # 从循环链表中删除数据
		if self.size != 0:
			nd = self.tail
			while nd.next.data != data:
				nd = nd.next
				if nd == self.tail:
					return False
			if nd.next == self.tail:
				self.tail = nd # 这就是为什么我们通过nd.next来寻找，这样可以保留尾节点的调整空间
			nd.next = nd.next.next
			self.size -= 1
			return True		
		else:
			return None
			
# 补充代码结束
t = int(input())
for i in range(t):
	lst = list(map(int,input().split()))
	lkList = LinkList()
	for x in lst:
		lkList.pushBack(x)
	lst = list(map(int,input().split()))
	for a in lst:
		result = lkList.remove(a)
		if result == True:
			lkList.printList()
		elif result == False:
			print("NOT FOUND")
		else:
			print("EMPTY")
	print("----------------")