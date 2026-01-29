from utils.list_node import ListNode
from utils.list_builder import build_list
from utils.list_printer import printList
# When working with linked lists, always import these 



# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def deleteDuplicates(self, head: ListNode) -> ListNode:
        originalHead = head # We will return this at the end
        curr = head # Fresh "copy"

        while curr: # Traverse
            # Process node here
            currVal = curr.val
            print("Current node: ", currVal)
            if curr.next and currVal == curr.next.val:
                if curr.next.next is None:
                    print("Tail is duplicate")
                    # If duplicate is tail, disconnect from tail
                    curr.next = None 
                # While our next value is a duplicate, keep going
                while curr.next and currVal == curr.next.val:

                    print("Duplicate found: ", curr.next.val)
                    # next arrow points two nodes in advance
                    curr.next = curr.next.next

            # Continue
            curr = curr.next
        
        return originalHead
    
    def deleteDuplicatesClean(self, head: ListNode) -> ListNode:
        res = head

        curr = head
        while curr: # As long as there is a node, lets traverse
            while curr.next and curr.val == curr.next.val:
                # We found a duplicate, lets connect skip it
                curr.next = curr.next.next
            
            curr = curr.next # Let's go forward
        
        return res
    
    def deleteDuplicates3(self, head: ListNode) -> ListNode:
        res = head

        curr = head
        while curr:
            if curr.next and curr.val == curr.next.val:
                # If there's a duplicate, skip it
                curr.next = curr.next.next
            else:
                # No duplicate, traverse
                curr = curr.next
        return res


# 1 -> 1 -> 1 -> 1 -> 1 -> None
# 1

sol = Solution()
head = build_list([1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 3, 4, 5])

printList(head)
resultAfterOperation = sol.deleteDuplicates3(head)
print("Res: ")
printList(resultAfterOperation)