# 链表合并

def merge_sorted_lists(l1, l2):
    dummy = Node(0)
    tail = dummy
    while l1 and l2:
        if l1.data > l2.data:
            tail.next = l1
            l1 = l1.next
        else:
            tail.next = l2
            l2 = l2.next
    if l1:
        tail.next = l1
    else:
        tail.next = l2
    return dummy.next