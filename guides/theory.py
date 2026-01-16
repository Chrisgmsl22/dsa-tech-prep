# ===================================
# PART 1: THE NODE CLASS
# ===================================

class TreeNode:
    """Basic building block of a binary tree"""
    def __init__(self, val=0, left=None, right=None):
        self.val = val      # The value stored in this node
        self.left = left    # Reference to left child (or None)
        self.right = right  # Reference to right child (or None)

# Let's build a simple tree manually
print("PART 1: Building a Tree")
print("=" * 40)

# Create individual nodes
root = TreeNode(1)
root.left = TreeNode(2)
root.right = TreeNode(3)
root.left.left = TreeNode(4)
root.left.right = TreeNode(5)

print("We just built this tree:")
print("""
        1
       / \\
      2   3
     / \\
    4   5
""")

print(f"Root value: {root.val}")
print(f"Root's left child: {root.left.val}")
print(f"Root's right child: {root.right.val}")
print(f"Root's left-left grandchild: {root.left.left.val}")

# ===================================
# PART 2: TREE TRAVERSAL WITH RECURSION
# ===================================

print("\n" + "=" * 40)
print("PART 2: Tree Traversal (Visiting Every Node)")
print("=" * 40)

def preorder_traversal(node, depth=0):
    """Visit: Root -> Left -> Right"""
    if node is None:
        return
    
    indent = "  " * depth
    print(f"{indent}Visiting: {node.val}")
    
    preorder_traversal(node.left, depth + 1)
    preorder_traversal(node.right, depth + 1)

print("\nPreorder Traversal (Root -> Left -> Right):")
preorder_traversal(root)

def inorder_traversal(node):
    """Visit: Left -> Root -> Right"""
    if node is None:
        return
    
    inorder_traversal(node.left)
    print(f"Visiting: {node.val}")
    inorder_traversal(node.right)

print("\nInorder Traversal (Left -> Root -> Right):")
inorder_traversal(root)

def postorder_traversal(node):
    """Visit: Left -> Right -> Root"""
    if node is None:
        return
    
    postorder_traversal(node.left)
    postorder_traversal(node.right)
    print(f"Visiting: {node.val}")

print("\nPostorder Traversal (Left -> Right -> Root):")
postorder_traversal(root)

# ===================================
# PART 3: RECURSIVE TREE PATTERN
# ===================================

print("\n" + "=" * 40)
print("PART 3: The Recursive Tree Pattern")
print("=" * 40)

print("""
The KEY insight for tree recursion:

def solve_tree_problem(node):
    # BASE CASE: Empty tree
    if node is None:
        return base_value
    
    # RECURSIVE CASE:
    # 1. Solve for left subtree
    left_result = solve_tree_problem(node.left)
    
    # 2. Solve for right subtree
    right_result = solve_tree_problem(node.right)
    
    # 3. Combine results with current node
    return combine(node.val, left_result, right_result)

This pattern works because:
- Each node trusts its children to solve their subtrees
- Then combines their answers with its own value
""")

# ===================================
# PART 4: EXAMPLE - COUNT NODES
# ===================================

print("\n" + "=" * 40)
print("PART 4: Example - Count Total Nodes")
print("=" * 40)

def count_nodes(node, depth=0):
    """Count total number of nodes in tree"""
    indent = "  " * depth
    
    # Base case: empty tree has 0 nodes
    if node is None:
        print(f"{indent}Empty node → return 0")
        return 0
    
    print(f"{indent}At node {node.val}")
    
    # Recursive case: count left + count right + 1 (current node)
    print(f"{indent}Counting left subtree of {node.val}:")
    left_count = count_nodes(node.left, depth + 1)
    
    print(f"{indent}Counting right subtree of {node.val}:")
    right_count = count_nodes(node.right, depth + 1)
    
    total = 1 + left_count + right_count
    print(f"{indent}Node {node.val}: 1 + {left_count} + {right_count} = {total}")
    
    return total

print("Counting nodes in our tree:")
total = count_nodes(root)
print(f"\nTotal nodes: {total}")

# ===================================
# PART 5: EXAMPLE - TREE SUM
# ===================================

print("\n" + "=" * 40)
print("PART 5: Example - Sum All Values")
print("=" * 40)

def sum_tree(node):
    """Sum all node values in tree"""
    # Base case
    if node is None:
        return 0
    
    # Recursive case: current + left sum + right sum
    left_sum = sum_tree(node.left)
    right_sum = sum_tree(node.right)
    
    return node.val + left_sum + right_sum

print("Summing all values:")
total_sum = sum_tree(root)
print(f"Sum: {total_sum}")
print(f"Calculation: 1 + 2 + 3 + 4 + 5 = {total_sum}")

# ===================================
# PART 6: EXAMPLE - MAXIMUM VALUE
# ===================================

print("\n" + "=" * 40)
print("PART 6: Example - Find Maximum Value")
print("=" * 40)

def find_max(node):
    """Find maximum value in tree"""
    # Base case
    if node is None:
        return float('-inf')  # Negative infinity (smaller than any number)
    
    # Recursive case: max of current, left max, right max
    left_max = find_max(node.left)
    right_max = find_max(node.right)
    
    return max(node.val, left_max, right_max)

print("Finding maximum value:")
max_val = find_max(root)
print(f"Maximum: {max_val}")

# ===================================
# PART 7: YOUR PROBLEM - MAX DEPTH
# ===================================

print("\n" + "=" * 40)
print("PART 7: Maximum Depth of Binary Tree")
print("=" * 40)

def max_depth(node, depth=0):
    """
    Find the maximum depth (longest path from root to leaf)
    
    Depth = number of edges from root to that node
    Or: number of levels in the tree
    """
    indent = "  " * depth
    
    # Base case: empty tree has depth 0
    if node is None:
        print(f"{indent}Empty node → depth 0")
        return 0
    
    print(f"{indent}At node {node.val}")
    
    # Recursive case: 1 + max(left depth, right depth)
    print(f"{indent}Exploring left subtree of {node.val}:")
    left_depth = max_depth(node.left, depth + 1)
    
    print(f"{indent}Exploring right subtree of {node.val}:")
    right_depth = max_depth(node.right, depth + 1)
    
    current_depth = 1 + max(left_depth, right_depth)
    print(f"{indent}Node {node.val}: 1 + max({left_depth}, {right_depth}) = {current_depth}")
    
    return current_depth

print("Our tree:")
print("""
        1
       / \\
      2   3
     / \\
    4   5
""")
print("\nCalculating maximum depth:")
depth = max_depth(root)
print(f"\nMaximum depth: {depth}")

# ===================================
# PART 8: CLEAN VERSION FOR LEETCODE
# ===================================

print("\n" + "=" * 40)
print("PART 8: Clean LeetCode Solution")
print("=" * 40)

class Solution:
    def maxDepth(self, root):
        """
        The clean version you'd submit to LeetCode
        """
        # Base case: empty tree
        if root is None:
            return 0
        
        # Recursive case: 1 + max of subtree depths
        left_depth = self.maxDepth(root.left)
        right_depth = self.maxDepth(root.right)
        
        return 1 + max(left_depth, right_depth)

solution = Solution()
result = solution.maxDepth(root)
print(f"LeetCode solution result: {result}")

# ===================================
# PART 9: WHY RECURSION WORKS FOR TREES
# ===================================

print("\n" + "=" * 40)
print("PART 9: Why Recursion is Perfect for Trees")
print("=" * 40)

print("""
Trees are INHERENTLY RECURSIVE structures!

A binary tree is either:
1. Empty (None) → BASE CASE
2. A node with two subtrees (which are also trees) → RECURSIVE CASE

This natural recursion makes tree problems elegant:

For max depth:
- Empty tree? Depth is 0
- Tree with root? Depth is 1 + max(left depth, right depth)

The recursion handles all the complexity:
- Visiting every node
- Tracking depth
- Comparing subtrees

You just define:
1. What to do with an empty tree (base case)
2. How to combine current node with subtree results (recursive case)
""")

# ===================================
# PART 10: PRACTICE PROBLEMS
# ===================================

print("\n" + "=" * 40)
print("PART 10: Practice Problems to Try")
print("=" * 40)

print("""
Now that you understand the pattern, try these:

BEGINNER:
1. Count leaf nodes (nodes with no children)
2. Check if a value exists in the tree
3. Sum of all leaf node values

INTERMEDIATE:
4. Check if tree is symmetric
5. Minimum depth of binary tree
6. Path sum (check if root-to-leaf path sums to target)

The pattern is always the same:
- Base case: if node is None, return something
- Recursive: solve for left, solve for right, combine with current
""")

# Let me show you one more as an example
print("\n" + "=" * 40)
print("BONUS: Count Leaf Nodes")
print("=" * 40)

def count_leaves(node):
    """Count nodes that have no children"""
    # Base case: empty tree
    if node is None:
        return 0
    
    # Base case: this IS a leaf (no children)
    if node.left is None and node.right is None:
        print(f"Found leaf: {node.val}")
        return 1
    
    # Recursive case: count leaves in subtrees
    left_leaves = count_leaves(node.left)
    right_leaves = count_leaves(node.right)
    
    return left_leaves + right_leaves

leaf_count = count_leaves(root)
print(f"Total leaf nodes: {leaf_count}")