"""
Utilities to build linked lists from arrays (LeetCode style).
"""

from .list_node import ListNode


def build_list(values):
    """
    Build a singly linked list from an array (LeetCode style).
    
    Args:
        values: List of values. Example: [1, 2, 3, 4, 5]
                Creates: 1 -> 2 -> 3 -> 4 -> 5 -> None
    
    Returns:
        ListNode: Head of the linked list, or None if values is empty.
    
    Example:
        >>> head = build_list([1, 2, 3])
        >>> head.val
        1
        >>> head.next.val
        2
    """
    if not values:
        return None
    
    # Create head node
    head = ListNode(values[0])
    current = head
    
    # Add remaining nodes
    for i in range(1, len(values)):
        current.next = ListNode(values[i])
        current = current.next
    
    return head


def list_to_array(head):
    """
    Convert a linked list back to an array.
    
    Args:
        head: Head of the linked list
    
    Returns:
        list: Array representation of the linked list
    
    Example:
        >>> head = ListNode(1, ListNode(2, ListNode(3)))
        >>> list_to_array(head)
        [1, 2, 3]
    """
    result = []
    current = head
    
    while current:
        result.append(current.val)
        current = current.next
    
    return result
