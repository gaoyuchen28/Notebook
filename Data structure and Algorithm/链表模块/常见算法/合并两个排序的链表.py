def merge_sorted_lists(l1, l2):
    dummy = Node(0) # 为新链表建立了一个头节点
    tail = dummy
    while l1 and l2: #两个序列都还没有被遍历
        if l1.data < l2.data:
            tail.next = l1
            l1 = l1.next
        else:
            tail.next = l2
            l2 = l2.next
        tail = tail.next #tail也需要不断向后呀
    
    if l1:
        tail.next = l1
    else:
        tail.next = l2
    return dummy.next # 返回的是列表的头节点