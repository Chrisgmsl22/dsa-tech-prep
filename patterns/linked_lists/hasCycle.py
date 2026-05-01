from utils.list_node import ListNode
from utils.list_builder import build_list
from utils.list_printer import printList

# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, x):
#         self.val = x
#         self.next = None

class Solution:
    def hasCycle(self, head: ListNode) -> bool:
        seen = set()

        curr = head
        while curr:
            if curr in seen:
                return True
            # Otherwise, simply iterate
            seen.add(curr) # Adding actual Nodes, not values
            curr = curr.next
        return False



"""
    NOTES:
    - Input: a head of a linked list (does not have to be sorted), and a pos pointer 
    which indicates where in the list there is (or there isnt a cycle).
    - Output: Boolean, which represents the result of checking if the list has a cycle.

    Assumptions: our list can be empty, it may or it may not contain a cycle. pos is not a parameter that we put into the function directly. its something that leetcode is going to use.

    we need to traverse through the array. 
    how do we know its a cycle, if we go back to an already visited node?
    do we need to deal with actual memory address?
    It wont make sense to look for the value, but rather we need to look for either a reference.

    Yes, we can use a set to keep track of the elements we have seen before, we iterate and if we find a note that was already present, we return true
    If not, we will complete the iterations, so we can return False as a result.

""" 