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
    def levelOrder(self, root: TreeNode) -> list[list[int]]:
        
        queue = [root]
        res = []

        while queue: # While there is something in my queue
            level = len(queue)
            temp = []
            # We go through each elements in the level (horizontally elements)
            for _ in range(level):
                curr = queue.pop(0)
                temp.append(curr.val)

                if curr.left:
                    # Still unsure if I need to append the whole node or just the value
                    queue.append(curr.left)
                if curr.right:
                    queue.append(curr.right)
            res.append(temp[:])
        
        return res
"""
    Since this is for traversals, we need to go as wide as possible, considering each level and storing 
    its elements.
    For this we need to perform a BFS traversal, which will require a queue
"""
root = build_tree([3, 9, 20, None, None, 15, 7])
sol = Solution()

res = sol.levelOrder(root)
print(res)