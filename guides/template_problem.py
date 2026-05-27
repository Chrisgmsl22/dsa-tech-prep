"""
Template: Copy this file to start a new tree problem

Problem: [Problem name]
LeetCode: [Number if applicable]
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

from utils.tree_node import TreeNode
from utils.tree_builder import build_tree
from utils.tree_printer import printTree


class Solution:
    def problemName(self, root: TreeNode) -> int:
        """
        [Describe your approach]
        
        Time: O(?)
        Space: O(?)
        """
        # Base case
        if not root:
            return 0
        
        # Recursive case
        left = self.problemName(root.left)
        right = self.problemName(root.right)
        
        # Process and return
        return 1 + max(left, right)


# ============================================================================
# Test your solution - just click run!
# ============================================================================

if __name__ == "__main__":
    solution = Solution()
    
    # Test 1
    print("Test 1:")
    tree = build_tree([1, 2, 3, 4, 5])
    printTree(tree)
    result = solution.problemName(tree)
    print(f"Result: {result}")
    print()
    
    # Test 2
    print("Test 2:")
    tree2 = build_tree([1, None, 2])
    printTree(tree2)
    result2 = solution.problemName(tree2)
    print(f"Result: {result2}")
    print()
    
    # Test 3
    print("Test 3: Empty tree")
    result3 = solution.problemName(None)
    print(f"Result: {result3}")
