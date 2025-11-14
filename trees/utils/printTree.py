def print_tree(node, prefix="", is_tail=True):
    """
    Prints a visual tree structure using ASCII characters
    """
    if node is None:
        return
    
    # Print current node
    print(prefix + ("└── " if is_tail else "├── ") + str(node.val))
    
    # Prepare prefix for children
    extension = "    " if is_tail else "│   "
    
    # Get children
    children = []
    if node.left is not None:
        children.append(('L', node.left))
    if node.right is not None:
        children.append(('R', node.right))
    
    # Print children
    for i, (side, child) in enumerate(children):
        is_last = (i == len(children) - 1)
        print_tree(child, prefix + extension, is_last)


def print_tree_levels(root):
    """
    Prints the tree level by level (breadth-first)
    """
    if not root:
        return
    
    from collections import deque
    queue = deque([root])
    level = 0
    
    while queue:
        level_size = len(queue)
        print(f"Level {level}: ", end="")
        
        for i in range(level_size):
            node = queue.popleft()
            print(node.val, end=" ")
            
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        
        print()  # New line after each level
        level += 1


def print_tree_pretty(root, level=0, prefix="Root: "):
    """
    Prints tree with indentation showing structure
    """
    if root is not None:
        tabulation = " " * (level * 4)
        print(tabulation + prefix + str(root.val))
        if root.left is not None or root.right is not None:
            if root.left:
                # if current node has value, recurse and print
                print_tree_pretty(root.left, level + 1, "L--- ")
            else:
                # If current node does not have value, just print None
                print(" " * ((level + 1) * 4) + "L--- None")
            if root.right:
                print_tree_pretty(root.right, level + 1, "R--- ")
            else:
                print(" " * ((level + 1) * 4) + "R--- None")
