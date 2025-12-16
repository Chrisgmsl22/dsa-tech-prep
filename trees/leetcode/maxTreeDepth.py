# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
from trees.classes.tree import TreeNode


class Solution:
    def maxDepth(self, root: TreeNode) -> int:
        
        if not root: 
            return 0

        leftBranch = self.maxDepth(root.left)
        rightBranch = self.maxDepth(root.right)

        return 1 + max(leftBranch, rightBranch)
            
        
    
    
""" 
    NOTES:
    - Input: A tree
    - Output: A number, which represents the maximum depth of the tree, so the longest value
    - Assumptions: Our tree can be empty, and it can contain a large sum of values
    Each node can contain negative values

    - Brainstorming:
        We have a tree, best way to navigate through this tree is using recursion, more specificallt, doing a DFS search
        So that we keep going down and down. How do we know we reach the bottom?
        When our current node does not exist. When we reach this part we can keep track of the longest path, maybe through an index number. 
        We are not iterating so we cannot just count i, we need to force a counter ourselves.
        This mean we can have multiple solutions, or that the value is updated several times, by the time we finish our DFS, we know we will have found the solution

"""