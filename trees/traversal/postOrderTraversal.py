import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from classes.tree import TreeNode


def postOrderTraversal(node: TreeNode):
    res = []
    def recurse(n: TreeNode):
        if not n: # If we've reached the end, then we stop recursing
            return
        
        recurse(n.left)
        recurse(n.right)
        # Process node
        res.append(n.val)

    recurse(node)
    return res