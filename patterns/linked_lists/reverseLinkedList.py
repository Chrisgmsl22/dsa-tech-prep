from utils.list_node import ListNode
from utils.list_builder import build_list
from utils.list_printer import printList
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def reverseList(self, head: ListNode) -> ListNode:
        arr = []
        res = ListNode(0) # This will be our final result
        r = res

        curr = head
        while curr:
            arr.append(curr.val)
            curr = curr.next
        
        while arr:
            currVal = arr.pop()
            print(currVal)
            res.next = ListNode(currVal)
            res = res.next
        
        return r.next
    
    def reverseList2(self, head: ListNode) -> ListNode:
        prev = None
        next = None
        curr = head
        # We need a prev (node behind me)
        # curr (curent node)
        # next node (node ahead, so we don't lose it when we reverse)
        # 1 -> 2 -> 3 -> None
        # next: 2
        # 
        while curr:
            print(curr.val)
            next = curr.next # We store what's next
            curr.next = prev    
            
            prev = curr
            curr = next
        
        return prev
        
sol = Solution()
head = build_list([1, 2, 3, 4, 5])

res = sol.reverseList2(head)
printList(res)



""" 
    NOTES:
    The point of this is to reverse a linked list.
    We need to keep in mind that a linked list only points forward, not backwards.
    (this is not a doubly linked list)
    Do we need to consider the idea of possibly creating a new linked list from scratch
    We need to traverse through it. But we also need to keep track of our current node.

    My first idea is to use an additional data structure, an array/stack, that can contain all the values stacked. We iterate again and pop the array each time, we create a node and link it. By the time we are done, we would have a new linked list but now reversed-

    But, should we really do this?, are we even allowed to do this?


"""