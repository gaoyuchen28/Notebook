def find_middle_node(head):
    slow = fast = head
    while fast:
        fast = fast.next.next
        slow = slow.next
    return slow