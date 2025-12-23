from platform import node
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from utils.tree_builder import build_tree
from utils.tree_node import TreeNode
from utils.tree_printer import printTree


def bfsTemplateA(root: TreeNode):
    if not root:
        return
    nodes = []
    queue = [root]

    while queue:
        # Option A: Process one node at a time
        currNode = queue.pop(0) # Do something with your node NOW
        # print("A", currNode)
        nodes.append(currNode.val)

        
        # Always add children
        if currNode.left:
            queue.append(currNode.left)
        if currNode.right:
            queue.append(currNode.right)
    return nodes

def bfsTemplateB(root: TreeNode):
    if not root:
        return
    nodes = []
    queue = [root]

    while queue:
        # Option B: Process the entire level
        levelSize = len(queue)
        levelArr = []
        for _ in range(levelSize):
            currNode = queue.pop(0)
            # Do something with node NOW
            # print("B", currNode)
            levelArr.append(currNode.val)
        
            # Always add children
            if currNode.left:
                queue.append(currNode.left)
            if currNode.right:
                queue.append(currNode.right)
        nodes.append(levelArr[:])
    
    return nodes
    

def bfs(root: TreeNode):
    if not root: 
        return

    queue = [root]
    ans = []

    while queue:
        # FIFO
        removedNode = queue.pop(0)
        ans.append(removedNode.val)

        # Add children back to queue
        if removedNode.left:
            queue.append(removedNode.left)
        if removedNode.right:
            queue.append(removedNode.right)

    return ans

def dfs(root: TreeNode, ans = []):

    if root is None:
        return
    
    dfs(root.left, ans)
    dfs(root.right, ans)
    ans.append(root.val)

    return ans



root = build_tree([1, 2, 3, 4, 5, None, 6])
""""
        1
    2       3
4      5        6
"""

#printTree(root)
#print('DFS: ', dfs(root))
print('BFS: ', bfs(root))
print(bfsTemplateA(root))
print("-----------------------------")
print(bfsTemplateB(root))