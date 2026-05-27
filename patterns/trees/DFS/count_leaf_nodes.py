import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from utils.tree_node import TreeNode


class Solution:
    def countLeafNodes(self, root: TreeNode) -> int:
        if not root:
            return 0
        
        if not root.left and not root.right:
            return 1
        
        return self.countLeafNodes(root.left) + self.countLeafNodes(root.right)
