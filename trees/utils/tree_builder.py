"""
Utilities to build binary trees from different representations.
"""

from collections import deque
from .tree_node import TreeNode


def build_tree(values):
    """
    Build a binary tree from a list (LeetCode style).
    
    Args:
        values: List of values in level-order. Use None for missing nodes.
                Example: [1, 2, 3, None, 5] creates:
                     1
                    / \\
                   2   3
                    \\
                     5
    
    Returns:
        TreeNode: Root of the constructed tree, or None if values is empty.
    
    Example:
        >>> root = build_tree([1, 2, 3, 4, 5])
        >>> root.val
        1
        >>> root.left.val
        2
    """
    if not values or values[0] is None:
        return None
    
    root = TreeNode(values[0])
    queue = deque([root])
    i = 1
    
    while queue and i < len(values):
        node = queue.popleft()
        
        # Add left child
        if i < len(values) and values[i] is not None:
            node.left = TreeNode(values[i])
            queue.append(node.left)
        i += 1
        
        # Add right child
        if i < len(values) and values[i] is not None:
            node.right = TreeNode(values[i])
            queue.append(node.right)
        i += 1
    
    return root


def tree_to_list(root):
    """
    Convert a binary tree back to a list (level-order with None for missing nodes).
    
    Args:
        root: Root of the binary tree
    
    Returns:
        list: Level-order representation with None for missing nodes
    
    Example:
        >>> root = TreeNode(1, TreeNode(2), TreeNode(3))
        >>> tree_to_list(root)
        [1, 2, 3]
    """
    if not root:
        return []
    
    result = []
    queue = deque([root])
    
    while queue:
        node = queue.popleft()
        if node:
            result.append(node.val)
            queue.append(node.left)
            queue.append(node.right)
        else:
            result.append(None)
    
    # Remove trailing None values
    while result and result[-1] is None:
        result.pop()
    
    return result
