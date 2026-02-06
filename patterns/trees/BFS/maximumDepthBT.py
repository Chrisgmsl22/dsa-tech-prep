import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from utils.tree_builder import build_tree
from utils.tree_node import TreeNode
from utils.tree_printer import printTree

class Solution:
    def maxDepth(self, root: TreeNode) -> int:
        if not root:
            return 0
        collection = []
        queue = [root]
        levels = 0

        while queue:
            levelSize = len(queue)
            print("Current queue: ", queue, levelSize)
            for _ in range(levelSize):
                currNode = queue.pop(0)
                #levelArr.append(currNode.val)
                if currNode.left:
                    queue.append(currNode.left)
                if currNode.right:
                    queue.append(currNode.right)
            levels += 1
        
        # collection has all the levels found
        return levels
                

        
       
    
""" 
   Notes:
   We need to find the MAXIMUM depth of a binary tree. Immediately, we know 2 things:
   We will need to compare some elements with something else (we will need to check which one is larger, max()), and we have a binary tree. So this means we wil have 2 
   branches for each node.

   The way to work for this is that we have to go to the bottom, and then count all of our levels. We can traverse this tree. And for that we are going to need recursion.
   Also, since this is a binary tree, we will need to recurse on all possible branches, binary == 2 == 2 recursive calls

   To solve this we also need to break down the problem into smaller chunks. For traversing we know that our base case will be when our node does not exist (we stop recursing).

   But we also need to know how small this problem can be.
   We can assume that the smalles possible case would be when our current node is only worth 1 level, so if we sum all of the levels we traverse, we will get the biggest possible value.

   Also, since we need to find the max value, then we would need to compare each branch

"""