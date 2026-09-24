# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def deleteDuplicates(self, head: ListNode | None) -> ListNode | None:
        seen = set()

        curr = head # new node, points at the head
        prev = None
        while curr:
            # Process
            if curr.val not in seen:
                seen.add(curr.val)
                prev = curr
                curr = curr.next # advance
                
            else:
                # Means we have a duplicate
                prev.next = curr.next # Point prev to next node
                curr.next = None # Disconnect duplicate from list
                curr = prev.next
            # traverse
        
        return head
            
        """
            OPTIMAL:
            res = head

        curr = head
        while curr: # As long as there is a node, lets traverse
            while curr.next and curr.val == curr.next.val:
                # We found a duplicate, lets connect skip it
                curr.next = curr.next.next
            
            curr = curr.next # Let's go forward
        
        return res

        """


"""
    NOTES: 
    - Input: a head node, which in leetcode is represented by an array of numbers 
    - Output: a linked list, which will represent the initial list with all duplicates removed.

    One thing to note here is that our list will be sorted, so, if we're having duplicates, it will only
    be adjacent to the current node that we have.

    Things I need to remember: How to traverse a linked list. Since I don't know the length of a linked list
    I can use a more permament loop (while node exists)

    Then, as soon as I see a number, I could keep track of the uniques?
    first one is unique, we add it to a seen set
    We continue, if current number in set? yes, so instead of deleting or doing something too aggresive.
    We can link our previous one to the next node
    
    This means we can also rely on extra memory to keep our previous node as a backup


"""