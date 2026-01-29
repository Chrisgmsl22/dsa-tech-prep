from utils.list_node import ListNode
from utils.list_builder import build_list
from utils.list_printer import printList
# When working with linked lists, always import these 

head = build_list([1, 2, 3, 4, 5])

printList(head)

def traverseLinkedListRec(head: ListNode) -> list[int]:
    res = []

    # Lets do this recursively
    def rec(h: ListNode):
        if h is None:
            return
        
        res.append(h.val)
        return rec(h.next)
    
    rec(head)
    return res

def traverseLinkedlist(head: ListNode) -> list[int]:
    res = []

    while head:
        res.append(head.val)
        head = head.next
    
    return res

#print(f"Result after calling my function: {traverseLinkedListRec(head)}")
print(f"Iterative approach: {traverseLinkedlist(head)}")