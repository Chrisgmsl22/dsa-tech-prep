from utils.list_node import ListNode
from utils.list_builder import build_list
from utils.list_printer import printList

# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def mergeTwoLists(self, list1: ListNode, list2: ListNode) -> [ListNode]:
        dummy = ListNode(0)
        tail = dummy
        
        while list1 and list2:
            if list1.val <= list2.val: # l1 is the smaller one
                tail.next = list1
                list1 = list1.next
            else:
                tail.next = list2
                list2 = list2.next
            tail = tail.next # Dont forget to advance the tail
        if list1: # it we still have this, them append the rest to the tail
            tail.next = list1
        if list2:
            tail.next = list2

        return dummy.next
                
        

sol = Solution()
list1 = build_list([1, 2, 4])
list2 = build_list([1, 3, 4])

res = sol.mergeTwoLists(list1, list2)
printList(res)


"""
    NOTES:
    - Input: 2 heards for two SORTED (ASC) singly linked lists
    - Output: A head, which represents the 2 given linked lists merged into 1 while keeping the original ASC order.
    - Assumptions: Are our linked lists going to have the same length?, are our linked lists always going to be sorted?, our result needs to be sorted as well?. How do we handle repeated values within the list.

    We need to look at our lists. We need to be able to iterate through both. I feel like this can be similar to another problem where we merged two sorted arrays. So lets assume the length of the heads is not always the same. We iterate over the smallest to avoid overflow.

    Then, we need to compare both values, I have a feeling we might need a new linked list to be created, and that is where we might connect our two heads.

    Once we are done, our heads 1 and 2 will now be pointing to the new head 3.
    Also, lets consider how we should deal with the remaining vals of a linked list thats larger. We should ideally simply append the rest to the constructed list

"""