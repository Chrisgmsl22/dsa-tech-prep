import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from utils.tree_builder import build_tree
from utils.tree_node import TreeNode
from utils.tree_printer import printTree

"""
    Given a binary tree, find its minimum depth.

The minimum depth is the number of nodes along the shortest path from the root node down to the nearest leaf node.

Note: A leaf is a node with no children.
"""
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def minDepth(self, root: TreeNode) -> int:
        queue = [root]
        ans: int = 0

        while queue:
            ans += 1 # We know we are one level deep
            levelL = len(queue)
            
            for _ in range(levelL):
                currNode = queue.pop(0)

                if currNode.left:
                    queue.append(currNode.left)
                elif currNode.right:
                    queue.append(currNode.right)
                elif not currNode.right and not currNode.left:
                    # Then we know its a leaf node
                    return ans
            


"""
    We need to find the MINIMUM height. A height is the sum of all the nodes
    that go from A node to B node. In our case its about the root
    So we need to go from the root to an N node, and calculate its height.
    We could store this height somehow to keep track of if and update it as we go

    This sounds a lot like a DFS problem, but I think all DFS problems could
    techincally be solved with BFS.

    The way to know our height can be calculated is if our starting node is a root
    and our last node is a leaf (meaning it has no children)

    we do a BFS, and for each level that is not a root, we check if our current nodes are leaves, if they are, then we can break the loop, because we will
    already start from the beginning, so there could not be a smaller?
    Or maybe we keep track of it

    then we return the level number in which the depht was found
"""


root = build_tree([3, 9, 20, None, None, 15, 7])
sol = Solution()

res = sol.minDepth(root)
print(res)