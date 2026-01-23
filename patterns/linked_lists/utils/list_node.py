"""
ListNode class - the fundamental building block for linked lists.
"""

class ListNode:
    """
    A node in a singly linked list.
    
    Attributes:
        val: The value stored in the node
        next: Reference to the next node (or None if this is the tail)
    """
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
    
    def __repr__(self):
        return f"ListNode({self.val})"
