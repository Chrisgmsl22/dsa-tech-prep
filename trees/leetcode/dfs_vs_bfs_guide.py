"""
DFS vs BFS Decision Guide
When to use which traversal method?
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from utils.tree_builder import build_tree
from utils.tree_node import TreeNode
from utils.tree_printer import printTree


# ============================================================================
# ✅ USE DFS: Problems about DEPTH, HEIGHT, PATHS
# ============================================================================

def maxDepth(root: TreeNode) -> int:
    """
    LeetCode 104: Maximum Depth of Binary Tree
    
    WHY DFS? We need to explore ALL THE WAY DOWN to find depth.
    DFS naturally goes deep before wide.
    
    Time: O(n), Space: O(h) where h = height
    """
    if not root:
        return 0
    
    # Go all the way left, then all the way right
    left_depth = maxDepth(root.left)
    right_depth = maxDepth(root.right)
    
    return 1 + max(left_depth, right_depth)


def hasPathSum(root: TreeNode, targetSum: int) -> bool:
    """
    LeetCode 112: Path Sum
    Check if there's a root-to-leaf path that sums to targetSum.
    
    WHY DFS? We need to explore COMPLETE PATHS from root to leaf.
    DFS follows one path all the way down before backtracking.
    
    Time: O(n), Space: O(h)
    """
    if not root:
        return False
    
    # Reached a leaf?
    if not root.left and not root.right:
        return targetSum == root.val
    
    # Explore left and right paths
    remaining = targetSum - root.val
    return hasPathSum(root.left, remaining) or hasPathSum(root.right, remaining)


def isSymmetric(root: TreeNode) -> bool:
    """
    LeetCode 101: Symmetric Tree
    Check if tree is mirror image of itself.
    
    WHY DFS? We need to COMPARE left and right subtrees.
    DFS naturally compares corresponding nodes in both subtrees.
    
    Time: O(n), Space: O(h)
    """
    def isMirror(left: TreeNode, right: TreeNode) -> bool:
        if not left and not right:
            return True
        if not left or not right:
            return False
        
        # Check: values match AND subtrees are mirrors
        return (left.val == right.val and
                isMirror(left.left, right.right) and
                isMirror(left.right, right.left))
    
    if not root:
        return True
    return isMirror(root.left, root.right)


def isValidBST(root: TreeNode) -> bool:
    """
    LeetCode 98: Validate Binary Search Tree
    Check if tree is a valid BST.
    
    WHY DFS? We need to CHECK PROPERTIES as we go deep.
    Each node must be within a valid range.
    
    Time: O(n), Space: O(h)
    """
    def validate(node: TreeNode, min_val: float, max_val: float) -> bool:
        if not node:
            return True
        
        # Current node must be in valid range
        if node.val <= min_val or node.val >= max_val:
            return False
        
        # Left subtree: all values < node.val
        # Right subtree: all values > node.val
        return (validate(node.left, min_val, node.val) and
                validate(node.right, node.val, max_val))
    
    return validate(root, float('-inf'), float('inf'))


# ============================================================================
# ✅ USE BFS: Problems about LEVELS, SHORTEST DISTANCE
# ============================================================================

def levelOrder(root: TreeNode) -> list[list[int]]:
    """
    LeetCode 102: Binary Tree Level Order Traversal
    Return nodes grouped by level.
    
    WHY BFS? Problem explicitly asks for LEVEL-BY-LEVEL.
    BFS processes one level at a time.
    
    Time: O(n), Space: O(w) where w = max width
    """
    if not root:
        return []
    
    queue = [root]
    result = []
    
    while queue:
        level_size = len(queue)
        current_level = []
        
        for _ in range(level_size):
            node = queue.pop(0)
            current_level.append(node.val)
            
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        
        result.append(current_level)
    
    return result


def rightSideView(root: TreeNode) -> list[int]:
    """
    LeetCode 199: Binary Tree Right Side View
    Return rightmost node at each level.
    
    WHY BFS? Need to process LEVEL BY LEVEL.
    At each level, we take the last node.
    
    Time: O(n), Space: O(w)
    """
    if not root:
        return []
    
    queue = [root]
    result = []
    
    while queue:
        level_size = len(queue)
        
        for i in range(level_size):
            node = queue.pop(0)
            
            # Last node of this level
            if i == level_size - 1:
                result.append(node.val)
            
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
    
    return result


def minDepth(root: TreeNode) -> int:
    """
    LeetCode 111: Minimum Depth
    Find shortest path from root to any leaf.
    
    WHY BFS? We want SHORTEST path.
    BFS finds the first leaf it encounters = shortest!
    
    Note: Can also solve with DFS, but BFS is more efficient here.
    
    Time: O(n), Space: O(w)
    """
    if not root:
        return 0
    
    queue = [(root, 1)]  # (node, depth)
    
    while queue:
        node, depth = queue.pop(0)
        
        # Found first leaf? That's the minimum depth!
        if not node.left and not node.right:
            return depth
        
        if node.left:
            queue.append((node.left, depth + 1))
        if node.right:
            queue.append((node.right, depth + 1))
    
    return 0


# ============================================================================
# 🤔 EITHER WORKS: Some problems can use both
# ============================================================================

def invertTree_DFS(root: TreeNode) -> TreeNode:
    """
    LeetCode 226: Invert Binary Tree (DFS approach)
    
    DFS feels more natural here - recursively swap subtrees.
    """
    if not root:
        return None
    
    # Swap children
    root.left, root.right = root.right, root.left
    
    # Recurse
    invertTree_DFS(root.left)
    invertTree_DFS(root.right)
    
    return root


def invertTree_BFS(root: TreeNode) -> TreeNode:
    """
    LeetCode 226: Invert Binary Tree (BFS approach)
    
    BFS works too - swap at each level.
    """
    if not root:
        return None
    
    queue = [root]
    
    while queue:
        node = queue.pop(0)
        
        # Swap children
        node.left, node.right = node.right, node.left
        
        if node.left:
            queue.append(node.left)
        if node.right:
            queue.append(node.right)
    
    return root


# ============================================================================
# 📝 QUICK DECISION FLOWCHART
# ============================================================================

def print_decision_guide():
    """
    Quick decision guide printed to console.
    """
    guide = """
╔══════════════════════════════════════════════════════════════════╗
║                  DFS vs BFS DECISION GUIDE                       ║
╚══════════════════════════════════════════════════════════════════╝

🔍 USE DFS WHEN:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Problem mentions: "depth", "height", "path", "subtree"
✅ You need to explore ALL THE WAY DOWN before backtracking
✅ Comparing left and right subtrees
✅ Validating tree properties (BST, balanced, etc.)
✅ Finding all paths from root to leaf
✅ Checking if something exists along a path

📌 DFS KEYWORDS: depth, height, path, validate, symmetric, subtree

📌 COMMON DFS PROBLEMS:
   - Maximum/Minimum Depth (104, 111*)
   - Path Sum (112, 113, 437)
   - Symmetric Tree (101)
   - Same Tree (100)
   - Validate BST (98)
   - Balanced Tree (110)
   - Diameter of Tree (543)
   - Lowest Common Ancestor (236)
   - Count Good Nodes (1448)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🌊 USE BFS WHEN:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Problem mentions: "level", "layer", "row", "shortest"
✅ You need to process nodes LEVEL BY LEVEL
✅ Finding shortest distance/path from root
✅ Need to group results by level
✅ "What nodes are at distance K?"
✅ "Average/sum of each level"

📌 BFS KEYWORDS: level, layer, shortest, nearest, row, distance

📌 COMMON BFS PROBLEMS:
   - Level Order Traversal (102, 107, 103)
   - Right/Left Side View (199)
   - Minimum Depth* (111)
   - Average of Levels (637)
   - Zigzag Level Order (103)
   - Largest Value in Each Row (515)
   - Binary Tree Width (662)

*Can use both, but BFS is better

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🤔 EITHER WORKS:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Simple operations on every node (use DFS, it's simpler)
✅ Invert Tree (226) - DFS more intuitive
✅ Count nodes (222) - DFS simpler
✅ Sum of all nodes - DFS simpler

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💡 QUICK DECISION:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Ask yourself:

1️⃣  Does the problem mention "level", "layer", or "row"?
    → YES: Use BFS
    → NO: Keep reading...

2️⃣  Do you need the SHORTEST distance/path?
    → YES: Use BFS
    → NO: Keep reading...

3️⃣  Are you exploring complete PATHS from root to leaf?
    → YES: Use DFS
    → NO: Keep reading...

4️⃣  Are you comparing or validating subtrees?
    → YES: Use DFS
    → NO: Keep reading...

5️⃣  Default: Use DFS (it's simpler and more intuitive for trees)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 COMPLEXITY COMPARISON:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

                Time        Space
DFS:            O(n)        O(h)    h = height (best: log n, worst: n)
BFS:            O(n)        O(w)    w = width (best: 1, worst: n/2)

Balanced tree:  DFS wins on space (O(log n) vs O(n/2))
Skewed tree:    Same space complexity

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎯 PRO TIP: When in doubt, start with DFS!
   - Most tree problems use DFS
   - DFS code is usually shorter
   - Recursion is more natural for trees
"""
    print(guide)


# ============================================================================
# Run Examples
# ============================================================================

if __name__ == "__main__":
    print_decision_guide()
    
    print("\n" + "="*70)
    print("TESTING WITH EXAMPLE TREE")
    print("="*70)
    
    root = build_tree([3, 9, 20, None, None, 15, 7])
    """
            3
        9       20
              15  7
    """
    printTree(root)
    
    print("\n🔍 DFS EXAMPLES:")
    print(f"Max Depth (DFS): {maxDepth(root)}")
    print(f"Has Path Sum 12 (DFS): {hasPathSum(root, 12)}")
    print(f"Is Symmetric (DFS): {isSymmetric(root)}")
    
    print("\n🌊 BFS EXAMPLES:")
    print(f"Level Order (BFS): {levelOrder(root)}")
    print(f"Right Side View (BFS): {rightSideView(root)}")
    print(f"Min Depth (BFS): {minDepth(root)}")

