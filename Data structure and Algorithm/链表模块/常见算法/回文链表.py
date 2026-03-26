# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def isPalindrome(self, head: Optional[ListNode]) -> bool:
        if not head or not head.next:
            return True
        
        slow = head
        fast = head
        while fast and fast.next: # 快慢指针这里一定要注意
            slow = slow.next
            fast = fast.next.next

        prev = None
        current = slow
        while current:
            new_node = current.next
            current.next = prev
            prev = current
            current = new_node

        left, right = head, prev
        while right: # 如何判断两个列表是否相等
            if left.val != right.val:
                return False
            left = left.next
            right = right.next

        return True