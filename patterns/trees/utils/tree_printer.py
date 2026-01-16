"""
Simple tree visualization utility.
"""


def printTree(root, level=0, prefix="Root: "):
    """
    Print tree with indentation showing detailed structure (shows None nodes).
    
    Args:
        root: Root of the tree
        level: Internal use for indentation (default: 0)
        prefix: Label for the node (default: "Root: ")
    
    Example:
        >>> root = TreeNode(1, TreeNode(2), TreeNode(3))
        >>> printTree(root)
        Root: 1
            L--- 2
            R--- 3
    """
    if root is not None:
        tabulation = " " * (level * 4)
        print(tabulation + prefix + str(root.val))
        if root.left is not None or root.right is not None:
            if root.left:
                printTree(root.left, level + 1, "L--- ")
            else:
                print(" " * ((level + 1) * 4) + "L--- None")
            if root.right:
                printTree(root.right, level + 1, "R--- ")
            else:
                print(" " * ((level + 1) * 4) + "R--- None")

