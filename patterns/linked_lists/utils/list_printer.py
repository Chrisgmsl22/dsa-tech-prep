"""
Utility to visualize linked lists.
"""


def printList(head):
    """
    Print a linked list in a visual format.
    
    Args:
        head: Head of the linked list
    
    Example:
        >>> head = ListNode(1, ListNode(2, ListNode(3)))
        >>> printList(head)
        1 -> 2 -> 3 -> None
    """
    if not head:
        print("Empty list: None")
        return
    
    # Collect all values
    values = []
    current = head
    
    # Prevent infinite loops (detect cycles)
    visited = set()
    while current:
        if id(current) in visited:
            values.append(f"[CYCLE detected at {current.val}]")
            break
        
        visited.add(id(current))
        values.append(str(current.val))
        current = current.next
    
    # Print with arrows
    result = " -> ".join(values) + " -> None"
    print(result)


