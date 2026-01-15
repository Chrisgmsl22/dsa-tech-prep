import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from utils.tree_builder import build_tree
from utils.tree_node import TreeNode
from utils.tree_printer import printTree
"""
    Given the root of a binary tree, return the average value of the nodes on each level in the form of an array. Answers within 10-5 of the actual answer will be accepted.

"""
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def averageOfLevels(self, root: TreeNode) -> list[float]:
        queue: list[TreeNode] = [root] # Start with the root
        res: list[list[int]] = []
        averageArr: list[int] = []

        while queue:
            levelLength = len(queue)
            temp = [] # This will hold our values temporarily

            for _ in range(levelLength):
                currNode = queue.pop(0)
                temp.append(currNode.val)

                if currNode.left:
                    queue.append(currNode.left)
                if currNode.right:
                    queue.append(currNode.right)
            # Once we're done on our current level, we add our list to res
            res.append(temp[:])
        
        # Up to this point we should have something like
        # [[3], [9, 20], [15, 7]]
        # We go over the array again
        for level in res:
            # Level should be an array
            totalSum = sum(level)
            average = totalSum / len(level)
            averageArr.append(average)
        
        return averageArr


root = build_tree([3, 9, 20, None, None, 15, 7])

sol = Solution()

print(sol.averageOfLevels(root))

"""
    We need to get the average values for EACH LEVEL, that
    means we need to traverse through our tree and find a way to get
    the current value, add it to an array.

    Then, once we're done, we need to go over each element in our array
    this would turn them into an array of arrays, for each element
    we will sum all their values and divide them by their length, once
    we ger this value, we will append it to a new array
"""