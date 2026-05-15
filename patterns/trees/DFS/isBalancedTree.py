"""
Given a binary tree, determine if it is height-balanced.

 

"""
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from utils.tree_builder import build_tree
from utils.tree_node import TreeNode
from utils.tree_printer import printTree

class Solution:
    def isBalanced(self, root: TreeNode) -> bool:
        isBalanced = True

        def recurse(node: TreeNode):
            nonlocal isBalanced
            if not node:
                return 0
            
            leftHeight = recurse(node.left)
            rigthHeight = recurse(node.right)

            if abs(leftHeight - rigthHeight) > 1:
                isBalanced = False
            
            return 1 + max(leftHeight, rigthHeight)
        
        recurse(root)
        return isBalanced


sol = Solution()

root = build_tree([3,9,20,None,None,15,7])
printTree(root)
res = sol.isBalanced(root)

print("Final result: ", res)