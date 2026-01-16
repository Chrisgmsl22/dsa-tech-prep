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
    def hasPathSum(self, root: TreeNode, targetSum: int) -> bool:
        if not root:
            return False

        def helper(root: TreeNode, currSum: int, targetSum: int):
            # If curr node is a leaf node
            if (root):
                currSum += root.val
                
                if (not root.left and not root.right):
                    print('base case hit', root.val)
                    return currSum == targetSum
            
                print(root.val, "Current val: ", currSum)
            
                # Keep going
            
                return helper(root.left, currSum, targetSum) or helper(root.right, currSum, targetSum)
                

                ## Maybe we need to backtrack and remove our used node's value
                print(f"Curr Node: {root.val}, currSum: {currSum} currSum - val {currSum - root.val}")
                currSum -= root.val
            else:
                return False

        
        return helper(root, 0, targetSum)
    def hasPathSum2(self, root: TreeNode, targetSum: int) -> bool:
        def helper(root: TreeNode, currSum: int):
            if not root: 
                return False
            # base case, we are a leaf node

            currSum += root.val
            if (not root.left and not root.right):
                return currSum == targetSum
            
            leftBranch = helper(root.left, currSum)
            rightBranch = helper(root.right, currSum)

            return leftBranch or rightBranch

        return helper(root, 0)


root = build_tree([5, 4, 8, 11, None, 13, 4, 7, 2, None, None, None, 1])

target = 22
#printTree(root)
sol = Solution()
print(sol.hasPathSum2(root, target))

secRoot = build_tree([1, 2])
#printTree(secRoot)
print(sol.hasPathSum2(secRoot, 1))


""""
    NOTES:
    Input: an imperfect binary tree and a number target
    Output: Boolean, which represents if there is a path that can sum up all nodes from root to leaf equal to the target
    Assumptions: There is always a target, target is integer, but the outcome of the operation is boolean (keep this in mind for recursion)

    Brainstorm approach:
        - We need to navigate through all the nodes in our tree, in this case, since we care about the root-to-lead relation
        then we need to go as deep as possible first, DEEP === Depth === DFS. So this DFS will always account for the current node value
        and it will propagate down to the leaf node.
        If we are in a leaf node (if root is None), we check if the sum made so far equals to target, if so, return true and stop recursing
        If not, return false and continue the work

        After this search is completed we should know if there is a valid path or not
"""