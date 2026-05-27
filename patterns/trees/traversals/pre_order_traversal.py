import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from utils.tree_node import TreeNode


def preOrderTraversal(root: TreeNode) -> list[int]:
    """
    Preorder traversal: Root -> Left -> Right
    """
    res = []

    def recurse(node: TreeNode):
        if node is None:
            return
        res.append(node.val)
        recurse(node.left)
        recurse(node.right)
    
    recurse(root)
    return res
    

