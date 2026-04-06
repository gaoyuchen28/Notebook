# 链表反转（Reverse Linked List）

def reverse(head):
    current = head
    prev = None
    while current:
        node = current.next
        current.next = prev
        prev = current
        current = node
    return prev