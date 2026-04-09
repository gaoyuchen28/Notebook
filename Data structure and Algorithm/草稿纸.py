# 例题: Swap Nodes in Pairs


# Definition for singly-linked list.
class ListNode:
    def __init__(self, val):
        self.val = val
        self.next = None


class Solution:
    def __init__(self):
        self.head = None

    def swapPairs(self, head):
        """
        :type head: Optional[ListNode]
        :rtype: Optional[ListNode]
        """
        # 改正1: 递归终止条件要同时处理空链表和只剩一个节点的情况
        if head is None or head.next is None:
            return head

        first = head
        second = head.next

        # 改正2: 先递归处理后面的链表，再把结果接回当前这一对节点
        first.next = self.swapPairs(second.next)

        # 改正3: 交换当前两个节点
        second.next = first

        # 改正4: 返回交换后的新头结点，也就是原来的第二个节点
        return second

    def insert(self, data):
        nd = ListNode(data)

        # 改正5: 插入节点时要真正接到 self.head 这条链表上
        if self.head is None:
            self.head = nd
            return

        current = self.head
        while current.next:
            current = current.next
        current.next = nd

    def prints(self):
        current = self.head
        values = []
        while current:
            # 改正6: 打印节点的值，而不是直接打印节点对象
            values.append(str(current.val))
            current = current.next
        print(" -> ".join(values))


# 改正7: 这里要创建 Solution 的实例，而不是直接把类名赋值给变量
sol = Solution()

# 改正8: 读入形如 1,2,3,4 的序列，并逐个插入链表
nums = list(map(int, input().split(",")))
for num in nums:
    sol.insert(num)

# 改正9: 交换后要把返回的新头结点重新赋值给 sol.head
sol.head = sol.swapPairs(sol.head)

sol.prints()
