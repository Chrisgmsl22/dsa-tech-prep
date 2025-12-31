import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from utils.tree_builder import build_tree
from utils.tree_node import TreeNode
from utils.tree_printer import printTree
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    # This will act as the recursive function, because it needs to compare 2 subtrees, and on and on
    def isMirror(self, left: TreeNode, right: TreeNode) -> bool:
        # What is going to be our base case?
        if not right and not left:
            return True
        if left is None or right is None:
            return False
        if left.val != right.val:
            return False
        
        leftRes = self.isMirror(left.left, right.right)
        rightRes = self.isMirror(left.right, right.left)
        

        return leftRes and rightRes
            
        

    # This will not be the recursive function, as this will only work as the starting point of the tree
    def isSymmetric(self, root: TreeNode) -> bool:
        return self.isMirror(root.left, root.right)



root = build_tree([1, 2, 2, 3, 4, 4, 3])
falsy = build_tree([1,2,2,None,3,None,3])
printTree(root)
printTree(falsy)

problem = Solution()
print(problem.isSymmetric(root))
# print(problem.isSymmetric(falsy))