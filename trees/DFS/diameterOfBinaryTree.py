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
    def diameterOfBinaryTree(self, root: TreeNode) -> int:
        # If root does not have children, return 0
        if not root.left and not root.right: 
            return 0
        
        maxDiameterSize = 0
        def dfs(root: TreeNode) -> int:
            nonlocal maxDiameterSize 
            # Base case, no more nodes
            if not root:
                print("no nodes")
                return 0
            # When we are a leaf, then we know our height is 1
            #if not root.left and not root.right:
             #   print("leaf nodes")
              #  return 1
            print('current node: ', root.val, f"Current max diam: {maxDiameterSize}")

        

            leftBranch = dfs(root.left)
            rightBranch = dfs(root.right)
            print(f"leftB: {leftBranch}, rightB: {rightBranch}")
            possibleDiameter = leftBranch + rightBranch
            print("Possible diameter: ", possibleDiameter)
            maxDiameterSize = max(possibleDiameter, maxDiameterSize)
            return 1 + max(leftBranch, rightBranch)
        
        dfs(root)
        return maxDiameterSize
"""
    In only order to build a diameter, we need to build it by adding the height of 
    both branches (left and right)
    So on each recursive call (left and right) we return the current height
    and we propagate this to the parent node

    there is a chance we have different diameters, so when we go through the tree
    we need to keep track of the LONGEST diameter so far, so that in the end we just return it
"""

root = build_tree([1, 2, 3, 4, 5])

printTree(root)

sol = Solution()

#print(sol.diameterOfBinaryTree(root))
print(sol.diameterOfBinaryTree(build_tree([2, 3, None, 1])))