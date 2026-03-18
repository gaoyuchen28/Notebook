def reverse_linked_list(head):
    prev = None
    current = head
    while current:
        new_node = current.next
        current.next = prev
        prev = current
        current = new_node
    return prev
        